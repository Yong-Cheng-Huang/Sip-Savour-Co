from django.urls import path
from . import views  # 你目前 news 的 view 寫在 products 裡

urlpatterns = [
    path('', views.news_index, name='news_index'),
]