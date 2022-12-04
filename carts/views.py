from django.core.checks import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from product.models import Product, Variation
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from promotion.forms import CouponApplyForm
import requests
from promotion.models import Coupon
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    
    product = Product.objects.get(id=product_id) #get the product
    current_user = request.user

    #IF USER IS AUTHENTICATEDD
    if current_user.is_authenticated:
        product_variations = []

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)

                except:
                    pass
        

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            #existing variation -> database
            # current variation -> product_variation
            # item_id -> database 
            ex_var_list = []
            id = []

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            

            if product_variations in ex_var_list:
            
                #increase cart_item quantity
                index = ex_var_list.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product = product, id=item_id)
                item.quantity += 1
                item.save()
                

            else:
                #create a new cart item

                item = CartItem.objects.create(product=product, quantity = 1, user=current_user)

                if len(product_variations) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variations)
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user=current_user,
            )
            if len(product_variations) > 0:
                cart_item.variations.clear()

                cart_item.variations.add(*product_variations)
            cart_item.save()
        
        return redirect('cart')

    else:
        product_variations = []

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)

                except:
                    pass
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session (cookies)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request) 
            ) 
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            #existing variation -> database
            # current variation -> product_variation
            # item_id -> database 
            ex_var_list = []
            id = []

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            

            if product_variations in ex_var_list:
            
                #increase cart_item quantity
                index = ex_var_list.index(product_variations)
                item_id = id[index]
                item = CartItem.objects.get(product = product, id=item_id)
                item.quantity += 1
                item.save()
                

            else:
                #create a new cart item

                item = CartItem.objects.create(product=product, quantity = 1, cart=cart)

                if len(product_variations) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variations)
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variations) > 0:
                cart_item.variations.clear()

                cart_item.variations.add(*product_variations)
            cart_item.save()
        
        return redirect('cart')
       

def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



def cart(request, shipping = 0, total=0, quantity=0, grand_total=0, discounted_price=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.discount * cart_item.quantity)
            quantity += cart_item.quantity

        if total < 1000000:
            shipping = 30000
        else:
            shipping = 0
        
    
    except ObjectDoesNotExist:
        pass   #ignore


    coupon_apply_form = CouponApplyForm()
    if request.method == 'POST':
        form = CouponApplyForm(request.POST or None)
        if form.is_valid():

            try:
                code = form.cleaned_data.get('code')
                coupon = Coupon.objects.get(code=code,)
                print(code)
                if coupon:
                    discounted = coupon.discount
                    discounted_price = total*discounted
                else:
                    pass
                return discounted_price
            except:
                pass
            #     cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            #     cart_items.coupon = get_coupon(request, code)
            #     # cart_items.save()
            #     return redirect('cart')

            # except ObjectDoesNotExist:
            #     return redirect('cart')

    grand_total = total + shipping - discounted_price
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'shipping': shipping,
        'grand_total': grand_total,
        'coupon_apply_form': coupon_apply_form,
    } 
    return render(request, 'store/cart.html', context)

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code,)
    except ObjectDoesNotExist:
        messages.info('Do not have access')
        return redirect('checkout')

def add_coupon(request):
        if request.method == 'POST':
            form = CouponApplyForm(request.POST or None)
            if form.is_valid():

                try:
                    code = form.cleaned_data.get('code')
                    coupon = Coupon.objects.get(code=code,)
                    # print(code)
                    # if coupon:
                    #     discounted = coupon.discount
                    #     discounted_price = total*discounted

                    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
                    cart_items.coupon = get_coupon(request, code)
                    # cart_items.save()
                    return redirect('cart')

                except ObjectDoesNotExist:
                    return redirect('cart')
        #raise erros
        return render(request, 'store/cart.html')


@login_required(login_url='login')
def checkout(request, shipping = 0, total=0, quantity=0, grand_total=0, cart_items=None, province_id=None, city=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.discount * cart_item.quantity)
            quantity += cart_item.quantity

        if total < 1000000:
            shipping = 30000 
        else:
            shipping = 0

        grand_total = total + shipping
    
    except ObjectDoesNotExist:
        pass   #ignore
    
    # GHN API
    query = {'token': '8b0febe1-e748-11ea-a8d3-9e52d41de21a'}

        # 1. Get PROVINCE
    province_response = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/province', headers=query)
    district_response = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/district', headers=query)
    ward_response = requests.get('https://online-gateway.ghn.vn/shiip/public-api/master-data/ward', headers=query)
    provinces = province_response.json()['data']
    districts = district_response.json()['data']
    
    province_names = []
    district_names = []

    # Store all data
    for i in range(0, len(provinces)):
        p = provinces[i]['ProvinceName']
        province_names.append(p)
    city = request.GET.get('city')
    if city is not None:
        
        print(city)
        for i in range(0, len(provinces)):
            if provinces[i]['ProvinceName'] == city:
                province_id = provinces[i]['ProvinceID']

        print(province_id)

        for i in range(0, len(districts)):
            if districts[i]['ProvinceID'] == province_id:
                p = districts[i]['DistrictName']

                district_names.append(p)
        context = {
        
        'province_names': province_names,
        'district_names': district_names,
        } 

        print(district_names)
    else:

    # TODO: CAN GET THE DISTRICTS IN CONSOLE BUT CANNOT SHOW ON HTML FILE!!


        
        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'shipping': shipping,
            'grand_total': grand_total,
            'province_names': province_names,
        } 
    return render(request, 'store/checkout.html', context)