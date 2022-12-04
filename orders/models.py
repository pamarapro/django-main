from django.db import models
from django.db.models.base import Model
from accounts.models import Account
from product.models import Product,Variation
# Create your models here.

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('Thanh toán khi nhận hàng', 'Thanh toán khi nhận hàng'),
        ('Chuyển khoản online', 'Chuyển khoản online'),
        ('Quét mã Momo', 'Quét mã Momo'),
    )
    # user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    # payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHODS, default='Thanh toán khi nhận hàng', blank=True)

    def __str__(self):
        return self.payment_id
    class Meta:
        verbose_name = 'Phương thức thanh toán'
        verbose_name_plural = "Phương thức thanh toán"

class Order(models.Model):
    STATUS = (
        ('Mới', 'Mới'),
        ('Đang xử lý', 'Đang xử lý'),
        ('Hoàn tất', 'Hoàn tất'),
        ('Huỷ', 'Huỷ'),
    )

    # user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    # email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    # address_line_2 = models.CharField(max_length=100)
    # state = models.CharField(max_length=100)
    # city = models.CharField(max_length=100)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()  
    shipping = models.FloatField()
    status = models.CharField(max_length=100, choices=STATUS, default='Mới')
    ip =  models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def full_name(self):
    #     return f'{self.first_name} {self.last_name}'

    # def full_address(self):
    #     return f'{self.address_line_1}, {self.address_line_2}, {self.state}, {self.city}'
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Đơn hàng'
        verbose_name_plural = "Đơn hàng"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_product")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    # user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_product")
    variation = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def  __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Sản phẩm đặt hàng'
        verbose_name_plural = "Sản phẩm đặt hàng"