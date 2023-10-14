from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, BlacklistMixin
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from rest_framework_simplejwt.backends import TokenBackend
from django.contrib import messages
import jwt


def enforce_csrf(request):
    """
    Enforce CSRF validation.
    """
    check = CSRFCheck(request)
    # populates request.META['CSRF_COOKIE'], which is used in process_view()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        # CSRF failed, bail with explicit error message
        raise exceptions.PermissionDenied("CSRF Failed: %s" % reason)


class JWTCookieAuthentication(JWTAuthentication, BlacklistMixin):
    def authenticate(self, request):
        header = self.get_header(request)
        raw_token = None
        if header is not None:
            raw_token = self.get_raw_token(header)
        elif request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_COOKIE"]):
            try:
                refresh_token = RefreshToken(request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_COOKIE"]))
                refresh_token.verify() #BlacklistMixin이 있으므로, blacklist 검증까지 수행
                raw_token = bytes(str(refresh_token.access_token), "utf-8")
            except Exception as e:
                print("유효하지 않은 refresh token : ", e)
                return None
        elif request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]):
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])

        if raw_token is None:
            return None  # 세션인증으로 넘어감

        
        validated_token = self.get_validated_token(raw_token)  
        #raw_token은 모두 byte형식임
        # get_validate_token은 settings에 있는 accesstoken만 검증함
        try:
            user = self.get_user(validated_token)
            if not user.is_active:
                raise
        except Exception as e:
            print(e)
            validated_token.blacklist()
            return None

        enforce_csrf(request)
        return user, validated_token


class AuthenticationManager(BlacklistMixin):
    @staticmethod
    def issue_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @staticmethod
    def verify_token(token):
        try:
            token.check_blacklist()
            return token
        except Exception as e:
            return None

    @staticmethod
    def blacklisting_tokens(request):
        header = request.META.get(settings.SIMPLE_JWT["AUTH_HEADER_NAME"])
        raw_token_list = []
        if header is not None:
            raw_token_list.append(self.get_raw_token(header))
        elif request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]):
            raw_token_list.append(request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]))
        for raw_token in raw_token_list:
            validated_token = self.get_validated_token(raw_token)
            validated_token.blacklist()

        if request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_COOKIE"]):
            try:
                RefreshToken(request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_COOKIE"])).blacklist()
            except:
                pass

    @staticmethod
    def is_logined(request):
        if request.user.is_authenticated:  # 세션인증시
            return True

        if JWTCookieAuthentication().authenticate(request) is not None:
            return True

        return False


class JWTLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        """If token was provided, ignore authenticated status."""
        header = request.META.get(settings.SIMPLE_JWT["AUTH_HEADER_NAME"])
        if header and settings.SIMPLE_JWT["AUTH_HEADER_TYPES"] in header:
            pass

        elif request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_COOKIE"]) or request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]):
            pass

        elif not request.user.is_authenticated:
            messages.info(request, "로그인이 되어있지 않네요.. :( \n 로그인을 하시면 IIOL의 모든 기능을 이용할 수 있습니다.")
            return self.handle_no_permission()

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
