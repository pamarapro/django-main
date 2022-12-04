from django.urls import path, include

from data import views

urlpatterns = [
    path('data/', views.DataLists.as_view()),

]