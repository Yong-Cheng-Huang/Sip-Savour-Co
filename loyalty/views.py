from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Coupon
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required
def loyalty_card(request):
    profile = request.user.profile
    coupons = Coupon.objects.filter(user=request.user)

    if request.method == 'POST' and profile.points >= 5:
        # 集滿5點兌換折扣券
        profile.points -= 5
        profile.save()
        expires_at = timezone.now() + timedelta(days=30)  # 30天有效
        Coupon.objects.create(user=request.user, expires_at=expires_at)
        return redirect('loyalty_card')

    return render(request, 'loyalty/loyalty_card.html', {
        'profile': profile,
        'coupons': coupons,
    })

@login_required
def loyalty_card(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user, phone="請補填手機號")

    profile = request.user.profile
    coupons = Coupon.objects.filter(user=request.user)

    if request.method == 'POST':
        # 加點數
        if 'phone' in request.POST:
            phone = request.POST.get('phone')
            try:
                target_profile = Profile.objects.get(phone=phone)
                target_profile.points += 1
                target_profile.save()
                messages.success(request, f"已成功幫 {phone} 加 1 點！")
            except Profile.DoesNotExist:
                messages.error(request, f"找不到電話 {phone}，請確認輸入正確！")
            return redirect('loyalty_card')

        # 刪除折扣券
        if 'delete_coupon' in request.POST:
            coupon_id = request.POST.get('delete_coupon')
            coupon = get_object_or_404(Coupon, id=coupon_id, user=request.user)
            coupon.delete()
            messages.success(request, "已成功刪除折扣券！")
            return redirect('loyalty_card')

        # 【⚡️這邊修正重點：兌換】
        if 'redeem' in request.POST:
            if profile.points >= 5:  # ✅ 滿 5 點才能兌換
                profile.points -= 5
                profile.save()
                expires_at = timezone.now() + timedelta(days=30)  # 折扣券 30 天有效
                Coupon.objects.create(user=request.user, expires_at=expires_at)
                messages.success(request, "兌換成功！已新增一張折扣券。")
            else:
                messages.error(request, "你的點數還沒集滿 5 點，不能兌換喔！")
            return redirect('loyalty_card')
        
        if 'use_coupon' in request.POST:
            coupon_id = request.POST.get('use_coupon')
            coupon = get_object_or_404(Coupon, id=coupon_id, user=request.user)
            coupon.is_used = True
            coupon.save()
            messages.success(request, "優惠券已標記為已使用！")
            return redirect('loyalty_card')

    return render(request, 'loyalty/loyalty_card.html', {
        'profile': profile,
        'coupons': coupons,
    })