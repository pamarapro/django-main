from django.db import models
from product.models import Product, Variation
from accounts.models import Account
from promotion.models import Coupon
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=200, blank=True)
    date_added = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    time_added = models.DateTimeField(auto_now_add=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)

    # def __init__(self, request):

    #     self.session = request.session
    #     self.coupon_id = self.session.get('coupon_id')
    
    # def count_added_times(self):
    #     if 

    def sub_total(self):

        
        return self.product.discount * self.quantity


    def __unicode__(self):
        return self.product

    # def total_products(self):
    #     return self.product


