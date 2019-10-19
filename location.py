from math import radians, cos, sin, asin, sqrt

class Coordinate:
    def __init__(self, latitude, longitude):
        self.longitude = longitude
        self.latitude = latitude
    
    def as_tuple(self):
        return (self.latitude, self.longitude)

def dist_between_coords(coord1, coord2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)

    From: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    lon1, lat1 = coord1.as_tuple()
    lon2, lat2 = coord2.as_tuple()
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
