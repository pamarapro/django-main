from django.contrib.auth import tokens
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages, auth
from django.http import HttpResponse

from accounts.forms import RegistrationForm, UserForm, UserProfileForm
from accounts.models import Account, UserProfile 
from django.contrib.auth.decorators import login_required


import requests

# EMAIL
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.models import CartItem, Cart
from carts.views import _cart_id
from orders.models import Order, OrderProduct


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password'] 
            email = form.cleaned_data['email']
            # username = form.cleaned_data['username']
            username = email.split('@')[0]
            

            user = Account.objects .create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password,
                username=username,
            )
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            email_subject = "Vui lòng kích hoạt tài khoản của bạn."
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            to_email = email
            send_mail = EmailMessage(email_subject, message, to=[to_email])
            send_mail.send()


            # messages.success(request, "Cảm ơn bạn đã đăng ký! Chúng tôi đã gửi 1 email kèm đường link xác thực đến địa chỉ email của bạn, vui lòng kiểm tra & kích hoạt tài khoản.")
            return redirect("/accounts/login/?command=verification&email="+email)

    else:
        # if just get request --> send form    
        form = RegistrationForm()


    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)
    
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
 
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # get the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get cart item in user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # Compare and find the same variation in both and increase quantity
                    for pv in product_variation:
                        if pv in ex_var_list:
                            index = ex_var_list.index(pv)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)

                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass


            auth.login(request, user)
            messages.success(request, "Bạn đã đăng nhập thành công!")
            # REDIRECT TO CHECKOUT AFTER LOGIN --- FOR USING @login_required in checkout page( which i dont use )
            url = request.META.get('HTTP_REFERER')

            
            

            try:
                query = requests.utils.urlparse(url).query
                #next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if next in params:
                    nextPage = params['next']
                    return redirect(nextPage)

            except:
                return redirect("dashboard")    

        else:
            messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
            return redirect("login")

    return render(request, 'accounts/login.html')
    
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "Đăng xuất thành công.")
    return redirect("login")
    
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Chúc mừng! Tài khoản của bạn đã được kích hoạt thành công.')
        return redirect("login")

    else:
        messages.error(request, "Link bị lỗi hoặc đã hết hạn")
        return redirect("register")

@login_required(login_url="login")
def dashboard(request):
    orders =  Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    count_orders = orders.count()

    user_profile = UserProfile.objects.get(user_id=request.user.id)


    context = {
        'count_orders': count_orders,
        'user_profile': user_profile,

    }

    return render(request, 'accounts/dashboard.html', context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # USER FORGOT PW
            current_site = get_current_site(request)
            email_subject = "Lấy lại mật khẩu đăng nhập."
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            to_email = email
            send_mail = EmailMessage(email_subject, message, to=[to_email])
            send_mail.send()

            messages.success(request, "Yêu cầu lấy lại mật khẩu thành công, chúng tôi đã gửi 1 email kèm đường link để lấy lại mật khẩu, vui lòng kiểm tra email của bạn.")
            return redirect('login')

        else:
            messages.error(request, "Email bạn nhập không khớp với bất kỳ tài khoản nào. Vui lòng thử lại.")
            return redirect("forgotPassword")
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Vui lòng lấy lại mật khẩu của bạn.")
        return redirect('resetPassword')

    else:
        messages.error(request, "Link này đã hết hạn, vui lòng kiểm tra lại.")
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()

            messages.success(request, "Thay đổi mật khẩu thành công!")
            return redirect("login")

        else:
            messages.error(request, "Mật khẩu nhập vào không khớp, vui lòng thử lại.")
            return redirect('resetPassword')

    else:

        return render(request, 'accounts/reset_password.html')

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user_id=request.user.id, is_ordered=True).order_by('-created_at')
    count_orders = orders.count()

    context = {
        'orders': orders,
        'count_orders': count_orders,
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        print('USERPROFILE')
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            print('UNDER')
            user_profile_form.save()
            messages.success(request, 'Cập nhật thông tin cá nhân thành công!')
            print('CHECKEDDD')
            return redirect('edit_profile')
    else:
        print('GET INSTANCE')
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'userprofile': userprofile,
    }

    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_new_password:
            checked_old_password = user.check_password(current_password)
            if checked_old_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Thay đổi mật khẩu thành công.')
                return redirect('change_password')

            else:
                messages.error(request, 'Mật khẩu cũ không chính xác, vui lòng thử lại.')
                return redirect('change_password')
        else:
            messages.error(request, 'Mật khẩu mới bạn nhập không khớp, vui lòng thử lại.')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    ordertotal = 0

    for i in order_detail:
        subtotal += i.product_price * i.quantity
    ordertotal = subtotal + order.shipping
    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
        'ordertotal': ordertotal,
    }

    return render(request, 'accounts/order_detail.html', context)