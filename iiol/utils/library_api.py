import os
import json
import requests
from os.path import abspath, dirname
from dotenv import load_dotenv
BASE_DIR = dirname(dirname(abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)


class CallLibraryApi():
    BASIC_API_URL = 'http://data4library.kr/api/'
    LIBRARY_API_KEY = os.environ.get('LIBRARY_API_KEY')
    SERVICE_NAME = ''

    def is_there_book_in_my_region(self, ISBN=None, region=None, subregion=None):
        if ISBN == None or region == None:
            return False

        lib_code_list = self.search_libcode_by_region(
            region=11, subregion=subregion)

        success_list = []
        for lib in lib_code_list:
            res = self.search_book_availability_of_lib_by_ISBN(
                lib['lib_code'], ISBN)
            lib['hasBook'] = res['result']['hasBook']
            lib['loanAvailable'] = res['result']['loanAvailable']
            print(res)
            success_list.append(lib)

        return success_list

    def search_libcode_by_region(self, region=11, subregion=None):
        self.SERVICE_NAME = 'libSrch'
        request_params = {}
        request_params['region'] = str(region)
        request_params['dtl_region'] = str(subregion)

        response = self.request(request_params)
        lib_code_list = []
        if response['numFound'] != 0:
            for lib in response['libs']:
                lib_dict = {
                    'lib_code': lib['lib']['libCode'], 'lib_name': lib['lib']['libName']}
                lib_code_list.append(lib_dict)

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


api = CallLibraryApi()
# 9788956748535 -> AWS
# 9788950982256 -> 다크호스

res = api.is_there_book_in_my_region(
    region=11, subregion=11190, ISBN=9788950982256)
# res = api.search_libcode_by_region(region=11, subregion=11190)
# res = api.search_book_detail_by_ISBN(9788950982874)
# res = api.search_book_availability_of_lib_by_ISBN(111111, 9788950982874)
print(json.dumps(res, indent=4, ensure_ascii=False))
