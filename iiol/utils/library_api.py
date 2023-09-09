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

    # [6.도서상세조회 API] +  # [11.도서관별 도서 소장여부 및 대출가능여부 조회]

    def is_there_book_in_my_region(self, ISBN=None, region=None, subregion=None):
        if ISBN == None or subregion == None:
            return False
        book_detail = self.search_book_detail_by_ISBN(ISBN)
        print(json.dumps(book_detail, indent=4, ensure_ascii=False))
        lib_code_list = self.search_libcode_by_region(
            subregion=subregion)

        lib_available_list = []
        for lib in lib_code_list:
            res = self.search_book_availability_of_lib_by_ISBN(
                lib['lib_code'], ISBN)
            if res['result']['hasBook'] != 'Y':
                continue
            lib['hasBook'] = res['result']['hasBook']
            lib['loanAvailable'] = res['result']['loanAvailable']
            lib_available_list.append(lib)
        return book_detail, lib_available_list

    #[1. 지역내 도서관 코드 조회]
    def search_libcode_by_region(self, region=11, subregion=None):
        self.SERVICE_NAME = 'libSrch'
        request_params = {}
        request_params['region'] = str(region)
        request_params['dtl_region'] = str(subregion)
        request_params['pageSize'] = 20
        lib_response = self.request(request_params)
        lib_code_list = []

        try :
            if lib_response['numFound'] != 0:
                for lib in lib_response['libs']:
                    lib_dict = {
                        'lib_code': lib['lib']['libCode'], 'lib_name': lib['lib']['libName']}
                    lib_code_list.append(lib_dict)
        except:
            pass

        return lib_code_list

    # [6.도서상세조회 API]
    def search_book_detail_by_ISBN(self, ISBN):
        self.SERVICE_NAME = 'srchDtlList'
        request_params = {}
        request_params['isbn13'] = str(ISBN)
        request_params['loaninfoYN'] = 'Y'

        return self.request(request_params)

    # [11.도서관별 도서 소장여부 및 대출가능여부 조회]
    def search_book_availability_of_lib_by_ISBN(self, lib_code,  ISBN):

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
