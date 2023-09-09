from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'upload', views.BarcodeViewSet)


app_name = 'barcode'

urlpatterns = [
    path('', views.detect, name='detect_barcodes'),
    path('upload/', views.BarcodeViewSet.as_view(), name='upload'),
    path('region_code/', views.retrieve_region_code, name='region_code'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
