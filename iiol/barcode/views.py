from rest_framework.views import APIView
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from .models import Barcode
from library.models import Library, SmallRegion, BigRegion
from books.models import Book
from .serializers import BarcodeSerializer
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.forms.models import model_to_dict
from books.serializers import BookSerializer
from library.serializers import LibrarySerializer
import cv2
import numpy as np
import json
import os
from datetime import datetime, timedelta
from utils.library_api import LibraryApi

from .tasks import save_book_on_DB

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
    return_json = None
    region_code = None

    def set_JSON_header(self, code, msg):
        self.return_json["status"]["code"] = code
        self.return_json["status"]["msg"] = msg


    def post(self, request, *args, **kwargs):
        self.return_json = {'status' : {'code' : "", 'msg' : ""},
                            'request_data': {'ISBN': self.ISBN, 'region_code': self.region_code},
                            'result_data' : {}}  
        
        try:
            if request.POST['region_code']:
                self.region_code = request.POST['region_code'].strip()
            if request.POST['ISBN_string']:
                self.ISBN = request.POST['ISBN_string'].strip()
                if len(self.ISBN) != 13:
                    self.set_JSON_header('E', '13자리의 ISBN을 입력하십시오.')
            elif request.FILES['barcode_photo']:
                barcode_photo = request.FILES['barcode_photo'].read()
                img = bytearray(barcode_photo)
                numbyarray = np.asarray(img, dtype=np.uint8)
                img = cv2.imdecode(buf=numbyarray, flags=cv2.IMREAD_COLOR)
                for detect__string in self.bardet.detectAndDecode(img):
                    if len(detect__string) == 13:
                        self.ISBN = detect__string
                        break;
        except:
            self.set_JSON_header('E', 'ISBN을 추출하던 중 오류가 발생헀습니다. 직접 입력해보십시오.')
            return render(request, 'barcode/detect_result.html', {
                    **self.return_json,
                })
            # return JsonResponse(data=self.return_json, status=404, json_dumps_params={'ensure_ascii': False})
        

        if self.ISBN is None:
            self.set_JSON_header('E', 'ISBN을 찾을 수 없었습니다. 13자리의 ISBN을 직접 입력해보십시오.')
            return render(request, 'barcode/detect_result.html', {
                    **self.return_json,
                })
            # return JsonResponse(data=self.return_json, status=404, json_dumps_params={'ensure_ascii': False}, safe=False)
        else:    
            self.return_json['request_data'] = {'ISBN': self.ISBN, 'region_code': self.region_code} 
            self.return_json['result_data'] ={}

            SUCESS, MSG = self.book_info()

            if not SUCESS:
                self.set_JSON_header('E', f'{self.ISBN} : 해당하는 ISBN에 일치하는 도서정보가 없습니다.')
                self.return_json['status']['msg'] = f"{self.return_json['status']['msg']} \n MSG" 
                return render(request, 'barcode/detect_result.html', {
                    **self.return_json,
                })
                # return JsonResponse(data=self.return_json, status=404, json_dumps_params={'ensure_ascii': False})

            self.get_library_list(self.region_code)
            self.get_book_availablity_by_libcode()


            self.return_json['result_data']['book_detail'] = self.BOOKINFO_JSON
            self.return_json['result_data']['library_info'] = self.LIBRARY_INFO_JSON
            
            self.set_JSON_header('S', MSG)

            return render(request, 'barcode/detect_result.html', {
                **self.return_json,
            })

            # return JsonResponse(data=self.return_json, json_dumps_params={'ensure_ascii': False}, status=200)
    

    def get_library_list(self, region_code):
        LIBRARY_INFO_JSON = cache.get(f'Library_in_{region_code}')
        # LIBRARY_INFO_JSON = None
        if LIBRARY_INFO_JSON is None:  # 캐시조회실패
            try:
                queryset = Library.objects.filter(small_region_code=region_code)
                if queryset.exists():
                    serialized_library = LibrarySerializer(queryset, many=True).data
                    self.LIBRARY_INFO_JSON = {}
                    [self.LIBRARY_INFO_JSON.update({lib['libCode']: dict(lib)}) for lib in serialized_library]
                else:
                    raise
            except:
                lib_response = self.LibAPI.search_libcode_by_region(
                    region_code=region_code)  # API를 통해 해당 지역의 Libary 호출 후
                self.LIBRARY_INFO_JSON = {}
                [self.LIBRARY_INFO_JSON.update(
                    {lib['libCode']: lib}) for lib in lib_response]
                cache.set(f'Library_in_{region_code}', json.dumps(
                    self.LIBRARY_INFO_JSON), CACHE_TTL)
                
                for lib in lib_response:
                    lib.update({'big_region_code' : region_code[0:2]})
                    lib.update({'small_region_code' : region_code})

                BigRegion_obj, created = BigRegion.objects.get_or_create(big_region_code=region_code[0:2])
                SmallRegion.objects.get_or_create(big_region_code=BigRegion_obj, small_region_code=region_code)

                serializer=LibrarySerializer(data=lib_response, many=True)

                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)

      
        else:
            self.LIBRARY_INFO_JSON = json.loads(LIBRARY_INFO_JSON)
        self.libcode_list = list(self.LIBRARY_INFO_JSON.keys())
        return

    def book_info(self):
        msg = None
        # 일단은 ISBN13이 들어올것이라고 기대, ISBN10일경우도 추후 만들기
        BOOKINFO_JSON = cache.get(f'ISBN13_{self.ISBN}')
        # BOOKINFO_JSON = None
        if BOOKINFO_JSON is not None: 
            self.BOOKINFO_JSON=json.loads(BOOKINFO_JSON)
        else: # 캐시조회실패
            queryset = Book.objects.filter(isbn13=self.ISBN)

            if queryset.exists(): #DB에 있었음!
                serialized_book = BookSerializer(queryset, many=True).data
                self.BOOKINFO_JSON = [dict(book) for book in serialized_book]
                cache.set(f'ISBN13_{self.ISBN}', json.dumps(
                    self.BOOKINFO_JSON), CACHE_TTL)
            else: # API로 최초조회 -> 당신이 이올에서 처음 이책을 발견했어요! 
                book_response=self.LibAPI.search_book_detail_by_ISBN(
                    self.ISBN)
                try:
                    self.BOOKINFO_JSON=[book['book']
                                        for book in book_response['detail']]
                    cache.set(f'ISBN13_{self.ISBN}', json.dumps(
                        self.BOOKINFO_JSON), CACHE_TTL)

                    serializer=BookSerializer(data=self.BOOKINFO_JSON[0])
                    if serializer.is_valid():
                        serializer.save()
                    msg = "축하합니다! IIOL에서 이 책을 처음 검색하였습니다!"
                except:
                    return False, book_response
        return True, msg
                    

                
        

    def get_book_availablity_by_libcode(self):
        for libcode in self.libcode_list:
            book_availablity_cache=cache.get(f'{libcode}_{self.ISBN}')
            if book_availablity_cache is not None:
                self.LIBRARY_INFO_JSON[libcode]['hasBook']=book_availablity_cache[0]
                self.LIBRARY_INFO_JSON[libcode]['loanAvailable']=book_availablity_cache[1]
            else:
                book_availablity=self.LibAPI.search_book_availability_of_lib_by_ISBN(
                    ISBN=self.ISBN, lib_code=libcode)
                self.LIBRARY_INFO_JSON[libcode]['hasBook']=book_availablity['result']['hasBook']
                self.LIBRARY_INFO_JSON[libcode]['loanAvailable']=book_availablity['result']['loanAvailable']

                book_availablity_cache=(
                    book_availablity['result']['hasBook'], book_availablity['result']['loanAvailable'])
                cache.set(f'{libcode}_{self.ISBN}',
                          book_availablity_cache, self.get_remain_sec_of_today())
        return

    def get_remain_sec_of_today(self):
        now=datetime.now()
        midnight=datetime(now.year, now.month, now.day, 23, 59, 59)
        time_remain=midnight-now
        return time_remain.total_seconds()


def get_region_json_with_cache():
    region_json=cache.get('region_json')
    if region_json is None:
        file_path=os.path.join(settings.STATIC_ROOT, 'json/region_code.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            region_json=json.load(f)
        cache.set('region_json', region_json, CACHE_TTL)
    return region_json


# @ cache_page(60, key_prefix='barcode:html')
def detect(request):
    region_json=get_region_json_with_cache()
    return render(request, 'barcode/detect.html', {
        'region_json': region_json,
    })


def retrieve_region_code(request):
    region_json=get_region_json_with_cache()
    return JsonResponse(data=region_json, json_dumps_params={'ensure_ascii': False}, status=200, safe=False)

# 9788956748535
