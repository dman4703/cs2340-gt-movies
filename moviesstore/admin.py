from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Movie, Review, ShoppingCart, CartItem, Order, OrderItem


# Inlines for the User model

# Inline display of Reviews associated with a User
# This allows admins to see up to 5 recent reviews directly on the User admin page
class UserReviewInline(admin.TabularInline):
    model = Review
    extra = 0  # Do not display extra empty forms for new reviews
    ordering = ['-created_date']  # Order reviews by most recent first
    max_num = 5  # Display a maximum of 5 reviews
    # Display read-only fields: a clickable movie link, rating, created date, and review text
    readonly_fields = ['movie_link', 'rating', 'created_date', 'review_text']

    def movie_link(self, obj):
        """
        Returns a clickable link to the Movie's admin change page.
        """
        url = reverse("admin:moviesstore_movie_change", args=[obj.movie.pk])
        return mark_safe(f'<a href="{url}">{obj.movie.title}</a>')
    movie_link.short_description = 'Movie'


# Inline display of Orders associated with a User.
# This allows you to view up to 5 recent orders directly on the User admin page
class UserOrderInline(admin.TabularInline):
    model = Order
    extra = 0  # Do not display extra empty forms for new orders
    ordering = ['-order_date']  # Order orders by most recent first
    max_num = 5  # Display a maximum of 5 orders
    # Display read-only fields: order date, payment status, and total amount
    readonly_fields = ['order_date', 'payment_status', 'total_amount']


# Custom UserAdmin to include inlines for reviews and orders
class CustomUserAdmin(UserAdmin):
    inlines = [UserOrderInline, UserReviewInline]
    search_fields = ('username', 'email')  # Enable search by username and email


# Unregister the default User admin and register the customized one.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Movie Admin Configuration

class MovieAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'price', 'release_date', 'stock_quantity')
    # Enable searching by title or genre
    search_fields = ('title', 'genre')
    # Add filters for genre and release date in the sidebar
    list_filter = ('genre', 'release_date')
    ordering = ('title',)  # Order movies alphabetically by title
    readonly_fields = ('release_date',)  # Prevent editing the release date in admin

# Review Admin with Star Ratings and Clickable Links

class ReviewAdmin(admin.ModelAdmin):
    # Display these columns in the review list view
    list_display = ('user_link', 'movie_link', 'star_rating', 'created_date')
    # Enable search by movie title or username
    search_fields = ('movie__title', 'user__username')
    # Add filters for rating and created date
    list_filter = ('rating', 'created_date')
    # Optimize query performance by pre-fetching related user and movie objects
    list_select_related = ('user', 'movie')
    # Use AJAX-powered autocomplete fields for foreign key selections
    autocomplete_fields = ['user', 'movie']

    def user_link(self, obj):
        """
        Returns a clickable link to the User's admin change page.
        """
        url = reverse("admin:auth_user_change", args=[obj.user.pk])
        return mark_safe(f'<a href="{url}">{obj.user.username}</a>')
    user_link.short_description = 'User'

    def movie_link(self, obj):
        """
        Returns a clickable link to the Movie's admin change page.
        """
        url = reverse("admin:moviesstore_movie_change", args=[obj.movie.pk])
        return mark_safe(f'<a href="{url}">{obj.movie.title}</a>')
    movie_link.short_description = 'Movie'

    def star_rating(self, obj):
        """
        Render the review rating as star icons using Unicode characters.
        Filled stars (gold) represent the rating value and empty stars (light gray)
        fill up to 5 stars.
        """
        full_star = '<span style="color: gold;">&#9733;</span>'      # Gold filled star.
        empty_star = '<span style="color: lightgray;">&#9734;</span>'  # Light gray empty star.
        stars = full_star * obj.rating + empty_star * (5 - obj.rating)
        return mark_safe(stars)
    star_rating.short_description = 'Rating'

# Order & OrderItem Admin with Autocomplete

# Inline for OrderItem within an Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Provide one extra blank form for new order items
    # Enable autocomplete for the movie selection
    autocomplete_fields = ['movie']

class OrderAdmin(admin.ModelAdmin):
    # Fields to display in the order list view
    list_display = ('user_link', 'order_date', 'payment_status', 'total_amount')
    # Enable search by username and order date
    search_fields = ('user__username', 'order_date')
    # Add filters for payment status and order date
    list_filter = ('payment_status', 'order_date')
    inlines = [OrderItemInline]  # Include inline editing for order items
    # Enable autocomplete for the user field
    autocomplete_fields = ['user']
    # Optimize query performance by pre-fetching the related user
    list_select_related = ('user',)

    def user_link(self, obj):
        """
        Returns a clickable link to the User's admin change page.
        """
        url = reverse("admin:auth_user_change", args=[obj.user.pk])
        return mark_safe(f'<a href="{url}">{obj.user.username}</a>')
    user_link.short_description = 'User'

# ShoppingCart & CartItem Admin with Autocomplete

# Inline for CartItem within a ShoppingCart
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Provide one extra blank form for new cart items
    # Enable autocomplete for the movie field
    autocomplete_fields = ['movie']

class ShoppingCartAdmin(admin.ModelAdmin):
    # Fields to display in the shopping cart list view
    list_display = ('user_link', 'created_date')
    # Enable search by the username associated with the shopping cart
    search_fields = ('user__username',)
    inlines = [CartItemInline]  # Include inline editing for cart items
    # Enable autocomplete for the user field
    autocomplete_fields = ['user']
    # Optimize query performance by pre-fetching the related user
    list_select_related = ('user',)

    def user_link(self, obj):
        """
        Returns a clickable link to the User's admin change page.
        """
        url = reverse("admin:auth_user_change", args=[obj.user.pk])
        return mark_safe(f'<a href="{url}">{obj.user.username}</a>')
    user_link.short_description = 'User'

# OrderItem Admin (Managed Separately)

class OrderItemAdmin(admin.ModelAdmin):
    # Fields to display in the order item list view
    list_display = ('order', 'movie_link', 'quantity', 'price_at_purchase')
    # Enable autocomplete for both movie and order fields
    autocomplete_fields = ['movie', 'order']
    # Optimize query performance by pre-fetching related movie and order objects
    list_select_related = ('movie', 'order')

    def movie_link(self, obj):
        """
        Returns a clickable link to the Movie's admin change page.
        """
        url = reverse("admin:moviesstore_movie_change", args=[obj.movie.pk])
        return mark_safe(f'<a href="{url}">{obj.movie.title}</a>')
    movie_link.short_description = 'Movie'

# Register Models with the Admin Site

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(CartItem)  # Register CartItem separately if desired.
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

# Customize the Admin Site Appearance

# The header displayed at the top of the admin site
admin.site.site_header = "GT Movies Store Admin"
# The title of the admin site
admin.site.site_title = "GT Movies Management"
# The index title on the main admin page
admin.site.index_title = "Welcome to the GT Movies Store Admin Panel"
