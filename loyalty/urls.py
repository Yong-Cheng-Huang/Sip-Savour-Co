from django.urls import path
from . import views

urlpatterns = [
    path('card/', views.loyalty_card, name='loyalty_card'),
]
