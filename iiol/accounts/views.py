from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm, ProfileForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, logout_then_login, PasswordChangeView as AuthPasswordChangeView)
from django.urls import reverse_lazy
from django.conf import settings
login = LoginView.as_view(template_name="accounts/login_form.html")


def logout(request):
    messages.success(request, "로그아웃 되었습니다!")
    return logout_then_login(request, login_url=f'{settings.FORCE_SCRIPT_NAME}/accounts/login')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입을 환영합니다.")
            next_url = request.Get.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()

    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_vaild():
            form.save()
            messages.success(request, "프로필 수정/저장완료!")
            return redirect("profile_edit")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit_form.html", {
        'form': form
    })


class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url = reverse_lazy('')
    template_name = 'accounts/password_change_form.html'

    def form_valid(self):
        messages.success(self.request, "암호를 변경했습니다")
        return super().form_valid(form)
    pass


password_change = PasswordChangeView.as_view()
