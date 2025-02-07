from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from movies.models import Movie, Review
from cart.models import Order, Item
class ShoppingCart(models.Model):
    """
    A 1:1 relationship with User, representing a user's cart.
    """
    # Index for faster lookups (e.g., get a cart by user quickly)
    id = models.AutoField(primary_key=True)
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
    id = models.AutoField(primary_key=True)
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
        return f"{self.quantity} of {self.movie.name}"


