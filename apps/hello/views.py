from json import dumps
from django.shortcuts import render
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Person, Request
from .forms import ContactForm


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


@login_required()
def edit(request):
    last = Person.objects.filter().reverse()[0]
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=last)
        if form.is_valid():
            form.save()
            p = '%s' % last.photo
            p_url = '%s' % last.photo.url
            return HttpResponse(
                dumps({'picture': p, 'pict_url': p_url, 'result': 'success'})
            )
        else:
            response = {}
            for k in form.errors:
                response[k] = form.errors[k][0]
            return HttpResponse(dumps({
                'response': response,
                'result': 'error'
            }))
    else:
        form = ContactForm(instance=last)
    return render(request, 'edit.html', {'form': form})
