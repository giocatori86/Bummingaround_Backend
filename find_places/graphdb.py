import requests

__author__ = 'matteo'

GRAPHDB_URL = "http://covolunablu.org:27019/openrdf-workbench/repositories/bummingaround/add"


class GraphDB:
    def __init__(self):
        pass

    def query(self, query):
        # TODO do stuff
        pass

    def add_turtle(self, turtle_string):
        files = {
            'Content-Type': "text/turtle",
            'source': 'contents',
            'content': turtle_string
        }
        r = requests.post(GRAPHDB_URL, files=files)
        print(r.text)