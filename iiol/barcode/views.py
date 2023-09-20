from rest_framework.views import APIView
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from .models import Barcode
from library.models import Library
from books.models import Book
from .serializers import BarcodeSerializer
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils import timezone

import cv2
import numpy as np
import json
import os
from datetime import datetime, timedelta
from utils.library_api import LibraryApi

CACHE_TTL = getattr(settings, 'CACHE_TTL')


class BarcodeViewSet(APIView):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer
    # parser_classes = (MultiPartParser, FormParser)
    bardet = cv2.barcode_BarcodeDetector()
    LibAPI = LibraryApi()
    BOOKINFO_JSON = None
    LIBRARY_INFO_JSON = None
    libcode_list = []
    ISBN = None

    def post(self, request, *args, **kwargs):
        try:
            if request.POST['region_code']:
                self.region_code = request.POST['region_code'].strip()
            if request.POST['ISBN_string']:
                self.ISBN = request.POST['ISBN_string']
            elif request.FILES['barcode_photo']:
                barcode_photo = request.FILES['barcode_photo'].read()
                img = bytearray(barcode_photo)
                numbyarray = np.asarray(img, dtype=np.uint8)
                img = cv2.imdecode(buf=numbyarray, flags=cv2.IMREAD_COLOR)
                self.ISBN = self.bardet.detectAndDecode(
                    img)[0]
        except:
            return JsonResponse(data={'barcode_data': None}, status=400)

        if self.ISBN:
            print(self.ISBN, self.region_code)
            
            self.book_info()
            self.get_library_list(self.region_code)
            self.get_book_availablity_by_libcode()
                          
            returning_data = {'request_data': {'ISBN': self.ISBN, 'region_code': self.region_code},
                              'result': {'book_detail': self.BOOKINFO_JSON,
                                         'library_info': self.LIBRARY_INFO_JSON}}

            return render(request, 'barcode/detect_result.html', {
                'request_data': {'ISBN': self.ISBN, 'region_code': self.region_code},
                'book_detail': self.BOOKINFO_JSON,
                'library_info': self.LIBRARY_INFO_JSON,
            })

            # return JsonResponse(data=returning_data, json_dumps_params={'ensure_ascii': False}, status=200)
        else:
            return JsonResponse(data={'barcode_data': None}, status=404)

    def get_library_list(self, region_code):
        LIBRARY_INFO_JSON = cache.get(f'Library_in_{region_code}')
        if LIBRARY_INFO_JSON is None: # 캐시조회실패 
            try:
                librarys = Library.objects.get(small_region_code=region_code)
            except Library.DoesNotExist:
                lib_response = self.LibAPI.search_libcode_by_region(region_code = region_code)# API를 통해 해당 지역의 Libary 호출 후 
                self.LIBRARY_INFO_JSON = {}
                [ self.LIBRARY_INFO_JSON.update({ lib['libCode'] : lib}) for lib in lib_response ]
                cache.set(f'Library_in_{region_code}', json.dumps(self.LIBRARY_INFO_JSON), CACHE_TTL)
                
                # 해당 Libary 정보 DB && Cache하는 Celery Task 추가 
                # 해당 저장로직은 API 함수에 포함
            # finally: #DB조회성공
                # libcode_list = librarys.values_list(libcode, flat=True)
                # LIBRARY_INFO_JSON = librarys.values_list(named=True)
                
                # Cache하는 Celery Task 추가
        else:
            self.LIBRARY_INFO_JSON = json.loads(LIBRARY_INFO_JSON)
        self.libcode_list = list(self.LIBRARY_INFO_JSON.keys())
        return

    def book_info(self):
        #일단은 ISBN13이 들어올것이라고 기대, ISBN10일경우도 추후 만들기
        BOOKINFO_JSON = cache.get(f'ISBN13_{self.ISBN}')
        libcode_list = []
        if BOOKINFO_JSON is None: # 캐시조회실패 
            try:
                Books = Book.objects.get(isbn13=self.ISBN)
            except Book.DoesNotExist:
                book_response = self.LibAPI.search_book_detail_by_ISBN(self.ISBN)
                self.BOOKINFO_JSON = [book['book'] for book in book_response['detail']]
                cache.set(f'ISBN13_{self.ISBN}', json.dumps(BOOKINFO_JSON), CACHE_TTL)
                
                # 해당 Libary 정보 DB && Cache하는 Celery Task 추가 
                # 해당 저장로직은 API 함수에 포함
            # finally: #DB조회성공
                # libcode_list = librarys.values_list(libcode, flat=True)
                # LIBRARY_INFO_JSON = librarys.values_list(named=True)
                
                # Cache하는 Celery Task 추가
        else:
            self.BOOKINFO_JSON = json.loads(BOOKINFO_JSON)
        return

    def get_book_availablity_by_libcode(self):
        for libcode in self.libcode_list:
                book_availablity_cache = cache.get(f'{libcode}_{self.ISBN}')
                if book_availablity_cache is not None:
                    self.LIBRARY_INFO_JSON[libcode]['hasBook'] = book_availablity_cache[0]
                    self.LIBRARY_INFO_JSON[libcode]['loanAvailable'] = book_availablity_cache[1]
                else:
                    book_availablity = self.LibAPI.search_book_availability_of_lib_by_ISBN(ISBN=self.ISBN,lib_code=libcode)
                    self.LIBRARY_INFO_JSON[libcode]['hasBook'] = book_availablity['result']['hasBook']
                    self.LIBRARY_INFO_JSON[libcode]['loanAvailable'] = book_availablity['result']['loanAvailable']

                    book_availablity_cache = (book_availablity['result']['hasBook'], book_availablity['result']['loanAvailable'])
                    cache.set(f'{libcode}_{self.ISBN}', book_availablity_cache, self.get_remain_sec_of_today())
        return

    def get_remain_sec_of_today(self):
        now = datetime.now()
        midnight = datetime(now.year, now.month, now.day, 23, 59, 59)
        time_remain = midnight-now
        return time_remain.total_seconds()

def get_region_json_with_cache():
    region_json = cache.get('region_json')
    if region_json is None:
        file_path = os.path.join(settings.STATIC_ROOT, 'json/region_code.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            region_json = json.load(f)
        cache.set('region_json', region_json, CACHE_TTL)
    return region_json

@cache_page(CACHE_TTL, key_prefix='barcode:html')
def detect(request):
    region_json = get_region_json_with_cache()
    return render(request, 'barcode/detect.html', {
        'region_json': region_json,
    })

def retrieve_region_code(request):
    region_json = get_region_json_with_cache()
    return JsonResponse(data=region_json, json_dumps_params={'ensure_ascii': False}, status=200, safe=False)

# 9788956748535
