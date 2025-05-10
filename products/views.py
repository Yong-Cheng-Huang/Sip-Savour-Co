from django.shortcuts import render
from .models import Product, Category


def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:3]
    context = {
        'featured_products': featured_products
    }
    return render(request, 'home.html', context)


def product_list(request):
    # 獲取篩選參數
    category_id = request.GET.get('category', '')

    # 獲取所有分類
    categories = Category.objects.all()

    # 基本查詢集
    products = Product.objects.all()

    # 應用篩選
    if category_id:
        try:
            products = products.filter(category_id=category_id)
        except (Category.DoesNotExist, ValueError):
            pass

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    }

    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
