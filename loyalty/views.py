from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Coupon
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.models import User


@login_required
def loyalty_card(request):
    now = timezone.now()

    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    profile = request.user.profile
    local_message = None

    if request.method == 'POST':
        if 'delete_coupon' in request.POST:
            coupon_id = request.POST.get('delete_coupon')
            coupon = get_object_or_404(Coupon, id=coupon_id, user=request.user)
            coupon.delete()
            local_message = "已成功刪除折扣券！"
            
        elif 'redeem' in request.POST:
            profile = request.user.profile
            if profile.points >= 5:
                profile.points -= 5
                profile.save()
                expires_at = timezone.now() + timedelta(days=30)
                Coupon.objects.create(user=request.user, expires_at=expires_at)
                local_message = "兌換成功！已新增一張折扣券。"
            else:
                local_message = "你的點數還沒集滿 5 點，不能兌換喔！"
            
        elif 'use_coupon' in request.POST:
            coupon_id = request.POST.get('use_coupon')
            coupon = get_object_or_404(Coupon, id=coupon_id, user=request.user)
            coupon.is_used = True
            coupon.save()
            local_message = "優惠券已標記為已使用！"

        coupons = Coupon.objects.filter(user=request.user).order_by(
            'is_used',  # 未使用的排在前面
            'expires_at'  # 過期的排在後面
        )
        return render(request, 'loyalty/loyalty_card.html', {
            'profile': profile,
            'coupons': coupons,
            'now': now,
            'local_message': local_message,
        })

    coupons = Coupon.objects.filter(user=request.user).order_by(
        'is_used',  # 未使用的排在前面
        'expires_at'  # 過期的排在後面
    )
    return render(request, 'loyalty/loyalty_card.html', {
        'profile': profile,
        'coupons': coupons,
        'now': now,
        'local_message': local_message,
    })
