from django.contrib import admin
from .models import Library,SmallRegion,BigRegion
# Register your models here.
@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    pass

@admin.register(SmallRegion)
class SmallRegionAdmin(admin.ModelAdmin):
    pass

@admin.register(BigRegion)
class BigRegionAdmin(admin.ModelAdmin):
    pass