from django.db import models
from iiol.models import BaseTimeModel


class MybookWishlist(BaseTimeModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE)
    isbn13 = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE)
    when_it_put = models.CharField(max_length=100, blank=True)
    memo = models.TextField(blank=True)
    readYn = models.BooleanField(default=False)
    class Meta:
        unique_together = ('user', 'isbn13')
    def __str__(self):
        return f'{self.user}/{self.isbn13.isbn13}  | {self.isbn13.bookname} | {self.memo}'