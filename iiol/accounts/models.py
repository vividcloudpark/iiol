from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.template.loader import render_to_string
from django.core.validators import RegexValidator
# Create your models here.


class User(AbstractUser):

    bio = models.TextField(blank=True)

    phone_number = models.CharField(
        validators=[RegexValidator("^010-?[1-9]\d{3}-?\d{4}$")],
        max_length=14,
        default='000-0000-0000')

    @property
    def user_name(self):
        return f"{self.first_name} {self.last_name}"

    def send_welcome_email(self):
        subject = render_to_string("accounts/welcome_email_subject.txt", {
            "user": self,
        })

        content = render_to_string("accounts/welcome_email_content.txt", {
            "user": self,
        })

        sender_email = settings.WELCOME_EMAIL_SENDER
        send_mail(subject, content,
                  sender_email[self.email], fail_silently=False)
