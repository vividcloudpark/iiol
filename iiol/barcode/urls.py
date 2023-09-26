from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'detect', views.BarcodeView)


app_name = 'barcode'

urlpatterns = [
    path('', views.detect_page, name='barcode_root'),
    path('detect/', views.BarcodeView.as_view(), name='detect'),
    path('region_code/', views.retrieve_region_code, name='region_code'),
]
