from .models import Library
from rest_framework import serializers


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ('libCode',
                  'libName',
                  'address',
                  'tel',
                  'fax',
                  'latitude',
                  'longitude',
                  'homepage',
                  'closed',
                  'operatingTime',
                  'big_region_code',
                  'small_region_code',
                  )
