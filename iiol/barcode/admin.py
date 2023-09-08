from django.contrib import admin
from .models import Barcode

@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    pass

