import requests

__author__ = 'matteo'


GRAPHDB_URL = "http://covolunablu.org:27019/openrdf-workbench/repositories/bummingaround/add"
files = {
    'Content-Type': "text/turtle",
    'source': 'contents',
    'content': open('output.rdf', 'rb')
}
r = requests.post(GRAPHDB_URL, files=files)
print(r.text)