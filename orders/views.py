from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem
from loyalty.models import Coupon, Profile
from django.utils import timezone
from django.db.models import Q

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
        # 如果是管理員，可以查看所有訂單
        if request.user.is_staff:
            order = Order.objects.get(id=order_id)
        else:
            # 一般用戶只能查看自己的訂單
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

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_order_list(request):
    # 獲取所有訂單
    orders = Order.objects.all().order_by('-created_at')
    
    # 搜尋功能
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # 狀態篩選
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status_filter,
        'search_query': search_query,
    }
    return render(request, 'orders/admin_order_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'訂單 {order.order_number} 狀態已更新為 {order.get_status_display()}')
        else:
            messages.error(request, '無效的訂單狀態')
            
    return redirect('orders:admin_order_list')
