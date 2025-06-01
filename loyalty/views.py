from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Coupon
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.timezone import now


@login_required
def loyalty_card(request):
    now = timezone.now()

    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user, phone="請補填手機號")

    profile = request.user.profile

    local_message = None

    if request.method == 'POST':
        if request.user.is_superuser:
            phone = request.POST.get('phone')
            try:
                target_profile = Profile.objects.get(phone=phone)
                target_profile.points += 1
                target_profile.save()
                profile.refresh_from_db()
                local_message = f"已成功幫 {phone} 加 1 點！"
            except Profile.DoesNotExist:
                local_message = f"找不到電話 {phone}，請確認輸入正確！"

        elif 'delete_coupon' in request.POST:
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

        # ✅ ✅ ✅ 這裡重新抓最新的 coupon
        profile = request.user.profile
        coupons = Coupon.objects.filter(user=request.user)

        return render(request, 'loyalty/loyalty_card.html', {
            'profile': profile,
            'coupons': coupons,
            'now': now,
            'local_message': local_message,
        })

    # GET 的情況
    profile = request.user.profile
    coupons = Coupon.objects.filter(user=request.user)

    return render(request, 'loyalty/loyalty_card.html', {
        'profile': profile,
        'coupons': coupons,
        'now': now,
        'local_message': local_message,
    })
