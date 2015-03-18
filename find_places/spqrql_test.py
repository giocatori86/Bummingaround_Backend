__author__ = 'Sander'

import sys

import rdflib

from find_places import spqrql
lon = 52.3647435
lat = 4.8812636000
radius = 100 #meters

def make_request():

    sparql = spqrql.create_query(lon,lat,radius)
    results = sparql.query()

    raw_response = results.response.readall().decode('utf-8')
    return raw_response

xmlstring = make_request()

g = rdflib.Graph()

sys.stdout.flush()
sys.stderr.flush()
print(xmlstring)

sys.stdout.flush()
sys.stderr.flush()
g.parse(data=xmlstring, format='turtle')
g.serialize("output.rdf", format="turtle")

