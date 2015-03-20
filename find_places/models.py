import json
import logging
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


def load_venues_from_triple_json(triple_json):
    venues = []
    for line in triple_json['results']['bindings']:
        try:
            venue = Venue(
                line['id']['value'],
                line['lat']['value'],
                line['lon']['value'],
                line['label']['value'],
                "no address"  # TODO add address to the query
            )
            venues.append(venue)
        except KeyError:
            logging.error("line: {}".format(json.dumps(line)))
            raise
    return venues