from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from movies.models import Movie, Review
from cart.models import Order, Item

# Inline for Reviews in the Movie admin
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ('user', 'comment', 'rating', 'created_date')
    readonly_fields = ('created_date',)

# Movie Admin Configuration
class MovieAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'price', 'genre', 'image_thumbnail')
    search_fields = ('name', 'genre')
    list_filter = ('genre',)
    ordering = ('name',)
    inlines = [ReviewInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'description', 'genre', 'image', 'image_url', 'image_preview')
        }),
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """
        Display a larger preview of the image (uploaded or via URL) on the detail page.
        """
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;" />')
        elif obj.image_url:
            return mark_safe(f'<img src="{obj.image_url}" style="max-height: 200px;" />')
        return "No Image Available"
    image_preview.short_description = "Image Preview"

    def image_thumbnail(self, obj):
        """
        Display a small thumbnail of the image for the list view.
        """
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 50px;" />')
        elif obj.image_url:
            return mark_safe(f'<img src="{obj.image_url}" style="max-height: 50px;" />')
        return "No Image"
    image_thumbnail.short_description = "Thumbnail"

admin.site.register(Movie, MovieAdmin)

# Review Admin Configuration
class ReviewAdmin(admin.ModelAdmin):
    save_on_top = True
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

# Order & OrderItem Admin Configuration
class OrderItemInline(admin.TabularInline):
    model = Item
    extra = 1
    autocomplete_fields = ['movie']

class OrderAdmin(admin.ModelAdmin):
    save_on_top = True
    date_hierarchy = 'date'
    list_display = ('user_link', 'date', 'total_amount', 'item_count', 'item_summary')
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

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Item Count'

    def item_summary(self, obj):
        items = obj.items.all()
        if not items:
            return "No items"
        summary = "<br>".join([f"{item.movie.name} (Qty: {item.quantity})" for item in items])
        return mark_safe(summary)
    item_summary.short_description = 'Items in Order'

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('order_link', 'movie_link', 'quantity', 'price')
    autocomplete_fields = ['movie', 'order']
    list_select_related = ('movie', 'order')
    list_filter = ('order', 'movie')
    search_fields = ('order__id', 'movie__name')

    def order_link(self, obj):
        url = reverse("admin:cart_order_change", args=[obj.order.pk])
        return mark_safe(f'<a href="{url}">Order #{obj.order.pk}</a>')
    order_link.short_description = 'Order'

    def movie_link(self, obj):
        url = reverse("admin:movies_movie_change", args=[obj.movie.pk])
        return mark_safe(f'<a href="{url}">{obj.movie.name}</a>')
    movie_link.short_description = 'Movie'

admin.site.register(Item, OrderItemAdmin)

# Customize Admin Site Appearance
admin.site.site_header = "GT Movies Store Admin"
admin.site.site_title = "GT Movies Management"
admin.site.index_title = "Welcome to the GT Movies Store Admin Panel"
