import math

__author__ = 'Sander'

BASE_QUERY = """"
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
  #?sub geo:lat "52.3647435"^^xsd:double .
  ?sub rdf:type lgdo:Amenity ;
    rdfs:label ?label ;
    geo:lat ?lat;
    geo:long ?lon.
  FILTER( ({2}-xsd:float(?lat))*({2}-xsd:float(?lat)) + ({3}-xsd:float(?lon))*({3}-xsd:float(?lon))*({0}-({1}*xsd:float(?lat))) < 0.808779738472242 ) .
}} LIMIT 10
"""""


def create_query(lat, long, radius):
    numerator, denumerator = calculate_parameters(radius)
    query = BASE_QUERY.format(denumerator, numerator,lat,long)
    return query


def calculate_parameters(radius):
    numerator = math.cos(radius) *(math.cos(radius)-math.sin(radius)*(math.pi/180)*(radius-(2*radius)))
    denumerator = math.cos(radius)*math.cos(radius)*(math.pi/180)

    return numerator, denumerator





