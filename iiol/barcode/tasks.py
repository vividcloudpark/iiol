from __future__ import absolute_import, unicode_literals
from celery import shared_task
from books.serializers import BookSerializer
from books.models import Book
from django.shortcuts import get_object_or_404 
from django.core.cache import cache

import logging

@shared_task
def add(x, y):
    return x + y


@shared_task
def save_book_on_DB(BOOKINFO_JSON):
    isbn13=  BOOKINFO_JSON['isbn13']
    book = Book.objects.get(isbn13=isbn13)
    if book is None:
        serializer = BookSerializer(data=BOOKINFO_JSON)
        if serializer.is_valid():
            serializer.save()
        
    
