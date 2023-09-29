from .models import MybookWishlist
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from books.models import Book
from rest_framework.validators import UniqueTogetherValidator
from django.core.cache import cache
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class MybookWishlistSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='user.username')
    created_at  = serializers.ReadOnlyField()

    class Meta:
        model = MybookWishlist
        fields = ('user',  'author_username', 'isbn13', 'readYn', 'readDate',
                  'input_context', 'memo', 'DELETED', 'created_at')
    validaters = [
        UniqueTogetherValidator(
            queryset=MybookWishlist.objects.all(),
            fields=['user', 'isbn13']
        )
    ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        ISBN = instance.isbn13 if type(
            instance) == MybookWishlist else instance['isbn13']
        BOOKINFO_JSON = cache.get(f'ISBN13_{ISBN.isbn13}')
        response['book'] = json.loads(BOOKINFO_JSON)[0] if BOOKINFO_JSON is not None else BookSerializer(ISBN).data
        return response
