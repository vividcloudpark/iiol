from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from .forms import ProfileForm, SignupForm


class AccountLoginView(LoginView):
    template_name = "accounts/form.html"
    authentication_form = AuthenticationForm
    extra_context = {"title": "로그인", "submit_label": "로그인"}


class AccountLogoutView(LogoutView):
    http_method_names = ["post", "options"]


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "가입이 완료되었습니다.")
        return redirect("home")
    return render(request, "accounts/form.html", {
        "form": form,
        "title": "회원가입",
        "submit_label": "가입하기",
    })


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "프로필을 수정했습니다.")
        return redirect("profile")
    return render(request, "accounts/form.html", {
        "form": form,
        "title": "내 정보 수정",
        "submit_label": "저장하기",
    })


class AccountPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "accounts/form.html"
    success_url = reverse_lazy("profile")
    extra_context = {"title": "비밀번호 변경", "submit_label": "비밀번호 변경"}
