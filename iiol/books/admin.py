from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ['isbn13', 'bookname']
    list_display = ['isbn13', 'bookname', 'authors']

