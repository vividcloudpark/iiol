from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MybookWishlist
from .serializers import MybookWishlistSerializer
from rest_framework.response import Response  
from django.conf import settings


User=settings.AUTH_USER_MODEL


class MybookWishListViewSet(LoginRequiredMixin, APIView):
    login_url = '/login/'
    redirect_filed_name = 'redirect_to'
    queryset = MybookWishlist.objects.all()
    serializer_class = MybookWishlistSerializer

    def get(self, request, format=None):
        qs = MybookWishlist.objects.filter(user=request.user)
        serializer = MybookWishlistSerializer(qs, many=True)
        return Response(serializer.data)
