import sqlite3
from models import Measurement
import location
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interpolate
import math
from pyproj import Proj
from make_json import make_json

conn = sqlite3.connect('weather-store.db')
col_headers = ("source", "value", "unit", "latitude", "longitude", "confidence", "date")

def fetch_measurements_for_parameter(con, param_name):
    cursorObj = con.cursor()
    table_name = param_name + "_parameter"
    print(table_name)
    cursorObj.execute('SELECT * FROM ' + table_name)
    rows = cursorObj.fetchall()

    print("Finish fetching all rows.")
    measurements = []
    for row in rows:
        row_dict = dict(zip(col_headers, row))
        row_dict['parameter'] = param_name
        measurement = Measurement(row_dict)
        measurements.append(measurement)
    print("Finish converting to measurement objects.")
    return measurements

def plot_data_on_map(measurements):
    print("Converting locations to cartesian")
    for measurement in measurements:
        measurement.convert_location_to_cartesian()
    print("Getting x and y vals")
    coords = zip(*[measurement.location.as_tuple() for measurement in measurements])
    x_vals, y_vals = list(map(np.array, coords))
    print("Ready to plot")
    # print(x_vals)
    # print(y_vals)
    plt.plot(x_vals, y_vals, 'k.')
    plt.show()


def get_latest_measurements(measurements):
    sources = {}
    for measurement in measurements:
        location = measurement.location.as_tuple()
        sources[location] = measurement
    return list(sources.values())

def measurements_to_cartesian_points(measurements):
    for measurement in measurements:
        measurement.convert_location_to_cartesian()
    data_points = [(measurement.location.as_tuple(), measurement.value.value) for measurement in measurements]
    pts, z = list(zip(*data_points))
    print(len(pts))
    print(len(z))
    return pts, z

def find_grid_boundaries(pts):
    x, y = zip(*pts)
    return (min(x), max(x)), (min(y), max(y))

def make_mesh_grid(pts, cellsize=1000):
    x_bounds, y_bounds = find_grid_boundaries(pts)
    xmin, xmax = x_bounds
    ymin, ymax = y_bounds
    ncol = int(math.ceil(xmax-xmin)) / cellsize 
    nrow = int(math.ceil(ymax-ymin)) / cellsize

    gridx, gridy = np.mgrid[xmin:xmax:ncol*1j, ymin:ymax:nrow*1j]
    return gridx, gridy

def interpolate_measurements(measurements, interptype='griddata'):
    pts, z = measurements_to_cartesian_points(measurements)
    gridx, gridy = make_mesh_grid(pts)
    if interptype == 'griddata':
        grid = interpolate.griddata(pts, z, (gridx, gridy), method='linear', fill_value=-3e30)
    elif interptype == 'rbf':
        ptx, pty = list(zip(*pts))
        f = interpolate.Rbf(ptx, pty, z, function='linear')
        grid = f(gridy, gridx)
    elif interptype == 'gauss':
        from sklearn.gaussian_process import GaussianProcess
        ptx, pty = list(zip(*pts))
        ptx = np.array(ptx)
        pty = np.array(pty)
        z = np.array(z)
        print(math.sqrt(np.var(z)))
        gp = GaussianProcess(regr='quadratic',corr='cubic',theta0=np.min(z),thetaL=min(z),thetaU=max(z),nugget=0.05)
        gp.fit(X=np.column_stack([pty,ptx]),y=z)
        rr_cc_as_cols = np.column_stack([gridy.flatten(), gridx.flatten()])
        grid = gp.predict(rr_cc_as_cols).reshape((ncol,nrow))
    return gridx, gridy, grid    

def cartesian_pt_to_geo(pt):
    x, y = pt
    lat, lon = location.p(x, y, inverse=True)
    return (lat, lon)


# from pprint import pprint
# pprint(fetch_measurements_for_parameter(conn, "co"))
measurements = fetch_measurements_for_parameter(conn, "co")
measurements = get_latest_measurements(measurements)
gridx, gridy, grid = interpolate_measurements(measurements, interptype='rbf')
output_pts = zip(np.nditer(gridx), np.nditer(gridy))
output_z = list(np.nditer(grid))
output_z = [float(z) for z in output_z]
# output_z = [x[0] for x in output_z]
output_pts = list(map(cartesian_pt_to_geo, list(output_pts)))

OUTPUT_FILENAME = 'out.json'
success = make_json(output_z, output_pts, OUTPUT_FILENAME)
if success == 1:
    print("Grid succesfully written to json")
else:
    raise IOError("Writing to json file unsucessful")
