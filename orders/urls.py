from django.urls import path
from . import views

urlpatterns = [
    # path('place_order/', views.place_order, name='place_order'),
    # path('payments/', views.payments, name="payments"),
    # path('check_order/', views.check_order, name='check_order'),
    # path('order_complete/', views.order_complete, name='order_complete'),

    path('thanh-toan/', views.checkout),
    path('order-list/', views.OrdersList.as_view())
]
