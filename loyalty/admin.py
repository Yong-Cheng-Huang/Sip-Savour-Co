from django.contrib import admin
from .models import Profile, Coupon

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
    search_fields = ('user__username',)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'discount', 'created_at', 'expires_at', 'is_used')
    search_fields = ('user__username', 'code')
