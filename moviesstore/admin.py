from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from movies.models import Movie, Review
from cart.models import Order, Item
from .models import ShoppingCart, CartItem


# Movie Admin Configuration
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'genre')
    search_fields = ('name', 'genre')
    list_filter = ('genre',)
    ordering = ('name',)
    readonly_fields = ('image_url',)

admin.site.register(Movie, MovieAdmin)


# Review Admin Configuration
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'movie_link', 'star_rating', 'created_date')
    search_fields = ('movie__name', 'user__username')
    list_filter = ('rating', 'created_date')
    list_select_related = ('user', 'movie')
    autocomplete_fields = ['user', 'movie']

    def user_link(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.user.pk])
        return mark_safe(f'<a href="{url}">{obj.user.username}</a>')
    user_link.short_description = 'User'

    def movie_link(self, obj):
        url = reverse("admin:movies_movie_change", args=[obj.movie.pk])
        return mark_safe(f'<a href="{url}">{obj.movie.name}</a>')
    movie_link.short_description = 'Movie'

    def star_rating(self, obj):
        full_star = '<span style="color: gold;">&#9733;</span>'
        empty_star = '<span style="color: lightgray;">&#9734;</span>'
        return mark_safe(full_star * obj.rating + empty_star * (5 - obj.rating))
    star_rating.short_description = 'Rating'

admin.site.register(Review, ReviewAdmin)


# ShoppingCart & CartItem Admin Configuration
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    autocomplete_fields = ['movie']

class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'created_date')
    search_fields = ('user__username',)
    inlines = [CartItemInline]
    autocomplete_fields = ['user']
    list_select_related = ('user',)

    def user_link(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.user.pk])
        return mark_safe(f'<a href="{url}">{obj.user.username}</a>')
    user_link.short_description = 'User'

admin.site.register(ShoppingCart, ShoppingCartAdmin)


# Order & OrderItem Admin Configuration
class OrderItemInline(admin.TabularInline):
    model = Item
    extra = 1
    autocomplete_fields = ['movie']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_link', 'date', 'total_amount')
    search_fields = ('user__username', 'date')
    list_filter = ('date',)
    inlines = [OrderItemInline]
    autocomplete_fields = ['user']
    list_select_related = ('user',)

    def user_link(self, obj):
        url = reverse("admin:auth_user_change", args=[obj.user.pk])
        return mark_safe(f'<a href="{url}">{obj.user.username}</a>')
    user_link.short_description = 'User'

    @admin.display(description='Total Amount')
    def total_amount(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())

admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'movie_link', 'quantity', 'price')
    autocomplete_fields = ['movie', 'order']
    list_select_related = ('movie', 'order')

    def movie_link(self, obj):
        url = reverse("admin:movies_movie_change", args=[obj.movie.pk])
        return mark_safe(f'<a href="{url}">{obj.movie.name}</a>')
    movie_link.short_description = 'Movie'

admin.site.register(Item, OrderItemAdmin)


# Customize Admin Site Appearance
admin.site.site_header = "GT Movies Store Admin"
admin.site.site_title = "GT Movies Management"
admin.site.index_title = "Welcome to the GT Movies Store Admin Panel"
