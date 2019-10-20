from location import GeoCoordinate, geo_to_cartesian
import time

class Value:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

class Measurement:
    def __init__(self, row):
        self.parameter = row["parameter"]
        self.value = Value(row["value"], row["unit"])
        self.location_geo = GeoCoordinate(row["latitude"], row["longitude"])
        self.location = self.location_geo
        self.source = row["source"]
        self.time = time.strptime(row['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.confidence = row['confidence']        
        

    def convert_location_to_cartesian(self):
        self.location_cart = geo_to_cartesian(self.location_geo)
        self.location = self.location_cart

    def convert_location_to_geo(self):
        self.location = self.location_geo
