from django.shortcuts import render, get_object_or_404
from .models import Movie

def index(request):
    """
    Display a list of movies. If a search query is provided, filter by name.
    """
    search_term = request.GET.get('search', '')
    movies = Movie.objects.filter(name__icontains=search_term) if search_term else Movie.objects.all()

    template_data = {
        'title': 'Movies',
        'movies': movies,
    }
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    """
    Display details of a specific movie.
    """
    movie = get_object_or_404(Movie, id=id)

    template_data = {
        'title': movie.name,
        'movie': movie,
    }
    return render(request, 'movies/show.html', {'template_data': template_data})
