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

    def validate_bookImageURL(self, value):
        if not len(value) == 0:
            raise serializers.ValidationError("url이 공란입니다. 책 정보가 올바른지 확인하십시오.")
        if not value.startswith('http'):
            raise serializers.ValidationError("유효한 URL이 아닌것 같습니다. ")
        return value