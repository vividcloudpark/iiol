from django.contrib import admin
from .models import MybookWishlist, MybookWishlistGroup


@admin.register(MybookWishlist)
class MybookWishlistAdmin(admin.ModelAdmin):
    search_fields = ["user__username", "isbn13__bookname", "isbn13__isbn13", "memo"]
    list_display = ["DELETED", "user", "isbn13", "groupname", "memo", "readYn"]
    list_filter = ["DELETED", "user"]


@admin.register(MybookWishlistGroup)
class MybookWishlistGrouptAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
