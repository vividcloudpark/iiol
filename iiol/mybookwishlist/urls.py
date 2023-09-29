from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mybookwishlist'

router = DefaultRouter()
router.register(r'mylist', views.MybookWishListViewSet, )

mybookwishlist_list = views.MybookWishListViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('', include(router.urls), name='mybookwishlist_root'),
    path('mylist/', mybookwishlist_list, name='mylist'),

]

