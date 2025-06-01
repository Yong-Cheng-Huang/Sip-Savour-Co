from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem
from loyalty.models import Coupon, Profile
from django.utils import timezone

# Create your views here.

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    applied_coupon = request.session.get('applied_coupon')
    discount_amount = 0
    final_price = cart.total_price

    # 獲取用戶所有可用的優惠券
    available_coupons = Coupon.objects.filter(
        user=request.user,
        is_used=False,
        expires_at__gt=timezone.now()
    ).order_by('expires_at')

    if applied_coupon:
        try:
            coupon = Coupon.objects.get(code=applied_coupon, user=request.user)
            if not coupon.is_used and coupon.expires_at > timezone.now():
                discount_amount = (cart.total_price * coupon.discount) // 100
                final_price = cart.total_price - discount_amount
        except Coupon.DoesNotExist:
            request.session.pop('applied_coupon', None)
            applied_coupon = None

    context = {
        'cart': cart,
        'applied_coupon': applied_coupon,
        'discount_amount': discount_amount,
        'final_price': final_price,
        'available_coupons': available_coupons,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def place_order(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.warning(request, '購物車是空的！')
            return redirect('cart:view_cart')

        # 計算折扣
        discount_amount = 0
        final_price = cart.total_price
        applied_coupon = request.session.get('applied_coupon')
        
        if applied_coupon:
            try:
                coupon = Coupon.objects.get(code=applied_coupon, user=request.user)
                if not coupon.is_used and coupon.expires_at > timezone.now():
                    discount_amount = (cart.total_price * coupon.discount) // 100
                    final_price = cart.total_price - discount_amount
                    # 標記優惠券為已使用
                    coupon.is_used = True
                    coupon.save()
            except Coupon.DoesNotExist:
                pass

        # 創建訂單
        order = Order.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            notes=request.POST.get('notes', ''),
            total_price=cart.total_price,
            discount_amount=discount_amount,
            final_price=final_price
        )

        # 創建訂單項目
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # 計算並添加點數（每50元換一點）
        points_to_add = final_price // 50
        if points_to_add > 0:
            profile = Profile.objects.get(user=request.user)
            profile.points += points_to_add
            profile.save()
            messages.success(request, f'恭喜獲得 {points_to_add} 點！')

        # 清空購物車和優惠券
        cart.items.all().delete()
        request.session.pop('applied_coupon', None)

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

@login_required
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=coupon_code, user=request.user)
            if coupon.is_used:
                messages.error(request, '此優惠券已被使用')
            elif coupon.expires_at < timezone.now():
                messages.error(request, '此優惠券已過期')
            else:
                request.session['applied_coupon'] = coupon_code
                messages.success(request, '優惠券已成功套用')
        except Coupon.DoesNotExist:
            messages.error(request, '無效的優惠券代碼')
    return redirect('orders:checkout')

@login_required
def remove_coupon(request):
    if request.method == 'POST':
        request.session.pop('applied_coupon', None)
        messages.success(request, '優惠券已移除')
    return redirect('orders:checkout')
