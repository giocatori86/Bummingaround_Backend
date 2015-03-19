from rdflib import RDF, Literal
from find_places.graphdb import GraphDB, GRAPHDB_LINKEDGEODATA_URL, define_namespaces, NAMESPACES

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

lgdo = NAMESPACES['lgdo']

for venue in g.subjects(RDF.type, lgdo.Amenity):
    street = g.value(venue, lgdo['addr%3Astreet'])
    house_number = g.value(venue, lgdo['addr%3Ahousenumber'])
    if (street is not None) and (house_number is not None):
        address = "{} {}".format(street, house_number)
        g.add((venue, NAMESPACES['iwa'].address, Literal(address)))

ttl = g.serialize("output.rdf", format="turtle")
ttl = g.serialize(format="turtle")

db = GraphDB()
db.add_turtle(ttl)
