import json
import math

from SPARQLWrapper import SPARQLWrapper, TURTLE, JSON
from find_places.graphdb import GraphDB


__author__ = 'Sander'

# take a look at this
# http://www.slideshare.net/langec/linked-open-geodata-and-the-distributed-ontology-language-a-perfect-match
POSITION_QUERY = """
PREFIX spatial:<http://jena.apache.org/spatial#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX gn:<http://www.geonames.org/ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xds: <http://www.w3.org/2001/XMLSchema#>
PREFIX lgdo: <http://linkedgeodata.org/ontology/>
PREFIX lgd-meta: <http://linkedgeodata.org/meta/>
PREFIX iwa: <https://www.example.com/iwa/>

SELECT DISTINCT ?id (SAMPLE(?_label) AS ?label) (SAMPLE(?_lat) as ?lat) (SAMPLE(?_lon) as ?lon)
WHERE {{
 ?id a lgd-meta:Node ;
    rdfs:label ?_label ;
    iwa:lat ?_lat;
    iwa:lng ?_lon.
  FILTER( ({2}-xsd:float(?_lat))*({2}-xsd:float(?_lat)) + ({3}-xsd:float(?_lon))*({3}-xsd:float(?_lon))*({0}-({1}*xsd:float(?_lat))) < {4} ) .
  FILTER not exists {{
    ?id (owl:sameAs|^owl:sameAs)* ?id_
    filter( str(?id_) < str(?id) )
  }}.
}}
GROUP BY ?id
"""

GEODATA_BASE_QUERY_DESCRIBE = """
PREFIX spatial:<http://jena.apache.org/spatial#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX gn:<http://www.geonames.org/ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xds: <http://www.w3.org/2001/XMLSchema#>
PREFIX lgdo: <http://linkedgeodata.org/ontology/>

DESCRIBE ?sub
WHERE {{
 ?sub rdf:type lgdo:Amenity ;
    rdfs:label ?label ;
    geo:lat ?lat;
    geo:long ?lon.
  FILTER( ({2}-xsd:float(?lat))*({2}-xsd:float(?lat)) + ({3}-xsd:float(?lon))*({3}-xsd:float(?lon))*({0}-({1}*xsd:float(?lat))) < {4} ) .
}}
"""

BRGRAD = 111194.9
REF_LAT = 51.0


def create_geodata_query(lat, long, radius):
    return create_location_query(GEODATA_BASE_QUERY_DESCRIBE, lat, long, radius)


def create_location_query(base_query, lat, long, radius):
    numerator, denumerator, threshold = calculate_parameters(REF_LAT, lat, radius)
    query = base_query.format(numerator, denumerator, lat, long, threshold)
    # sparql = SPARQLWrapper("http://linkedgeodata.org/sparql/")
    # sparql.setQuery(query)
    # sparql.setReturnFormat(TURTLE)
    # return sparql
    return query


def calculate_parameters(ref_lat, lat, radius):
    cos = math.cos(ref_lat)
    sin = math.sin(ref_lat)
    denumerator = cos * sin * (math.pi / 180.0)
    numerator = cos * (cos - sin * (math.pi / 180.0) * (lat - (2 * ref_lat)))
    threshold = (radius / BRGRAD) * (radius / BRGRAD)

    return numerator, denumerator, threshold


graphDB = GraphDB()


def query_db_position(lat, long, radius):
    query = create_location_query(POSITION_QUERY, lat, long, radius)
    response = graphDB.query(query, JSON)
    #print(response.get_string())
    return json.loads(response.get_string())

query_db_position(52.36482245667135, 4.88149333504718, 1000000)