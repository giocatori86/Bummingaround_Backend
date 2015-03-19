import logging
import json

from rdflib import Graph, Namespace
from rdflib.namespace import OWL
import requests

from find_places.foursquare.data import Venue
from find_places.graphdb import GraphDB


__author__ = 'matteo'

CLIENT_ID = "4ONXH4IGRDUDFI2TBYITRJINHKBYQOTMWQAGHMXVB2GXDC0J"
CLIENT_SECRET = "T1MLXE4ZCTS1CCB0CODY1Q1KYDRPRF4IF2URBS0P0FU5LT33"
MELKWEG_FOURSQUARE_ID = "4a2703c8f964a52066851fe3"


def download_data():
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'v': 20150201,
        'm': 'foursquare'
    }

    try:
        r = requests.get("https://api.foursquare.com/v2/venues/{}".format(MELKWEG_FOURSQUARE_ID), params=payload)

        logging.debug("response from server: {}".format(r.text))
    except Exception as e:
        logging.error("request exception: {}".format(e))
        raise e

    j = json.loads(r.text)
    code = j['meta']['code']
    if code != 200:
        raise Exception("HTTP code different from 200 ({})".format(code))

    return j


def search_on_coordinates(lat, long, radius):
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'v': 20150201,
        'm': 'foursquare',
        'll': '{},{}'.format(lat, long),
        'radius': radius
    }

    logging.info("payload: {}".format(dump_to_json(payload)))

    try:
        r = requests.get("https://api.foursquare.com/v2/venues/search", params=payload)

        logging.debug("response from server: {}".format(r.text))
    except Exception as e:
        logging.error("request exception: {}".format(e))
        raise e

    j = json.loads(r.text)
    code = j['meta']['code']
    if code != 200:
        raise Exception("HTTP code different from 200 ({})".format(code))

    return j


def load_file_data(file_path):
    json_file = open(file_path)
    json_data = json.load(json_file)
    json_file.close()
    return json_data


def dump_to_json(o):
    return json.dumps(o, default=lambda _o: _o.__dict__)


class FoursquareTripleStore():
    filename = "foursquare.ttl"
    file_type = "turtle"

    def __init__(self):
        self.graph = Graph()
        self.graph.bind("owl", OWL)
        self.fs = Namespace("https://api.foursquare.com/v2/venues/")
        self.graph.bind("fs", self.fs)
        self.dcterms = Namespace("http://purl.org/dc/terms/")
        self.graph.bind("dcterms", self.dcterms)

        self.graphDB = GraphDB()

        self._create_classes()

    def _create_classes(self):
        Venue.save_class_definitions(self)

    def save(self):
        ttl = self.graph.serialize(format=self.file_type)
        self.graphDB.add_turtle(ttl)

    def add(self, s, p, o):
        self.graph.add((s, p, o))

    def set(self, s, p, o):
        self.graph.set((s, p, o))

    def remove(self, s, p, o):
        self.graph.remove((s, p, o))


if __name__ == '__main__':
    LOG_FORMAT = "%(asctime)-15s:%(levelname)-8s:%(threadName)s:%(filename)s:%(funcName)s: %(message)s"
    LOG_LEVEL = logging.DEBUG
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
    logging.info("starting application")

    response = search_on_coordinates(52.364822, 4.881493, 10)
    # response = load_file_data("/home/matteo/Documenti/VU/Intelligent Web Applications/foursquare.json")
    logging.info("data: {}".format(response['meta']))
    store = FoursquareTripleStore()
    for venue_json in response['response']['venues']:
        venue = Venue(venue_json)
        logging.info("venue: {}".format(dump_to_json(venue)))
        venue.save_in_triple_store(store)
    store.save()
