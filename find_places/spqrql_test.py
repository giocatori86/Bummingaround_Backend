from find_places.graphdb import GraphDB, GRAPHDB_LINKEDGEODATA_URL

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
g.serialize("output.rdf", format="turtle")

db = GraphDB()
db.add_turtle(query_result.get_string())
