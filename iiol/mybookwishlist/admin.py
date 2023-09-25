from django.contrib import admin
from .models import MybookWishlist


@admin.register(MybookWishlist)
class MybookWishlistAdmin(admin.ModelAdmin):
    pass

# Register your models here.
