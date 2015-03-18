from django.db import models

# Create your models here.


class Point:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
