import logging
from SPARQLWrapper import TURTLE, SPARQLWrapper
import rdflib
import requests

__author__ = 'matteo'

GRAPHDB_BASE_URL = "http://covolunablu.org:27019/openrdf-workbench/repositories/bummingaround/add"
GRAPHDB_LINKEDGEODATA_URL = "http://linkedgeodata.org/sparql/"


class QueryResult:
    def __init__(self, result):
        self.result = result
        self.string = result.response.readall().decode('utf-8')

    def __str__(self):
        return self.string

    def get_string(self):
        return self.string

    def get_graph(self):
        g = rdflib.Graph()
        g.parse(data=self.string, format='turtle')
        return g


class GraphDB:
    def __init__(self, url=None):
        if url is None:
            self.url = GRAPHDB_BASE_URL
        else:
            self.url = url
        pass

    def query(self, query):
        logging.info("starting query to {}".format(self.url))
        logging.info("query:\n{}".format(query))
        sparql = SPARQLWrapper(self.url)
        sparql.setQuery(query)
        sparql.setReturnFormat(TURTLE)
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