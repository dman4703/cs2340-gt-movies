from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Review
from django.contrib.auth.decorators import login_required

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
    reviews = Review.objects.filter(movie=movie)

    template_data = {'title': movie.name, 'movie': movie, 'reviews': reviews}
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if (request.method == 'POST'
            and (request.POST['comment'] != '')
            and (request.POST.get('rating') > 0)
            and request.POST.get('rating') < 6):
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
          and (request.POST.get('rating') > 0)
          and request.POST.get('rating') < 6):
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

