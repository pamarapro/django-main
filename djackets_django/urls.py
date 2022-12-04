from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('product.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('promotion.urls')),
    path('api/v1/', include('blog.urls')),
    path('api/v1/', include('data.urls')),
    path('api/v1/', include('policy.urls')),
    path('summernote/', include('django_summernote.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
