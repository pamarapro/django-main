from django.urls import path, include
from . import views

urlpatterns = [
    path('banner/', views.PromotionList.as_view())
]
