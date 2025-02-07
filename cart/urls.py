from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<int:id>/add_to_cart/', views.add_to_cart, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
]