# fortune/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.daily_fortune, name='daily_fortune'),
    path('draw-new-card/', views.draw_new_card, name='draw_new_card'),
]
