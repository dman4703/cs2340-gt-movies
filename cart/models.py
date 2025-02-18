from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.core.validators import MinValueValidator

# class Order(models.Model):
#     id = models.AutoField(primary_key=True)
#     total = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.id) + ' - ' + self.user.username
#
# class Item(models.Model):
#     id = models.AutoField(primary_key=True)
#     price = models.IntegerField()
#     quantity = models.IntegerField()
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     def __str__(self):
#         return str(self.id) + ' - ' + self.movie.name

class Order(models.Model):
    """
    Represents a user's order (1:N from User).
    """
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    # Index user and order_date for quicker filtering/sorting
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        db_index=True
    )
    date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    # @property
    # def total_amount(self):
    #     """
    #     Dynamically compute the sum of (price_at_purchase * quantity)
    #     across all OrderItems belonging to this order.
    #     """
    #     return sum(
    #         item.price_at_purchase * item.quantity
    #         for item in self.items.all()
    #     )


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.movie.name} (Order: {self.order.id})"
