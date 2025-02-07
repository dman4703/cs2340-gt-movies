from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# class Movie(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     price = models.IntegerField()
#     description = models.TextField()
#     image = models.ImageField(upload_to='movie_images/')
#     def __str__(self):
#         return str(self.id) + ' - ' + self.name
#
# from django.db import models
# from django.contrib.auth.models import User
#
# class Review(models.Model):
#     id = models.AutoField(primary_key=True)
#     comment = models.CharField(max_length=255)
#     date = models.DateTimeField(auto_now_add=True)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.id) + ' - ' + self.movie.name

class Movie(models.Model):
    """
    Represents a movie in the store.
    """
    id = models.AutoField(primary_key=True)
    GENRE_CHOICES = [
        ('ACTION', 'Action'),
        ('COMEDY', 'Comedy'),
        ('DRAMA', 'Drama'),
        ('HORROR', 'Horror'),
        ('SCIFI', 'Sci-Fi'),
        ('ROMANCE', 'Romance'),
    ]

    name = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES,
        default='DRAMA')

    image = models.ImageField(upload_to='movie_images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def clean(self):
        """Ensure that either `image` or `image_url` is set, but not both."""
        if self.image and self.image_url:
            raise ValidationError("You can only set either an image or an image URL, not both.")
        if not self.image and not self.image_url:
            raise ValidationError("You must provide either an image or an image URL.")

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Represents a user's review for a particular movie.
    """
    id = models.AutoField(primary_key=True)
    # Related name 'reviews' allows: user.reviews.all() and movie.reviews.all()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    comment = models.CharField(max_length=255)
    # Rating constrained between 1 and 5
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.movie.name}"