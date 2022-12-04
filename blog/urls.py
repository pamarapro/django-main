from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('post/<slug:post_slug>/', views.PostDetail.as_view()),
]
