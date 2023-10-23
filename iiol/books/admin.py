from django.contrib import admin
from .models import Book
from django.utils.safestring import mark_safe


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ["isbn13", "bookname"]
    list_display = ["book_img", "isbn13", "bookname", "authors", "created_at"]
    ordering = ("-created_at",)

    def book_img(self, book):
        return mark_safe(f"<img src={book.bookImageURL} style='width: 100px;' />")
