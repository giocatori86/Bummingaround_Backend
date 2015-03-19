import logging
from SPARQLWrapper import TURTLE, SPARQLWrapper
import rdflib
from rdflib import Namespace
import requests

__author__ = 'matteo'

GRAPHDB_BASE_URL = "http://covolunablu.org:27019/openrdf-workbench/repositories/bummingaround/add"
GRAPHDB_LINKEDGEODATA_URL = "http://linkedgeodata.org/sparql/"

NAMESPACES = {
    "dcterms": Namespace("http://purl.org/dc/terms/"),
    "spatial": Namespace("http://jena.apache.org/spatial#"),
    "geo": Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#"),
    "geom": Namespace("http://geovocab.org/geometry#"),
    "gn": Namespace("http://www.geonames.org/ontology#"),
    "lgdo": Namespace("http://linkedgeodata.org/ontology/"),
    "lgd": Namespace("http://linkedgeodata.org/triplify/"),
    "lgd-geom": Namespace("http://linkedgeodata.org/geometry/"),
}


def define_namespaces(graph):
    for prefix in NAMESPACES:
        graph.bind(prefix, NAMESPACES[prefix])


class QueryResult:
    def __init__(self, result):
        self.result = result
        self.string = result.response.readall().decode('utf-8')

    def __str__(self):
        return self.string

    def convert(self):
        return self.result.convert()

    def get_string(self):
        return self.string

    def get_graph(self):
        g = rdflib.Graph()
        define_namespaces(g)
        g.parse(data=self.string, format='turtle')
        return g


class GraphDB:
    def __init__(self, url=None):
        if url is None:
            self.url = GRAPHDB_BASE_URL
        else:
            self.url = url
        pass

    def query(self, query, response_type=TURTLE):
        logging.info("starting query to {}".format(self.url))
        logging.info("query:\n{}".format(query))
        sparql = SPARQLWrapper(self.url)
        sparql.setQuery(query)
        sparql.setReturnFormat(response_type)
        result = sparql.query()
        logging.info("query finished")
        return QueryResult(result)

    def add_turtle(self, turtle_string):
        files = {
            'Content-Type': "text/turtle",
            'source': 'contents',
            'content': turtle_string
        }
        r = requests.post(self.url, files=files)
        if r.status_code >= 400:
            raise Exception("ERROR uploading data!\n"
                            "Response: {}\n"
                            "Response body:\n{}".format(r, r.text))

        return r
