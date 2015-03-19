import json
import logging
import requests

__author__ = 'matteo'

#URL = "http://nominatim.openstreetmap.org/reverse?format=json&lat=52.36482245667135&lon=4.88149333504718"
URL = "http://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}"


def get_address(lat, long):
    logging.info("donwloading address for {}, {}".format(lat, long))
    r = requests.get(URL.format(lat, long))
    #print(r.text)

    address_json = json.loads(r.text)['address']

    try:
        road = address_json['road']
        house_number = address_json['house_number']
        address = "{} {}".format(road, house_number)
        return address
    except KeyError:
        return None
