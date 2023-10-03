from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.urls import reverse, resolve

from .forms import SignupForm, ProfileForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, logout_then_login, PasswordChangeView as AuthPasswordChangeView)
from django.urls import reverse_lazy
from django.conf import settings
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.middleware import csrf

from rest_framework_simplejwt.views import token_verify

# login = LoginView.as_view(template_name="accounts/login_form.html")
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def verify_access_token(token):
    try:
        access_token = AccessToken(token)
        access_token.verify()
        return True
    except Exception as e:
        return False

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [] #인증 안함을 명시적으로 밝힘.
    template_name = "accounts/login_form.html"
    return_json = {'status': {'code': "", 'msg': ""}, 'result_data': {}}
    response_type = "render"
    response = None
    request = None
    def set_JSON_header(self, code, msg):
        self.return_json["status"]["code"] = code
        self.return_json["status"]["msg"] = msg
    def response_with_type(self, code, msg, RESTCode=200, JWT_data=None):
        self.set_JSON_header(code, msg)
        self.return_json['result_data']['JWT'] = JWT_data
        # self.response_type = 'json'
        if self.response_type == "json":
            response = JsonResponse(data=self.return_json, status=RESTCode, json_dumps_params={'ensure_ascii': False})
        elif self.request.GET.get('next') or self.request.POST.get('next'):
            next_url = self.request.GET.get('next') if self.request.GET.get('next') is not None else self.request.POST.get('next')
            resolved_url = resolve(next_url)
            response = redirect(f'{resolved_url.app_names[0]}:{resolved_url.url_name}')
        else:
            response = redirect('mybookwishlist:mylist')

        csrf.get_token(self.request)
        if JWT_data is not None:
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=JWT_data["access"],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
        return response
    def get(self, request, format=None):
        self.request = request
        token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        if (token is not None ) and (verify_access_token(token)):
            return self.response_with_type('S', "이미 로그인 되어있었습니다!")

        return render(request=request, template_name="accounts/login_form.html", context={
            'form' : AuthenticationForm,
        })
    def post(self, request, format=None):
        self.request = request
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            return self.response_with_type('E', "해당하는 유저가 없거나, 패스워드가 일치하지 않습니다.", RESTCode=status.HTTP_404_NOT_FOUND)
        elif not user.is_active:
            return self.response_with_type('E', "이 유저는 현재 활성화 상태가 아닙니다 .", RESTCode=status.HTTP_404_NOT_FOUND)
        JWT_data = get_tokens_for_user(user)
        return self.response_with_type('S', "로그인에 성공하였습니다!", JWT_data=JWT_data)

def logout(request):
    messages.success(request, "로그아웃 되었습니다!")
    response = logout_then_login(request, login_url=f'{settings.FORCE_SCRIPT_NAME}/accounts/login',)
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입을 환영합니다.")
            next_url = request.GET.get('next', '/') or 'mywishlist/mylist'
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
