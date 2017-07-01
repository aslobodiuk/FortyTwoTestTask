from json import dumps
from django.shortcuts import render
from django.utils import simplejson
from django.http import HttpResponse
from .models import Person, Request


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
    requests = Request.objects.filter().reverse()[0:10]
    return JsonResponse(map(
        lambda r: {
            'text': r.link,
            'id': r.id,
        },
        requests
    ))


def requests(request):
    return render(request, 'requests.html', {})


def home(request):
    p = Person.objects.first()
    return render(request, 'home.html', {'p': p})


def edit(request):
    if request.method == 'POST':
        return HttpResponse(dumps({'result': 'success'}))
    return render(request, 'edit.html', {})
