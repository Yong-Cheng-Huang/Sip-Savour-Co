from django.shortcuts import render
from products.models import Product

def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:3]
    context = {
        'featured_products': featured_products
    }
    return render(request, 'home.html', context)

def news_index(request):
    context = {
        'title': '元氣鬆餅堡｜新品上市',
        'publish_date': '2025-05-16',
    }
    return render(request, 'news/index.html', context)