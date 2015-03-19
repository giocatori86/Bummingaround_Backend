from django.db import models

# Create your models here.


class Point:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


class Venue:
    def __init__(self, _id, lat, long, name, address):
        self.id = _id
        self.lat = lat
        self.long = long
        self.name = name
        self.address = address

    def serialize(self):
        return {
            'id': self.id,
            'lat': self.lat,
            'long': self.long,
            'name': self.name,
            'address': self.address
        }