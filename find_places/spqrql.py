import math

from SPARQLWrapper import SPARQLWrapper, TURTLE


__author__ = 'Sander'

BASE_QUERY = """
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
  FILTER( ({2}-xsd:float(?lat))*({2}-xsd:float(?lat)) + ({3}-xsd:float(?lon))*({3}-xsd:float(?lon))*({0}-({1}*xsd:float(?lat))) < {4:f} ) .
}} LIMIT 100
"""

BRGRAD = 111194.9
REF_LAT = 51.0

def create_query(lat, long, radius):
    numerator, denumerator, threshold = calculate_parameters(REF_LAT, lat, radius)
    query = BASE_QUERY.format(numerator, denumerator, lat, long, threshold)
    print(query)
    sparql = SPARQLWrapper("http://linkedgeodata.org/sparql/")
    sparql.setQuery(query)
    sparql.setReturnFormat(TURTLE)
    return sparql


def calculate_parameters(ref_lat, lat, radius):
    cos = math.cos(ref_lat)
    sin = math.sin(ref_lat)
    denumerator = cos * sin * (math.pi/180.0)
    numerator = cos * (cos - sin * (math.pi/180.0) * (lat - (2*ref_lat)))
    threshold = (radius/BRGRAD) * (radius/BRGRAD)

    return numerator, denumerator, threshold


def get_query(lat,lon,radius):
    create_query(lat,lon,radius)







