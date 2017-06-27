from django.shortcuts import render

from .models import Person


def home(request):
    p = Person.objects.first()
    return render(request, 'home.html', {'p': p})
