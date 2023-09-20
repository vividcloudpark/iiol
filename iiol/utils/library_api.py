import os
import json
import requests
from os.path import abspath, dirname
from dotenv import load_dotenv
BASE_DIR = dirname(dirname(abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)


class LibraryApi:
    def __init__(self):
        self.BASIC_API_URL = 'http://data4library.kr/api/'
        self.LIBRARY_API_KEY = os.environ.get('LIBRARY_API_KEY')
        self.SERVICE_NAME = ''

   
    def search_libcode_by_region(self, region_code=None):
        # [1. 지역내 도서관 코드 조회]
        self.SERVICE_NAME = 'libSrch'
        request_params = {}
        request_params['region'] = str(region_code)[0:2]
        request_params['dtl_region'] = str(region_code)
        request_params['pageSize'] = 20
        lib_response = self.request(request_params)
        
        try :
            if lib_response['numFound'] != 0:
                return [lib_item['lib'] for lib_item in lib_response['libs']]
        except:
            return []       

    def search_book_detail_by_ISBN(self, ISBN):
        # [6.도서상세조회 API]
        self.SERVICE_NAME = 'srchDtlList'
        request_params = {}
        request_params['isbn13'] = str(ISBN)
        request_params['loaninfoYN'] = 'Y'

        return self.request(request_params)


    def search_book_availability_of_lib_by_ISBN(self, lib_code=None,  ISBN=None):
        # [11.도서관별 도서 소장여부 및 대출가능여부 조회]
        self.SERVICE_NAME = 'bookExist'
        request_params = {}
        request_params['libCode'] = str(lib_code)
        request_params['isbn13'] = str(ISBN)

        return self.request(request_params)

    def request(self, request_params):
        FINAL_URL = self.BASIC_API_URL + self.SERVICE_NAME + \
            '?authKey=' + self.LIBRARY_API_KEY

        for key, value in request_params.items():
            if value != 'None':
                FINAL_URL += f'&{key}={value}'

        FINAL_URL += '&format=json'

        print(f'API CALLED ->>> {self.SERVICE_NAME}')
        res = requests.get(FINAL_URL)
        return res.json()['response']


# api = LibraryApi()
# # 9788956748535 -> AWS
# # 9788950982256 -> 다크호스
#
# res = api.is_there_book_in_my_region(
#     region=11, subregion=11190, ISBN=9788950982256)
# # res = api.search_libcode_by_region(region=11, subregion=11190)
# # res = api.search_book_detail_by_ISBN(9788950982874)
# # res = api.search_book_availability_of_lib_by_ISBN(111111, 9788950982874)
# print(json.dumps(res, indent=4, ensure_ascii=False))
