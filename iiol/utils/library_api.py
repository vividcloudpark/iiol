import os
import json
import logging
import requests
from os.path import abspath, dirname
from dotenv import load_dotenv

# 기본 경로 설정 및 환경 변수(.env) 로드
BASE_DIR = dirname(dirname(abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

# 표준 로거 생성
logger = logging.getLogger(__name__)


class LibraryApi:
    """
    도서관정보나루 OpenAPI 연동을 담당하는 API Wrapper 클래스입니다.
    """

    def __init__(self):
        self.BASIC_API_URL = 'http://data4library.kr/api/'
        self.LIBRARY_API_KEY = os.environ.get('LIBRARY_API_KEY')
        self.SERVICE_NAME = ''

    def search_libcode_by_region(self, region_code=None):
        """
        [1. 지역내 도서관 코드 조회 API]
        특정 지역 코드(5자리)를 기반으로 속해 있는 도서관 코드 목록을 검색합니다.
        """
        self.SERVICE_NAME = 'libSrch'
        request_params = {
            'region': str(region_code)[0:2],
            'dtl_region': str(region_code),
            'pageSize': 20
        }
        
        lib_response = self.request(request_params)
        
        try:
            if lib_response and lib_response.get('numFound', 0) != 0:
                return [lib_item['lib'] for lib_item in lib_response.get('libs', [])]
        except Exception as e:
            logger.warning(f"Failed to parse libraries list: {e}")
        return []

    def search_book_detail_by_ISBN(self, ISBN):
        """
        [6. 도서상세조회 API]
        책의 13자리 ISBN을 기반으로 대출 통계 및 도서 정보를 상세히 조회합니다.
        """
        self.SERVICE_NAME = 'srchDtlList'
        request_params = {
            'isbn13': str(ISBN),
            'loaninfoYN': 'Y'
        }
        return self.request(request_params)

    def search_book_availability_of_lib_by_ISBN(self, lib_code=None, ISBN=None):
        """
        [11. 도서관별 도서 소장여부 및 대출가능여부 조회 API]
        특정 도서관 코드와 ISBN을 대조하여 책의 소장 여부와 대출 가능 상태를 실시간 조회합니다.
        """
        self.SERVICE_NAME = 'bookExist'
        request_params = {
            'libCode': str(lib_code),
            'isbn13': str(ISBN)
        }
        return self.request(request_params)

    def request(self, request_params):
        """
        도서관정보나루 OpenAPI에 실제 HTTP GET 요청을 날리고 응답 결과를 반환하는 핵심 공통 메서드입니다.
        요청 시작과 응답의 성공/실패 여부를 표준 로그 레벨에 맞게 콘솔로 로깅합니다.
        """
        # API 인증 키를 포함한 엔드포인트 URL 구성 (API Key 누락 방지)
        FINAL_URL = self.BASIC_API_URL + self.SERVICE_NAME + \
            '?authKey=' + (self.LIBRARY_API_KEY or '')

        # 요청 파라미터 직렬화 (None 문자열 제외)
        for key, value in request_params.items():
            if value != 'None' and value is not None:
                FINAL_URL += f'&{key}={value}'

        FINAL_URL += '&format=json'

        # 외부 API 요청 로그 남기기 (보안을 위해 API Key 노출을 배제한 정보만 로그로 기록)
        logger.info(f"[API Request] Service: {self.SERVICE_NAME} | Params: {request_params}")
        
        try:
            res = requests.get(FINAL_URL, timeout=10)  # 타임아웃 10초 설정
            
            # HTTP 응답 상태 코드 검증
            if res.status_code != 200:
                logger.error(f"[API Error] Service: {self.SERVICE_NAME} failed with HTTP Status Code: {res.status_code}")
                return {}
            
            # JSON 응답 데이터 딕셔너리 안전 파싱
            response_data = res.json()
            if 'response' in response_data:
                logger.info(f"[API Response Success] Service: {self.SERVICE_NAME}")
                return response_data['response']
            else:
                logger.warning(f"[API Warning] Service: {self.SERVICE_NAME} response did not contain 'response' key: {response_data}")
                return {}
                
        except requests.exceptions.RequestException as e:
            # 네트워크 타임아웃, DNS 확인 실패 등 네트워크 결함 로깅
            logger.error(f"[API Connection Failed] Service: {self.SERVICE_NAME} | Error: {e}")
            return {}
        except ValueError as e:
            # 반환된 데이터가 JSON 포맷이 아닐 때 디코딩 에러 로깅
            logger.error(f"[API JSON Decode Failed] Service: {self.SERVICE_NAME} | Error: {e}")
            return {}
