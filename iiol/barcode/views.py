from rest_framework.views import APIView
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from .models import Barcode
from .serializers import BarcodeSerializer
from django.conf import settings



import cv2
import numpy as np
import json
import os
from utils.library_api import LibraryApi


class BarcodeViewSet(APIView):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer
    # parser_classes = (MultiPartParser, FormParser)
    bardet = cv2.barcode_BarcodeDetector()

    def post(self, request, *args, **kwargs):
        try:
            if request.POST['region_code']:
                region_code = request.POST['region_code'].strip()
            if request.POST['ISBN_string']:
                ISBN = request.POST['ISBN_string']
            elif request.FILES['barcode_photo']:
                barcode_photo = request.FILES['barcode_photo'].read()
                img = bytearray(barcode_photo)
                numbyarray = np.asarray(img, dtype=np.uint8)
                img = cv2.imdecode(buf=numbyarray, flags=cv2.IMREAD_COLOR)
                ISBN = self.bardet.detectAndDecode(
                    img)[0]
        except:
            return JsonResponse(data={'barcode_data': None}, status=400)

        if ISBN:
            api = LibraryApi()
            print(ISBN,region_code)
            book_detail, library_info = api.is_there_book_in_my_region(
                subregion=region_code, ISBN=ISBN)
            returning_data = {'barcode_data': ISBN,
                           'result' : {'book_detail' : book_detail,
                                       'library_info' : library_info}}
            return JsonResponse(data=returning_data, json_dumps_params={'ensure_ascii': False}, status=200)
        else:
            return JsonResponse(data={'barcode_data': None}, status=404)


def detect(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'json/region_code.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        region_json = json.load(f)
    return render(request, 'barcode/detect.html', {
        'region_json' :region_json,
    })

def retrieve_region_code(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'json/region_code.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        region_json = json.load(f)
    return JsonResponse(data=region_json, json_dumps_params={'ensure_ascii': False}, status=200, safe=False)

# 9788956748535
