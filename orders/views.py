from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem

# Create your views here.

@login_required
def checkout(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    if not cart.items.exists():
        messages.warning(request, '購物車是空的！')
        return redirect('cart:view_cart')
    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def place_order(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.warning(request, '購物車是空的！')
            return redirect('cart:view_cart')

        # 創建訂單
        order = Order.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            notes=request.POST.get('notes', ''),
            total_price=cart.total_price
        )

        # 創建訂單項目
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # 清空購物車
        cart.items.all().delete()

        messages.success(request, '訂單已成功送出！')
        return redirect('orders:order_detail', order_id=order.id)
    return redirect('cart:view_cart')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        return render(request, 'orders/order_detail.html', {
            'order': order,
        })
    except Order.DoesNotExist:
        messages.error(request, '找不到該訂單')
        return redirect('orders:order_list')
