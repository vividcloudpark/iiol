from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'upload', views.BarcodeViewSet)


app_name = 'barcode'

urlpatterns = [
    path('', views.detect, name='detect_barcodes'),
    path('upload/', views.BarcodeViewSet.as_view(), name='upload'),
]
