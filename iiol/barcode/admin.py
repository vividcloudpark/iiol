from django.contrib import admin
from .models import Barcode


@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ['client', 'statusCode',
                    'isbn13', 'created_at', 'user', 'ipaddress']
