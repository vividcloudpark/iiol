from .models import Barcode
from rest_framework import serializers


class BarcodeSerializer(serializers.ModelSerializer):
    statusMsg = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    user = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Barcode
        fields = ('client', 'small_region_code', 'isbn13',
                  'statusCode', 'statusMsg', 'user', 'ipaddress')
