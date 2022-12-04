from typing import Callable
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from carts.models import CartItem, Cart
from carts.views import _cart_id
# from .models import Order, OrderProduct
# from .forms import OrderForm, OrderCheck
# from .models import OrderProduct, Order
from product.models import Product
from django.contrib.auth.decorators import login_required
# mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from accounts.models import Account
import datetime
from rest_framework import status, authentication, permissions

from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, MyOrderSerializer

@api_view(['POST'])
def checkout(request):
    serializer = OrderSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['order_product'])
       
        try:
            serializer.save(order_total=paid_amount)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)

# Create your views here.

def place_order(request, total=0, quantity=0):
   
    current_user = request.user
    # if the cart item is less than 1, redirect to product
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('product')

    grand_total = 0
    shipping = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    shipping = 30000
    grand_total = total + shipping

    if request.method == 'POST':
        # to receive data, create OrderForm from froms.py
        form = OrderForm(request.POST)
        if form.is_valid():
            # product all billing inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            # data.payment_methods = form.cleaned_data['payment']
            
            data.order_total = grand_total
            data.shipping = shipping
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number by: date + id
            
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(is_ordered=False, order_number=order_number, user=current_user)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'shipping': shipping,
                'grand_total': grand_total,
            }

            return render(request, 'orders/payments.html', context)

        else:
            return redirect('checkout')

def payments(request):
    order = Order.objects.get(user=request.user, is_ordered=False)
    order.is_ordered = True
    order.save()

    # move cart items to OrderProduct table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        # orderproduct.payment = 
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True

        orderproduct.save()

        # Set variation for orderproduct
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

        # Reduce the stock quantity
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()  

    #Delete cart item in carts
    CartItem.objects.filter(user=request.user).delete()

    # Send order-received email to users

    email_subject = "Cảm ơn quý khách đã đặt hàng!"
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    text_content = strip_tags(message) # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(email_subject, text_content, to=[to_email, 'syhoangact@gmail.com'])
    msg.attach_alternative(message, "text/html")
    msg.send()


    # send_mail = EmailMessage(email_subject, message, to=[to_email, 'syhoangact@gmail.com'])
    # send_mail.send()
    return redirect('order_complete')

def order_complete(request):
    order = Order.objects.last()

    # order_number = request.GET.get('order_number')
    order_number = order.order_number
    try:

        order = Order.objects.get(is_ordered=True, order_number=order_number)
 
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        ordertotal = 0
        subtotal = 0

        for item in ordered_products:
            subtotal += item.product.discount * item.quantity

        ordertotal = subtotal + order.shipping

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'subtotal': subtotal,
            'ordertotal': ordertotal,
        }

        return render(request, 'orders/order_complete.html', context)

    except:
        return render(request, 'orders/order_complete.html')

# CHECK ORDERS
def check_order(request, order_input=None, status=None, created_at=None, phone=None, full_name=None):
    # GET ORDER_NUMBER AND CHECK STATUS

    
    if request.method == 'POST':
        
        form = OrderCheck(request.POST)
        if form.is_valid():
            order_input = request.POST.get('order_number')
            print(order_input)
            try:
                order = Order.objects.get(order_number = order_input)
                print(order)
                status = order.status
                created_at = order.created_at
                phone = order.phone
                full_name = order.full_name
            except:
                pass

        
    context = {
        'status': status, 
        'created_at': created_at,
        'phone': phone,
        'full_name': full_name,
        'order_input': order_input,
        
    }
    return render(request, 'orders/checkorders.html', context)

