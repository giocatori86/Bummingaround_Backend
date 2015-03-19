from rdflib import RDF, Literal
from find_places.graphdb import GraphDB, GRAPHDB_LINKEDGEODATA_URL, define_namespaces, NAMESPACES
from find_places.reverse_geocoding import get_address

__author__ = 'Sander'

from find_places import spqrql

lon = 52.3647435
lat = 4.8812636000
radius = 100  # meters


def make_request():
    linked_geo_data_db = GraphDB(GRAPHDB_LINKEDGEODATA_URL)
    query = spqrql.create_geodata_query(lon, lat, radius)
    return linked_geo_data_db.query(query)

query_result = make_request()

g = query_result.get_graph()

define_namespaces(g)

LGDO = NAMESPACES['lgdo']
GEO = NAMESPACES['geo']

for venue in g.subjects(RDF.type, LGDO.Amenity):
    street = g.value(venue, LGDO['addr%3Astreet'])
    house_number = g.value(venue, LGDO['addr%3Ahousenumber'])
    if (street is not None) and (house_number is not None):
        address = "{} {}".format(street, house_number)
    else:
        _lat = g.value(venue, GEO.lat)
        _lon = g.value(venue, GEO.long)
        address = get_address(_lat, _lon)

    if address is not None:
        g.add((venue, NAMESPACES['iwa'].address, Literal(address)))

ttl = g.serialize("output.rdf", format="turtle")
ttl = g.serialize(format="turtle")

db = GraphDB()
db.add_turtle(ttl)
