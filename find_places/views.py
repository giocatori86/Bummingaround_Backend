import json
from django.http import HttpResponse

from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from find_places.foursquare.download_foursquare_data import download_per_point_fs
from find_places.linkedgeodata import download_per_point_lgd
from find_places.models import Point, load_venues_from_triple_json
from find_places.spqrql import query_db_position

DEFAULT_RADIUS = 1000


def get_venues_from_pos(lat, long, radius):
    result = query_db_position(lat, long, radius)
    venues = load_venues_from_triple_json(result)
    return venues

@csrf_exempt
def search_stores(request):
    if request.method != 'POST':
        response = HttpResponse('error: only post supported')
        response.status_code = 400
        return response

    try:
        request_json = json.loads(request.body.decode("utf-8"))
        path = request_json['path']

        points = []
        for point in path:
            points.append(Point(point['lat'], point['lon']))

    except (KeyError, MultiValueDictKeyError) as e:
        response = HttpResponse('{"error": ' + str(e) + ' }')
        response.status_code = 400
        return response

    venues = {}
    for point in points:
        venues_per_point = get_venues_from_pos(point.lat, point.lon, DEFAULT_RADIUS)

        # if less than 5 venues are found, search on external sources ...
        if len(venues_per_point) < 5:
            download_per_point_lgd(point.lat, point.lon, DEFAULT_RADIUS)  # LGD
            download_per_point_fs(point.lat, point.lon, DEFAULT_RADIUS)  # FS
            # ... and recall the query
            venues_per_point = get_venues_from_pos(point.lat, point.lon, DEFAULT_RADIUS)

        for venue in venues_per_point:
            venues[venue.id] = venue.serialize()

    response = HttpResponse(json.dumps(venues))
    return response
