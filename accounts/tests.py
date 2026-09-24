from django.test import TestCase
from django.urls import reverse

from .models import User


class AccountFlowTests(TestCase):
    def test_signup_requires_a_region(self):
        response = self.client.post(reverse("signup"), {
            "username": "reader",
            "email": "reader@example.com",
            "password1": "ToughPassword2026!",
            "password2": "ToughPassword2026!",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="reader").exists())
        self.assertIn("region_code", response.context["form"].errors)

    def test_signup_saves_a_valid_region_and_logs_in(self):
        response = self.client.post(reverse("signup"), {
            "username": "reader",
            "email": "reader@example.com",
            "password1": "ToughPassword2026!",
            "password2": "ToughPassword2026!",
            "region_code": "11230",
        })
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(User.objects.get(username="reader").region_code, "11230")
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_profile_requires_region_and_persists_updates(self):
        user = User.objects.create_user(
            username="reader", email="reader@example.com", password="ToughPassword2026!", region_code="11230"
        )
        self.client.force_login(user)
        response = self.client.post(reverse("profile"), {
            "email": "reader@example.com",
            "region_code": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("region_code", response.context["form"].errors)

        response = self.client.post(reverse("profile"), {
            "email": "reader@example.com",
            "region_code": "11010",
        })
        self.assertRedirects(response, reverse("profile"))
        user.refresh_from_db()
        self.assertEqual(user.region_code, "11010")
