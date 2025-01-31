from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    """
    Represents a movie in the store.
    """
    GENRE_CHOICES = [
        ('ACTION', 'Action'),
        ('COMEDY', 'Comedy'),
        ('DRAMA', 'Drama'),
        ('HORROR', 'Horror'),
        ('SCIFI', 'Sci-Fi'),
        ('ROMANCE', 'Romance'),
        # Add more as needed
    ]

    # Index title for faster lookups
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    release_date = models.DateField()
    # Using choices for genre
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    image_url = models.URLField(blank=True, null=True)
    # Constrain stock_quantity to be non-negative
    stock_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Represents a user's review for a particular movie.
    """
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
    review_text = models.TextField()
    # Rating constrained between 1 and 5
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.movie.title}"


class ShoppingCart(models.Model):
    """
    A 1:1 relationship with User, representing a user's cart.
    """
    # Index for faster lookups (e.g., get a cart by user quickly)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        db_index=True
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    """
    Items within a shopping cart (1:N from ShoppingCart).
    """
    # related_name='cart_items' allows cart.cart_items.all()
    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # Must be at least 1
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f"{self.quantity} of {self.movie.title}"


class Order(models.Model):
    """
    Represents a user's order (1:N from User).
    """
    # Payment status choices
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('CANCELED', 'Canceled'),
    ]

    # Index user and order_date for quicker filtering/sorting
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        db_index=True
    )
    order_date = models.DateTimeField(auto_now_add=True, db_index=True)
    shipping_address = models.TextField()
    payment_status = models.CharField(
        max_length=9,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    @property
    def total_amount(self):
        """
        Dynamically compute the sum of (price_at_purchase * quantity)
        across all OrderItems belonging to this order.
        """
        return sum(
            item.price_at_purchase * item.quantity
            for item in self.items.all()
        )


class OrderItem(models.Model):
    """
    Items in a user's order (1:N from Order).
    """
    # related_name='items' so you can do: order.items.all()
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    # Price at the time of purchase
    price_at_purchase = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.movie.title} (Order: {self.order.id})"

