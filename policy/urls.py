from django.urls import path, include

from policy import views

urlpatterns = [
    path('policy/', views.PolicyPageLists.as_view()),
    path('policy/<slug:policy_slug>/', views.PolicyDetail.as_view()),
]