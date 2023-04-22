from django.http import HttpResponse
from django.shortcuts import render


def playground_home(request):
    return render(request, 'playground/home.html', {'title': 'Home'})


def playground_about(request):
    return render(request, 'playground/about.html', {'title': 'About'})