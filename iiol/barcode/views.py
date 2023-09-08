from rest_framework.views import APIView
from django.http import JsonResponse, StreamingHttpResponse
from datetime import datetime
import time
import os
from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Barcode
from .serializers import BarcodeSerializer
# from rest_framework.parsers import MultiPartParser, FormParser


import cv2
import numpy as np
from pyzbar.pyzbar import decode


class BarcodeViewSet(APIView):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer
    # parser_classes = (MultiPartParser, FormParser)
    bardet = cv2.barcode_BarcodeDetector()

    def post(self, request, *args, **kwargs):
        barcode_photo = request.FILES['barcode_photo'].read()
        img = bytearray(barcode_photo)
        numbyarray = np.asarray(img, dtype=np.uint8)
        img = cv2.imdecode(buf=numbyarray, flags=cv2.IMREAD_COLOR)
        returned_value = self.bardet.detectAndDecode(
            img)

        print(returned_value[0])
        if returned_value[0]:

            return JsonResponse(data={'barcode_data': returned_value[0]})
        else:
            return JsonResponse(data={'barcode_data': None})


def detect(request):
    return render(request, 'barcode/detect.html', {})


# 9788956748535
