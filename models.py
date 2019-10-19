from location import Location
import time

class Value:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

class Measurement:
    def __init__(self, row):
        self.parameter = row["parameter"]
        self.value = Value(row["value"], row["unit"])
        self.location = Location.location_factory(row["location"])
        self.source = row["source"]
        self.time = time.strptime(time.strptime(data['date']['utc'],
            "%Y-%m-%dT%H:%M:%S.%fZ")
        
        
