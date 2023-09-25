from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mybookwishlist'

router = DefaultRouter()
router.register(r'mylist', views.MybookWishListViewSet)

urlpatterns = [
    path('mylist/', views.MybookWishListViewSet.as_view(), name='mylist'),
]
