from pyproj import Proj
from math import radians, cos, sin, asin, sqrt, atan2

p = Proj(proj='utm',zone=10,ellps='WGS84', preserve_units=False)
class Coordinate:
    def __init__(self):
        raise NotImplementedError("Coordinate is an abstract class")

    def as_tuple(self):
        raise NotImplementedError("method is an abstract method")

class GeoCoordinate(Coordinate):
    def __init__(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude
    
    def as_tuple(self):
        return (self.latitude, self.longitude)

class CartesianCoordinate(Coordinate):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def as_tuple(self):
        return (self.x, self.y)

def geo_to_cartesian(geo_coord):
    # print(geo_coord.longitude, geo_coord.latitude)
    x,y = p(geo_coord.longitude, geo_coord.latitude)
    
    return CartesianCoordinate(x, y)

def measurement_to_cartesian(measurement):
    measurement.location = geo_to_cartesian(measurement.location)
    return measurement

def measurements_to_cartesian(measurements):
    return list(map(measurement_to_cartesian, measurements))



def dist_between_coords(coord1, coord2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)

    From: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    lat1, lon1 = coord1.as_tuple()
    lat2, lon2 = coord2.as_tuple()
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def bearing_between_coordinates(coord1, coord2):
    lat1, lon1 = coord1.as_tuple()
    lat2, lon2 = coord2.as_tuple()
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    
    y = sin(dlon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)

    brng = atan2(y, x)
    brng = degrees(brng)
    brng = (brng + 360) % 360
    return brng
