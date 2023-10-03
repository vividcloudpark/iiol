from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from iiol.authentication import JWTCookieAuthentication
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from .models import MybookWishlist
from .serializers import MybookWishlistSerializer, UserSerializer
from rest_framework.response import Response  
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework import viewsets
from django.db.models import Q
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        """If token was provided, ignore authenticated status."""
        http_auth = request.META.get("HTTP_AUTHORIZATION")
        if http_auth and "Bearer" in http_auth:
            pass

        elif request.COOKIES.get("access_token"):
            pass

        elif not request.user.is_authenticated:
            return self.handle_no_permission()

        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)

class MybookWishListViewSet(JWTLoginRequiredMixin, viewsets.ViewSet):
    basename = 'mylist'
    login_url = f'{settings.FORCE_SCRIPT_NAME}/accounts/login'
    authentication_classes = [
        SessionAuthentication,
        JWTCookieAuthentication,
        JWTAuthentication,
        ]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['bookname', 'isbn13']

    redirect_filed_name = 'redirect_to'
    queryset = MybookWishlist.objects.all()
    serializer_class = MybookWishlistSerializer
    return_json = None
    response_type = "render"
    request = None


    def response_with_type(self, code, msg, RESTCode=200):
        self.set_JSON_header(code, msg)
        if self.response_type == "json":
            return JsonResponse(data=self.return_json, status=RESTCode, json_dumps_params={'ensure_ascii': False})
        else:
            return render(self.request, 'mybookwishlist/mylist.html', {
                    **self.return_json,
                })
        
    def set_JSON_header(self, code, msg):
        self.return_json["status"]["code"] = code
        self.return_json["status"]["msg"] = msg

    def list(self, request):
        self.request = request
        self.return_json = None
        self.return_json = {'status': {'code': "", 'msg': ""}, 'result_data': {}}
        # if request.accepts('application/json'):
        #     self.response_type = 'json'
        qs = MybookWishlist.objects.all()\
            .filter(user=request.user.pk, DELETED=False).order_by("-updated_at").select_related("isbn13")
        if not qs:
            return self.response_with_type('S', '앗, 아직 저장하신 데이터가 없는것 같은데요...', RESTCode=status.HTTP_204_NO_CONTENT)
        serializer = MybookWishlistSerializer(qs, many=True)
        self.return_json['result_data'] = serializer.data
        return self.response_with_type('S', '')

    def create(self, request):
        self.request = request
        self.return_json = None
        self.response_type = 'json'

        request.data['user'] = request.user.pk
        serializer = MybookWishlistSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            self.return_json['result_data'] = serializer.data
            return self.response_with_type('S', '', RESTCode=status.HTTP_201_CREATED)
        else:
            return self.response_with_type('E', serializer.errors, RESTCode=status.HTTP_400_BAD_REQUEST)
    def partial_update(self, request, pk):
        self.request = request
        self.return_json = None
        self.response_type = 'json'
        try:
            item = MybookWishlist.objects.get(isbn13=pk, user=request.user.pk, DELETED=False)
        except MybookWishlist.DoesNotExist:
            return self.response_with_type('E', "내 mybookwishlist에서 해당 도서를 찾을 수 없었습니다. ", RESTCode=status.HTTP_404_NOT_FOUND)
        if request.data['readYn'] :
            request.data['readDate'] = datetime.date.today()
        else:
            request.data['readDate'] = None
        serializer = MybookWishlistSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.return_json['result_data'] = serializer.data
            return self.response_with_type('S', '정보 수정에 성공했습니다.', RESTCode=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return self.response_with_type('E', serializer.errors, RESTCode=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        self.request = request
        self.return_json = None
        self.response_type = 'json'
        try:
            item = MybookWishlist.objects.get(isbn13=pk, user=request.user.pk, DELETED=False)
        except MybookWishlist.DoesNotExist:
            return self.response_with_type('E', "해당 도서를 찾을 수 없었습니다. \n 이미 삭제되었는지 확인하십시오. ", RESTCode=status.HTTP_404_NOT_FOUND)
        serializer = MybookWishlistSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.return_json['result_data'] = serializer.data
            return self.response_with_type('S', '삭제에 성공하였습니다.', RESTCode=status.HTTP_202_ACCEPTED)
        return self.response_with_type('E', '삭제에 실패하였습니다.', RESTCode=status.HTTP_406_NOT_ACCEPTABLE)

