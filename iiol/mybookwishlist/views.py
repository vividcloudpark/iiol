from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MybookWishlist
from books.models import Book
from .serializers import MybookWishlistSerializer
from rest_framework.response import Response  
from django.conf import settings
from rest_framework import status
from django.shortcuts import redirect, reverse

User=settings.AUTH_USER_MODEL


class MybookWishListView(LoginRequiredMixin, APIView):
    login_url = f'{settings.FORCE_SCRIPT_NAME}/accounts/login'
    redirect_filed_name = 'redirect_to'
    queryset = MybookWishlist.objects.all()
    serializer_class = MybookWishlistSerializer
    return_json = None
    response_type = "render"
    request = None
    

    def __init__(self):
        self.set_default_structure()

    def set_default_structure(self):
        self.return_json = {'status' : {'code' : "", 'msg' : ""},
                    'result_data' : {}}  

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

    def get(self, request, format=None):
        self.request = request
        if request.content_type == 'application/json':
            self.type = 'json'
        qs = MybookWishlist.objects\
            .filter(user=request.user)
        serializer = MybookWishlistSerializer(qs, many=True)
        self.return_json['result_data'] = serializer.data
        return self.response_with_type('S', '')

    def post(self, request):
        self.request = request
        if request.content_type == 'application/json':
            self.type = 'json'
        serializer = MybookWishlistSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            self.return_json['result_data'] = serializer.data
            return self.response_with_type('S', '', status=status.HTTP_201_CREATED)
        else:
            return self.response_with_type('E', serializer.errors, status=status.HTTP_400_BAD_REQUEST)