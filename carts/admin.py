from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product','time_added', 'cart', 'quantity', 'is_active', )
    list_filter = ('time_added',)

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)