from django.contrib import admin
from .models import MybookWishlist

@admin.register(MybookWishlist)
class MybookWishlistAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'isbn13__bookname', 'isbn13__isbn13', 'memo']
    list_display = ['user', 'isbn13', 'memo', 'readYn']

