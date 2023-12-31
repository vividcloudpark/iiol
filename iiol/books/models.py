from django.db import models
from iiol.models import BaseTimeModel


class Book(BaseTimeModel):
    isbn13 = models.CharField(blank=False, unique=True,
                              db_index=True, primary_key=True, max_length=13)
    isbn = models.CharField(max_length=10, blank=True)
    bookname = models.CharField(blank=False, max_length=300)
    publication_date = models.CharField(max_length=20)
    authors = models.CharField(blank=False, max_length=100)
    publisher = models.CharField(max_length=100, blank=True)
    class_no = models.CharField(max_length=100, blank=True)
    class_nm = models.CharField(max_length=100, blank=True)
    publication_year = models.CharField(max_length=20, blank=True)
    bookImageURL = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'({self.isbn13}) {self.bookname}'
