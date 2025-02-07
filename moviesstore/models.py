from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from movies.models import Movie, Review

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
        return f"Cart of {self.user}"


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


class Order(models.Model):
    """
    Represents a user's order (1:N from User).
    """
    # Payment status choices
    id = models.AutoField(primary_key=True)
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
        return f"Order #{self.id} by {self.user}"

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
    id = models.AutoField(primary_key=True)
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
        return f"{self.quantity} of {self.movie.name} (Order: {self.order.id})"

