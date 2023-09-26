from .models import MybookWishlist
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from books.models import Book
from rest_framework.validators import UniqueTogetherValidator


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

    class Meta:
        model = MybookWishlist
        fields = ('user',  'author_username', 'isbn13',
                  'when_it_put', 'memo')
    validaters = [
        UniqueTogetherValidator(
            queryset=MybookWishlist.objects.all(),
            fields=['user', 'isbn13']
        )
    ]

    def validate_isbn13(self, data):
        if len(isbn13) != 13:
            raise ValueError('ISBN은 13자리여야합니다.')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['book'] = BookSerializer(instance.isbn13).data
        return response
