from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mybookwishlist'

router = DefaultRouter()
router.register(r'mylist', views.MybookWishListView)

urlpatterns = [
    path('', views.MybookWishListView.as_view(), name='mybookwishlist_root'),
    path('mylist/', views.MybookWishListView.as_view(), name='mylist'),
    # path('delete/<int:userpk>/<int:isbn13>/', views.MybookWishDeleteiew.as_view(), name='delete'),
]
