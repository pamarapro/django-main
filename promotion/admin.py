from django.contrib import admin
from .models import Coupon, Promotion
# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'total_spent', 'max_code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to', 'total_spent']
    search_fields = ['code']

class PromotionAdmin(admin.ModelAdmin):
    list_display = ['name', 'banner', 'running', 'created_at']
    list_filter = ['running']
    search_fields = ['name']

admin.site.register(Coupon, CouponAdmin)
admin.site.register(Promotion, PromotionAdmin)