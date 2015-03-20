import json
import logging
import traceback
from django.http import HttpResponse

from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from find_places.foursquare.download_foursquare_data import download_per_point_fs
from find_places.linkedgeodata import download_per_point_lgd
from find_places.models import Point, load_venues_from_triple_json
from find_places.spqrql import query_db_position

DEFAULT_RADIUS = 100


def get_venues_from_pos(lat, long, radius):
    result = query_db_position(lat, long, radius)
    _venues = load_venues_from_triple_json(result)
    return _venues


def search_stores(__points):
    __venues = {}
    for __point in __points:
        venues_per_point = get_venues_from_pos(__point.lat, __point.lon, DEFAULT_RADIUS)

        # if less than 5 venues are found, search on external sources ...
        if len(venues_per_point) < 5:
            download_per_point_fs(__point.lat, __point.lon, DEFAULT_RADIUS)  # FS
            download_per_point_lgd(__point.lat, __point.lon, DEFAULT_RADIUS)  # LGD
            # ... and recall the query
            venues_per_point = get_venues_from_pos(__point.lat, __point.lon, DEFAULT_RADIUS)

        for venue in venues_per_point:
            __venues[venue.id] = venue.serialize()

    return __venues


@csrf_exempt
def search_stores_view(request):
    if request.method != 'POST':
        response = HttpResponse('error: only post supported')
        response.status_code = 400
        return response

    try:
        request_json = json.loads(request.body.decode("utf-8"))
        _path = request_json['path']

        _points = []
        for _point in _path:
            _points.append(Point(_point['lat'], _point['lon']))

    except (Exception, KeyError, MultiValueDictKeyError) as e:
        logging.warning("error: {}".format(e))
        logging.warning(traceback.format_exc())
        response = HttpResponse(json.dumps({"error": str(e)}))
        response.status_code = 400
        return response


    _venues = search_stores(_points)
    logging.info("found {} venues after too much work".format(len(_venues)))

    response = HttpResponse(json.dumps(_venues))
    return response


if __name__ is "__main__":
    venues = search_stores([Point(52.36482245667135, 4.88149333504718)])
    print(json.dumps(venues))