from django.shortcuts import render
from django.utils import simplejson
from django.http import HttpResponse
from .models import Person


class JsonResponse(HttpResponse):
    """
        JSON response
    """
    def __init__(
            self, content, mimetype='application/json',
            status=None, content_type='application/json'):
        super(JsonResponse, self).__init__(
            content=simplejson.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type,
        )


def help(request):
    requests = [
                    {"text": "/", "id": 1},
                    {"text": "/requests/", "id": 2},
                    {"text": "/requests/", "id": 3}
                ]
    return JsonResponse(map(
        lambda r: {
            'text': r["text"],
            'id': r["id"],
        },
        requests
    ))


def requests(request):
    return render(request, 'requests.html', {})


def home(request):
    p = Person.objects.first()
    return render(request, 'home.html', {'p': p})
