from django.db import models

# Create your models here.

class Book(models.Model):
    bookname = models.CharField(blank=False)
    publication_date = models.CharField(max_length=4)
    authors = models.CharField(blank=False)
    publisher = models.CharField()
    class_no = models.CharField()
    class_nm = models.CharField()
    publication_year: models.CharField()
    bookImageURL = models.URLField()
    isbn = models.CharField()
    isbn13 = models.CharField(blank=False)
    description = models.TextField()

