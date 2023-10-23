from .models import MybookWishlist, MybookWishlistGroup
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from books.models import Book
from rest_framework.validators import UniqueTogetherValidator
from django.core.cache import cache
import json

from django.conf import settings
CACHE_TTL = getattr(settings, 'CACHE_TTL')
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'email']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class MybookWishlistSerializer(serializers.ModelSerializer):
    # author_username = serializers.ReadOnlyField(source='user.username')
    created_at  = serializers.ReadOnlyField()
    groupname_desc = serializers.ReadOnlyField(source='groupname.name', allow_null=True)
    groupname = serializers.PrimaryKeyRelatedField(queryset=MybookWishlistGroup.objects.all(), allow_null=True)

    class Meta:
        model = MybookWishlist
        fields = ('user', 'isbn13', 'readYn', 'readDate',
                  'input_context', 'memo', 'DELETED', 'created_at', 'groupname', 'groupname_desc')

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
        if BOOKINFO_JSON is not None:
            response['book'] = json.loads(BOOKINFO_JSON)[0]
        else:
            response['book'] = BookSerializer(ISBN).data
            cache.set(f'ISBN13_{ISBN.isbn13}', json.dumps([BookSerializer(ISBN).data]), CACHE_TTL)
        return response

class MybookWishlistGroupSerializer(serializers.ModelSerializer):
    pk  = serializers.ReadOnlyField()

    class Meta:
        model = MybookWishlistGroup
        fields = ('pk', 'name',)

    
    validaters = [
        UniqueTogetherValidator(
            queryset=MybookWishlistGroup.objects.all(),
            fields=['user', 'name']
        )
    ]