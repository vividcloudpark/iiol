from django.urls import path

from .views import AccountLoginView, AccountLogoutView, AccountPasswordChangeView, profile, signup

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", AccountLoginView.as_view(), name="login"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
    path("password/", AccountPasswordChangeView.as_view(), name="password_change"),
]
