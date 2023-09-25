from .models import MybookWishlist
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class MybookWishlistSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = MybookWishlist
        fields = ('user',  'author_username', 'isbn13', 'when_it_put', 'memo',)
