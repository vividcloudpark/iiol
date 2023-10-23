from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static

app_name = "mybookwishlist"

router = DefaultRouter()
router.register(
    r"mylist",
    views.MybookWishListViewSet,
)

mybookwishlist_list = views.MybookWishListViewSet.as_view(
    {"get": "list", "post": "create", "patch": "partial_update", "delete": "destroy"}
)

mybookwishlist_by_group_create = views.MybookWishListViewSet.as_view(
    {
        "post": "create_group",
    }
)

mybookwishlist_by_group = views.MybookWishListViewSet.as_view(
    {
        "patch": "update_group",
        "delete": "delete_group",
    }
)

urlpatterns = [
    path("api/", include(router.urls), name="mybookwishlist_root"),
    path("mylist/", mybookwishlist_list, name="mylist"),
    path("group/", mybookwishlist_by_group_create, name="mylist_group_create"),
    path("group/<int:groupPk>/", mybookwishlist_by_group, name="mylist_group"),
]
