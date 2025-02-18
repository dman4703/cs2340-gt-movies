from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Review
from django.contrib.auth.decorators import login_required

def index(request):
    """
    Display a list of movies.
    Optionally filter by 'search' and 'genre' GET parameters.
    """
    search_term = request.GET.get('search', '')
    genre_filter = request.GET.get('genre', '')

    # Start with all movies
    movies = Movie.objects.all()

    # Filter by search term if provided
    if search_term:
        movies = movies.filter(name__icontains=search_term)

    # Filter by genre if provided (and not blank)
    if genre_filter:
        movies = movies.filter(genre=genre_filter)

    # Pass available genre choices to the template
    template_data = {
        'title': 'Movies',
        'movies': movies,
        'genres': Movie.GENRE_CHOICES,  # e.g. [('ACTION','Action'), ('COMEDY','Comedy'), ...]
        'selected_genre': genre_filter, # to mark the dropdown as "selected"
        'search_term': search_term,     # so we can preserve search text
    }
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    """
    Display details of a specific movie.
    """
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {'title': movie.name, 'movie': movie, 'reviews': reviews}
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if (request.method == 'POST'
            and (request.POST['comment'] != '')
            and (int(request.POST['rating']) > 0)
            and (int(request.POST['rating']) < 6)):
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.rating = int(request.POST['rating'])
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {'title': 'Edit Review', 'review': review}
        return render(request, 'movies/edit_review.html',{'template_data': template_data})
    elif (request.method == 'POST'
          and (request.POST['comment'] != '')
            and (int(request.POST['rating']) > 0)
            and (int(request.POST['rating']) < 6)):
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.rating = int(request.POST['rating'])
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

