from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from projects.models import Movie
from django.template import loader


def index(request):
    return HttpResponse("Hello, world. You're at the projects index for ssdi_6112.")


def movies(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'projects/movies.html', context)
