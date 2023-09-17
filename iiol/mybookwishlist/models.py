from django.db import models
from iiol.models import BaseTimeModel
class MybookWishlist(BaseTimeModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE)
    isbn13 = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE)
    when_it_put = models.CharField(max_length=100)
    memo = models.TextField()
