from django.urls import path, include

from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/', views.search),
    path('products/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('category/<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('categories/', views.CategoryList.as_view(),),
    path('all-products/', views.ProductsViewSet.as_view({'get': 'list'}),)
]