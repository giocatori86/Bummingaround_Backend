from rdflib import Literal, URIRef, RDF, OWL
from find_places.reverse_geocoding import get_address

__author__ = 'matteo'


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


class Location():
    def __init__(self, json_data):
        self.lat = json_data['lat']
        self.lng = json_data['lng']
        self.cc = json_data['cc']
        self.country = json_data['country']
        self.formattedAddress = "\n".join(json_data['formattedAddress'])

        try:
            self.address = json_data['address']
        except KeyError:
            self.create_address()

        try:
            self.crossStreet = json_data['crossStreet']
        except KeyError:
            self.crossStreet = None

        try:
            self.postalCode = json_data['postalCode']
        except KeyError:
            self.postalCode = None

        try:
            self.city = json_data['city']
        except KeyError:
            self.city = None
        try:
            self.state = json_data['state']
        except KeyError:
            self.state = None

    @staticmethod
    def save_class_definitions(_store):
        _store.add(_store.fs.Location, RDF.type, OWL.Class)

    def save_in_triple_store(self, _store):
        location_node = _store.fs['location/' + str(self.lat) + ":" + str(self.lng)]
        _store.add(location_node, RDF.type, _store.fs.Location)
        if self.address is not None:
            _store.add(location_node, _store.fs.address, Literal(self.address))
        if self.crossStreet is not None:
            _store.add(location_node, _store.fs.crossStreet, Literal(self.crossStreet))
        _store.add(location_node, _store.fs.lat, Literal(self.lat))
        _store.add(location_node, _store.fs.lng, Literal(self.lng))
        if self.postalCode is not None:
            _store.add(location_node, _store.fs.postalCode, Literal(self.postalCode))
        _store.add(location_node, _store.fs.cc, Literal(self.cc))
        if self.city is not None:
            _store.add(location_node, _store.fs.city, Literal(self.city))
        if self.state is not None:
            _store.add(location_node, _store.fs.state, Literal(self.state))
        _store.add(location_node, _store.fs.country, Literal(self.country))
        _store.add(location_node, _store.fs.formattedAdress, Literal(self.formattedAddress))
        return location_node

    def create_address(self):
        self.address = get_address(self.lat, self.lng)



class Venue():
    def __init__(self, json_data):
        self.id = json_data['id']
        self.name = json_data['name']
        try:
            self.canonicalUrl = json_data['canonicalUrl']
            self.url = json_data['url']
            self.rating = json_data['rating']
            self.description = json_data['description']
            self.tags = json_data['tags']
            self.shortUrl = json_data['shortUrl']
            self.timeZone = json_data['timeZone']
            self.createdAt = json_data['createdAt']
        except KeyError:
            self.canonicalUrl = None
            self.url = None
            self.rating = None
            self.description = None
            self.tags = None
            self.shortUrl = None
            self.timeZone = None
            self.createdAt = None
        self.verified = json_data['verified']

        try:
            contact = json_data['contact']
            self.contact_phone = contact['phone']
            self.contact_formattedPhone = contact['formattedPhone']
            self.contact_twitter = contact['twitter']
        except KeyError:
            self.contact_phone = None
            self.contact_formattedPhone = None
            self.contact_twitter = None

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
        # ignoring events

    @staticmethod
    def save_class_definitions(_store):
        _store.add(_store.fs.Venue, RDF.type, OWL.Class)
        Location.save_class_definitions(_store)
        # _store.add(_store.fs.location, RDF.type, OWL.FunctionalProperty)
        # _store.add(_store.fs.location, RDF.type, OWL.InverseFunctionalProperty)

    def save_in_triple_store(self, _store):
        venue = _store.fs[self.id]
        _store.add(venue, RDF.type, _store.fs.Venue)
        _store.add(venue, _store.fs.name, Literal(self.name))
        if self.canonicalUrl is not None:
            _store.add(venue, _store.fs.canonicalUrl, URIRef(self.canonicalUrl))
        if self.url is not None:
            _store.add(venue, _store.fs.url, URIRef(self.url))
        if self.rating is not None:
            _store.add(venue, _store.fs.rating, Literal(self.rating))
        if self.description is not None:
            _store.add(venue, _store.fs.description, Literal(self.description))
        if self.shortUrl is not None:
            _store.add(venue, _store.fs.shortUrl, URIRef(self.shortUrl))
        if self.timeZone is not None:
            _store.add(venue, _store.fs.timeZone, Literal(self.timeZone))
        if self.createdAt is not None:
            _store.add(venue, _store.fs.createdAt, Literal(self.createdAt))
        _store.add(venue, _store.fs.verified, Literal(self.verified))

        # contact
        if self.contact_phone is not None:
            _store.add(venue, _store.fs.contact_phone, Literal(self.contact_phone))
            _store.add(venue, _store.fs.contact_formattedPhone, Literal(self.contact_formattedPhone))
            _store.add(venue, _store.fs.contact_twitter, Literal(self.contact_twitter))

        # location
        location_node = self.location.save_in_triple_store(_store)
        _store.set(venue, _store.fs.location, location_node)

        if self.tags is not None:
            for tag in self.tags:
                _store.add(venue, _store.fs.tag, Literal(tag))

        return venue
