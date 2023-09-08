from .models import Barcode
from rest_framework import serializers


class BarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barcode
        fields = ('image',)
