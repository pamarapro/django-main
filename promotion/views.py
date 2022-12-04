from django.shortcuts import redirect, render
from .models import Coupon
from .forms import CouponApplyForm
from django.views.decorators.http import require_POST
from django.utils import timezone

from rest_framework.response import Response
from rest_framework import generics
from .serializers import PromotionSerializer
from .models import Promotion
@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )
            request.session['coupon_id'] = coupon.id
        except:
            request.session['coupon_id'] = None

    return redirect('cart:cart_detail')


class PromotionList(generics.ListAPIView):
    queryset = Promotion.objects.all()
    
    def get(self, request, format=None):
        promotions = Promotion.objects.all()
        serializer = PromotionSerializer(promotions, many=True)
        return Response(serializer.data)