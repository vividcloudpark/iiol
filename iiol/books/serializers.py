from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('isbn13',
                    'isbn',
                    'bookname',
                    'publication_date',
                    'authors',
                    'publisher',
                    'class_no',
                    'class_nm',
                    'publication_year',
                    'bookImageURL',
                    'description',
                    )
