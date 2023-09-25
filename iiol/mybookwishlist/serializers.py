from .models import MybookWishlist
from rest_framework import serializers


class MybookWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = MybookWishlist
        fields = ('when_it_put', 'memo')
