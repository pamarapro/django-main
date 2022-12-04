from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.

class OrderProductInLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['product','variation', 'quantity', 'price',]
    extra = 0
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'order_total', 'status', 'is_ordered']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'name', 'phone']
    list_per_page = 50
    inlines = [OrderProductInLine]

admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
 