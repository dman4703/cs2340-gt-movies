from django.shortcuts import render
from movies.models import Movie
from django.db.models import Q


def index(request):
    # Select 3 random movies that have either an uploaded image or an image URL.
    featured_movies = Movie.objects.filter(
        Q(image__isnull=False) | Q(image_url__isnull=False)
    ).order_by('?')[:3]

    template_data = {
        'title': 'Movies Store',
        'featured_movies': featured_movies,
    }
    return render(request, 'home/index.html', {'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})