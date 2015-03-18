import json
from django.http import HttpResponse

from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from find_places.models import Point

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


    response = HttpResponse(json.dumps(points))
    return response
