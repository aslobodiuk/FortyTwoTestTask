from django.shortcuts import render, get_object_or_404
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
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
    requests = Request.objects.exclude(
            link__startswith="/static/"
        ).order_by("-priority", "-time")[:10]
    return JsonResponse(list(requests.values('link', 'id')))


def requests(request):
    return render(request, 'requests.html', {})


@login_required()
def priority(request):

    RequestFormSet = modelformset_factory(
        Request,
        fields=('priority',),
        extra=0
        )
    if request.method == 'POST':
        formset = RequestFormSet(request.POST)
        if formset.is_valid():
            formset.save()
    else:
        formset = RequestFormSet(
            queryset=Request.objects.order_by("-link_type", "-time")
        )
    return render(request, "priority.html", {"formset": formset})


def home(request):
    p = get_object_or_404(Person, pk=1)
    return render(request, 'home.html', {'p': p})


@login_required()
def edit(request):
    last = Person.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=last)
        if form.is_valid():
            form.save()
            p = '%s' % last.photo
            p_url = '%s' % last.photo.url
            return JsonResponse(
                {'picture': p, 'pict_url': p_url, 'result': 'success'}
            )
        else:
            return JsonResponse(
                {'response': form.errors, 'result': 'error'}
            )
    else:
        form = ContactForm(instance=last)
    return render(request, 'edit.html', {'form': form})
