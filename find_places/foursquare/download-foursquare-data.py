from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import OWL, RDF
import requests
import logging
import json

__author__ = 'matteo'

CLIENT_ID = "4ONXH4IGRDUDFI2TBYITRJINHKBYQOTMWQAGHMXVB2GXDC0J"
CLIENT_SECRET = "T1MLXE4ZCTS1CCB0CODY1Q1KYDRPRF4IF2URBS0P0FU5LT33"
MELKWEG_FOURSQUARE_ID = "4a2703c8f964a52066851fe3"

LOG_FORMAT = "%(asctime)-15s:%(levelname)-8s:%(threadName)s:%(filename)s:%(funcName)s: %(message)s"
LOG_LEVEL = logging.DEBUG


def __init__():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
    logging.info("starting application")


class Provider():
    def __init__(self, json_data):
        self.name = json_data['name']
        self.urlText = json_data['urlText']
        # ignoring icon

    def save_in_triple_store(self, _store):
        provider_URI = _store.fsevent["provider/" + self.name]
        _store.add(provider_URI, RDF.type, _store.fsevent.Provider)
        # _store.add(provider_URI, _store.fs.name, Literal(self.name))
        _store.add(provider_URI, _store.fs.urlText, Literal(self.urlText))

        return provider_URI

    @staticmethod
    def save_class_definitions(_store):
        _store.add(_store.fsevent.Provider, RDF.type, OWL.Class)


class Category():
    def __init__(self, json_data):
        self.id = json_data['id']
        self.name = json_data['name']
        self.pluralName = json_data['pluralName']
        self.shortName = json_data['shortName']
        self.primary = json_data['primary']
        # ignoring icon

    def save_in_triple_store(self, _store):
        category_URI = _store.fs["category/" + self.id]
        _store.add(category_URI, RDF.type, _store.fs.Category)
        _store.add(category_URI, _store.fs.name, Literal(self.name))
        _store.add(category_URI, _store.fs.shortName, Literal(self.shortName))
        _store.add(category_URI, _store.fs.pluralName, Literal(self.pluralName))
        _store.add(category_URI, _store.fs.primary, Literal(self.primary))

        return category_URI

    @staticmethod
    def save_class_definitions(_store):
        _store.add(_store.fs.Category, RDF.type, OWL.Class)


class Event():
    def __init__(self, json_data):
        self.id = json_data['id']
        self.name = json_data['name']
        self.allDay = json_data['allDay']
        self.timeZone = json_data['timeZone']
        self.text = json_data['text']
        self.url = json_data['url']
        self.provider = Provider(json_data['provider'])
        # ignoring stats
        # ignoring images

        # Duration
        if self.allDay:
            self.date = json_data['date']
        else:
            self.startAt = json_data['startAt']
            self.endAt = json_data['endAt']

        # Categories
        self.categories = []
        for category in json_data['categories']:
            self.categories.append(Category(category))

    def save_in_triple_store(self, _store):
        event_URI = _store.fsevent[self.id]
        _store.add(event_URI, RDF.type, _store.fs.Event)
        _store.add(event_URI, _store.fs.name, Literal(self.name))
        _store.add(event_URI, _store.fs.timeZone, Literal(self.timeZone))
        _store.add(event_URI, _store.fsevent.text, Literal(self.text))
        _store.add(event_URI, _store.fs.url, URIRef(self.url))

        _store.add(event_URI, _store.fsevent.allDay, Literal(self.allDay))
        if self.allDay:
            _store.add(event_URI, _store.fsevent.date, Literal(self.date))
        else:
            _store.add(event_URI, _store.fsevent.startAt, Literal(self.startAt))
            _store.add(event_URI, _store.fsevent.endAt, Literal(self.endAt))

        provider_URI = self.provider.save_in_triple_store(_store)
        _store.add(event_URI, _store.fsevent.provider, provider_URI)

        for category in self.categories:
            category_URI = category.save_in_triple_store(_store)
            _store.add(event_URI, _store.fsevent.category, category_URI)

        return event_URI

    @staticmethod
    def save_class_definitions(_store):
        _store.add(_store.fs.Event, RDF.type, OWL.Class)
        Provider.save_class_definitions(_store)
        Category.save_class_definitions(_store)


class Location():
    def __init__(self, json_data):
        self.address = json_data['address']
        self.crossStreet = json_data['crossStreet']
        self.lat = json_data['lat']
        self.lng = json_data['lng']
        self.postalCode = json_data['postalCode']
        self.cc = json_data['cc']
        self.city = json_data['city']
        self.state = json_data['state']
        self.country = json_data['country']
        self.formattedAddress = "\n".join(json_data['formattedAddress'])

    @staticmethod
    def save_class_definitions(_store):
        _store.add(_store.fs.Location, RDF.type, OWL.Class)

    def save_in_triple_store(self, _store):
        location_node = _store.fs['location/' + str(self.lat) + ":" + str(self.lng)]
        _store.add(location_node, RDF.type, _store.fs.Location)
        _store.add(location_node, _store.fs.address, Literal(self.address))
        _store.add(location_node, _store.fs.crossStreet, Literal(self.crossStreet))
        _store.add(location_node, _store.fs.lat, Literal(self.lat))
        _store.add(location_node, _store.fs.lng, Literal(self.lng))
        _store.add(location_node, _store.fs.postalCode, Literal(self.postalCode))
        _store.add(location_node, _store.fs.cc, Literal(self.cc))
        _store.add(location_node, _store.fs.city, Literal(self.city))
        _store.add(location_node, _store.fs.state, Literal(self.state))
        _store.add(location_node, _store.fs.country, Literal(self.country))
        _store.add(location_node, _store.fs.formattedAdress, Literal(self.formattedAddress))
        return location_node


class Venue():
    def __init__(self, json_data):
        self.id = json_data['id']
        self.name = json_data['name']
        self.canonicalUrl = json_data['canonicalUrl']
        self.url = json_data['url']
        self.rating = json_data['rating']
        self.description = json_data['description']
        self.tags = json_data['tags']
        self.shortUrl = json_data['shortUrl']
        self.timeZone = json_data['timeZone']
        self.verified = json_data['verified']
        self.createdAt = json_data['createdAt']

        contact = json_data['contact']
        self.contact_phone = contact['phone']
        self.contact_formattedPhone = contact['formattedPhone']
        self.contact_twitter = contact['twitter']

        self.location = Location(json_data['location'])

        # ignoring stats
        # ignoring likes
        # ignoring dislike
        # ignoring ok
        # ignoring ratingColor
        # ignoring ratingSignals
        # ignoring specials
        # ignoring photos
        # ignoring hereNow
        # ignoring reasons
        # ignoring tips
        # ignoring phrases
        # ignoring popular
        # ignoring pageUpdates
        # ignoring inbox
        # ignoring attributes
        # ignoring bestPhoto

        self.events = []
        try:
            for event in json_data['events']['items']:
                self.events.append(Event(event))
        except KeyError:
            # there are no events today
            pass

    @staticmethod
    def save_class_definitions(_store):
        _store.add(_store.fs.Venue, RDF.type, OWL.Class)
        Location.save_class_definitions(_store)
        Event.save_class_definitions(_store)
        # _store.add(_store.fs.location, RDF.type, OWL.FunctionalProperty)
        # _store.add(_store.fs.location, RDF.type, OWL.InverseFunctionalProperty)

    def save_in_triple_store(self, _store):
        venue = _store.fs[self.id]
        _store.add(venue, RDF.type, _store.fs.Venue)
        _store.add(venue, _store.fs.name, Literal(self.name))
        _store.add(venue, _store.fs.canonicalUrl, URIRef(self.canonicalUrl))
        _store.add(venue, _store.fs.url, URIRef(self.url))
        _store.add(venue, _store.fs.rating, Literal(self.rating))
        _store.add(venue, _store.fs.description, Literal(self.description))
        _store.add(venue, _store.fs.shortUrl, URIRef(self.shortUrl))
        _store.add(venue, _store.fs.timeZone, Literal(self.timeZone))
        _store.add(venue, _store.fs.verified, Literal(self.verified))
        _store.add(venue, _store.fs.createdAt, Literal(self.createdAt))

        # contact
        _store.add(venue, _store.fs.contact_phone, Literal(self.contact_phone))
        _store.add(venue, _store.fs.contact_formattedPhone, Literal(self.contact_formattedPhone))
        _store.add(venue, _store.fs.contact_twitter, Literal(self.contact_twitter))

        # location
        location_node = self.location.save_in_triple_store(_store)
        _store.set(venue, _store.fs.location, location_node)

        for tag in self.tags:
            _store.add(venue, _store.fs.tag, Literal(tag))

        for event in self.events:
            event_URI = event.save_in_triple_store(_store)
            _store.add(venue, _store.fs.event, event_URI)

        return venue


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
        self.graph.parse(self.filename, format=self.file_type)
        self.graph.bind("owl", OWL)
        self.fs = Namespace("https://api.foursquare.com/v2/venues/")
        self.graph.bind("fs", self.fs)
        self.fsevent = Namespace("https://api.foursquare.com/v2/events/")
        self.graph.bind("fsevent", self.fsevent)
        self.dcterms = Namespace("http://purl.org/dc/terms/")
        self.graph.bind("dcterms", self.dcterms)

        self._create_classes()

    def _create_classes(self):
        Venue.save_class_definitions(self)

    def save(self):
        self.graph.serialize(self.filename, format=self.file_type)

    def add(self, s, p, o):
        self.graph.add((s, p, o))

    def set(self, s, p, o):
        self.graph.set((s, p, o))

    def remove(self, s, p, o):
        self.graph.remove((s, p, o))


if __name__ == '__main__':
    __init__()
    response = download_data()
    # response = load_file_data("/home/matteo/Documenti/VU/Intelligent Web Applications/foursquare.json")
    logging.info("data: {}".format(response['meta']))
    melkweg = Venue(response['response']['venue'])
    logging.info("venue: {}".format(dump_to_json(melkweg)))
    store = FoursquareTripleStore()
    melkweg.save_in_triple_store(store)
    store.save()
