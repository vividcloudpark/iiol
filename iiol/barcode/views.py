from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import render
from .models import Barcode
from library.models import Library, SmallRegion, BigRegion
from books.models import Book
from django.conf import settings
from django.core.cache import cache
import logging
from django.views.decorators.cache import cache_page
from books.serializers import BookSerializer
from library.serializers import LibrarySerializer
from .serializers import BarcodeSerializer
import json
import os
from utils.library_api import LibraryApi
from utils.general_function import get_ipaddress, get_remain_sec_of_today
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from .tasks import save_book_on_DB

CACHE_TTL = getattr(settings, "CACHE_TTL")
logger = logging.getLogger(__name__)

EMPTY_ISBN = "0000000000000"


class BarcodeView(APIView):
    """
    바코드(ISBN) 혹은 도서 사진을 기반으로, 
    해당 도서의 메타데이터와 선택된 지역(small_region_code) 내 도서관들의 
    소장 여부 및 대출 가능 여부를 조회하여 반환해주는 통합 API View입니다.
    """
    permission_classes = [AllowAny]
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer
    LibAPI = LibraryApi()
    BOOKINFO_JSON = None
    LIBRARY_INFO_JSON = None
    libcode_list = []
    ISBN = None
    return_json = None
    region_code = None
    response_type = "render"
    request = None

    def response_with_type(self, code, msg, RESTCode=status.HTTP_200_OK):
        """
        API 요청 결과를 JSON 혹은 HTML 형태로 일관성 있게 반환해주는 헬퍼 메서드입니다.
        검색 이력을 DB(Barcode 객체)에 저장(로깅)하는 역할도 함께 수행합니다.
        
        Args:
            code (str): 'S' (성공) 혹은 'E', 'W' (에러/경고) 등의 커스텀 상태 코드
            msg (str): 반환할 메시지
            RESTCode (int): 최종적으로 응답에 실어보낼 HTTP 상태 코드
        """
        msg = "" if msg == None else msg
        user = self.request.user.pk if self.request.user.is_authenticated else None
        if self.ISBN == None:
            self.ISBN = EMPTY_ISBN

        input_data = {
            "isbn13": self.ISBN,
            "small_region_code": self.region_code,
            "statusCode": code,
            "statusMsg": msg,
            "user": user,
            "client": settings.SERVER_ALIAS,
            "ipaddress": get_ipaddress(self.request),
        }
        serializer = BarcodeSerializer(data=input_data)

        if serializer.is_valid():
            saved = serializer.save()
            self.return_json["status"]["searchPk"] = saved.pk
        else:
            code = "W"
            msg = serializer.errors

        self.set_JSON_header(code, msg)
        
        # 클라이언트가 JSON을 명시적으로 요구하거나, Content-Type이 JSON인 경우 JSON 반환
        if "application/json" in self.request.META.get("HTTP_ACCEPT", "") or self.request.content_type == "application/json":
            return JsonResponse(
                data=self.return_json,
                status=RESTCode,
                json_dumps_params={"ensure_ascii": False},
            )
        else:
            return render(
                self.request,
                "barcode/detect_result.html",
                {
                    **self.return_json,
                },
                None,
                RESTCode,
            )

    def set_JSON_header(self, code, msg):
        if (
            self.return_json["status"]["code"] == "" or code == "W"
        ):  # W로 에러상태를 이미 저장헀을때 반영
            self.return_json["status"]["code"] = code

        if code == "S":
            self.return_json["status"]["msg"] = msg
        else:
            self.return_json["status"]["msg"] = self.return_json["status"]["msg"] + str(
                msg
            )

    @extend_schema(
        tags=["barcode"],
        summary="ISBN13을 기반으로 한 바코드검색",
        parameters=[
            OpenApiParameter(
                name="small_region_code",
                type=str,
                description="5자리의 도서관 지역코드",
                required=True,
            ),
            OpenApiParameter(
                name="isbn13",
                type=str,
                description="13자리의 ISBN13 바코드. 사진이 있을경우 생략가능",
                required=True,
            ),
        ],
        responses={
            200: BookSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                name="request",
                summary="일반적인 바코드 요청",
                description="일반적인 바코드 요청",
                value={"small_region_code": "11010", "isbn13": "9788954699044"},
                request_only=True,
            ),
            OpenApiExample(
                name="400 : ISBN 13자리 아님",
                summary="400 : ISBN 13자리 아님",
                description="ISBN_string이 직접 입력되었으나, 해당 ISBN이 13자리가 아닐경우",
                value={
                    "status": {"code": "E", "msg": "13자리의 ISBN을 입력하십시오."},
                    "request_data": {"ISBN": "입력된13자리가아닌ISBN", "region_code": "11040"},
                    "result_data": {},
                },
                status_codes=["400"],
                response_only=True,
            ),
            OpenApiExample(
                name="400 : ISBN을 찾지 못함",
                summary="400 : 데이터가 입력되지 않았습니다",
                description="필수데이터가 입력되지 않았을경우임. region_code, (ISBN_String || barcode_photo)의 존재를 확인하십시오",
                value={
                    "status": {"code": "E", "msg": "데이터가 입력되지 않았습니다."},
                    "request_data": {"ISBN": "", "region_code": ""},
                    "result_data": {},
                },
                status_codes=["400"],
                response_only=True,
            ),
            OpenApiExample(
                name="400 : ISBN을 추출하던 중 오류가 발생헀습니다. 직접 ISBN을 입력해보십시오.",
                summary="400 : ISBN을 추출하던 중 오류가 발생헀습니다. 직접 ISBN을 입력해보십시오.",
                description="ISBN을 사진으로 추출하던 중 예외가 발생함. ",
                value={
                    "status": {
                        "code": "E",
                        "msg": "ISBN을 추출하던 중 오류가 발생헀습니다. 직접 ISBN을 입력해보십시오.",
                    },
                    "request_data": {"ISBN": "", "region_code": ""},
                    "result_data": {},
                },
                status_codes=["400"],
                response_only=True,
            ),
            OpenApiExample(
                name="400 : ISBN을 찾을 수 없었습니다. 13자리의 ISBN을 직접 입력해보십시오.",
                summary="400 : ISBN을 찾을 수 없었습니다. 13자리의 ISBN을 직접 입력해보십시오.",
                description="바코드에서 ISBN을 찾는데 실패하였음.",
                value={
                    "status": {
                        "code": "E",
                        "msg": "ISBN을 찾을 수 없었습니다. 13자리의 ISBN을 직접 입력해보십시오.",
                    },
                    "request_data": {"ISBN": "", "region_code": ""},
                    "result_data": {},
                },
                status_codes=["400"],
                response_only=True,
            ),
            OpenApiExample(
                name="404 : {self.ISBN} : 해당하는 ISBN에 일치하는 도서정보가 없습니다. \n {MSG}",
                summary="404 : {self.ISBN} : 해당하는 ISBN에 일치하는 도서정보가 없습니다. \n {MSG}",
                description="API에서 해당 ISBN을 찾는데 실패하였음. ",
                value={
                    "status": {
                        "code": "E",
                        "msg": "9782123456803 : 해당하는 ISBN에 일치하는 도서정보가 없습니다. \n {'error': 'ISBN에 해당하는 도서가 없습니다.'}",
                    },
                    "request_data": {"ISBN": "9782123456803", "region_code": "11010"},
                    "result_data": {},
                },
                status_codes=["400"],
                response_only=True,
            ),
            OpenApiExample(
                name="200 : 축하합니다! IIOL에서 이 책을 처음 검색하였습니다!",
                summary="200 : 축하합니다! IIOL에서 이 책을 처음 검색하였습니다!",
                description="IIOL의 DB에 데이터가 없었을 경우, 처음으로 검색에 성공함. ",
                value={
                    "status": {"code": "S", "msg": "축하합니다! IIOL에서 이 책을 처음 검색하였습니다!"},
                    "request_data": {"ISBN": "9788954699044", "region_code": "11010"},
                    "result_data": {},
                },
                status_codes=["200"],
                response_only=True,
            ),
            OpenApiExample(
                name="400 : Code가 W일때",
                summary="400 : Code가 W일때",
                description="검색결과를 DB에 저장할때 실패함",
                value={
                    "status": {
                        "code": "W",
                        "msg": "{'small_region_code': [ErrorDetail(string='이 필드는 null일 수 없습니다.', code='null')]}",
                    },
                    "request_data": {"ISBN": "", "region_code": ""},
                    "result_data": {},
                },
                status_codes=["400"],
                response_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        """
        POST 요청을 받아 도서 정보를 조회합니다.
        FormData 또는 JSON을 통해 'isbn13' 혹은 'barcode_photo'와 'small_region_code'를 전달받아,
        1) 도서 상세 정보를 조회하고
        2) 지역 도서관 목록을 가져온 후
        3) 각 도서관의 소장 및 대출 가능 여부를 확인합니다.
        """
        self.request = request
        self.return_json = {
            "status": {"code": "", "msg": ""},
            "request_data": {"ISBN": self.ISBN, "region_code": self.region_code},
            "result_data": {},
        }

        try:
            if request.POST["small_region_code"]:
                self.region_code = request.POST["small_region_code"].strip()
            if request.POST["isbn13"] and len(request.POST["isbn13"]) != 0:
                self.ISBN = request.POST["isbn13"].strip()
                if len(self.ISBN) != 13:
                    self.response_with_type(
                        "E", "13자리의 ISBN을 입력하십시오.", RESTCode=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return self.response_with_type(
                    "E", "데이터가 입력되지 않았습니다.", RESTCode=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error(f"Error parsing barcode/ISBN search request: {e}", exc_info=True)
            return self.response_with_type(
                "E",
                "ISBN을 추출하던 중 오류가 발생헀습니다. 직접 ISBN을 입력해보십시오.",
                RESTCode=status.HTTP_400_BAD_REQUEST,
            )

        if self.ISBN is None:
            return self.response_with_type(
                "E",
                "ISBN을 찾을 수 없었습니다. 13자리의 ISBN을 직접 입력해보십시오.",
                RESTCode=status.HTTP_400_BAD_REQUEST,
            )

        else:
            self.return_json["request_data"] = {
                "ISBN": self.ISBN,
                "region_code": self.region_code,
            }

            SUCESS, MSG = self.book_info()

            if not SUCESS:
                return self.response_with_type(
                    "E",
                    f"{self.ISBN} : 해당하는 ISBN에 일치하는 도서정보가 없습니다. \n {MSG}",
                    RESTCode=status.HTTP_404_NOT_FOUND,
                )

            self.return_json["result_data"] = {}

            self.get_library_list(self.region_code)
            self.get_book_availablity_by_libcode()
            self.return_json["result_data"]["book_detail"] = self.BOOKINFO_JSON
            self.return_json["result_data"]["library_info"] = self.LIBRARY_INFO_JSON

            return self.response_with_type("S", MSG, RESTCode=status.HTTP_200_OK)

    def get_library_list(self, region_code):
        """
        특정 지역 코드(small_region_code)에 해당하는 도서관 목록을 조회합니다.
        먼저 Redis 캐시에서 조회하고, 없으면 DB에서 확인하며,
        DB에도 없으면 외부 API(LibraryApi)를 호출하여 데이터를 가져온 뒤 캐시 및 DB에 저장합니다.
        """
        LIBRARY_INFO_JSON = cache.get(f"Library_in_{region_code}")
        # LIBRARY_INFO_JSON = None
        if LIBRARY_INFO_JSON is None:  # 캐시조회실패
            try:
                queryset = Library.objects.filter(small_region_code=region_code)
                if queryset.exists():
                    serialized_library = LibrarySerializer(queryset, many=True).data
                    self.LIBRARY_INFO_JSON = {}
                    [
                        self.LIBRARY_INFO_JSON.update({lib["libCode"]: dict(lib)})
                        for lib in serialized_library
                    ]
                else:
                    raise
            except:
                lib_response = self.LibAPI.search_libcode_by_region(
                    region_code=region_code
                )  # API를 통해 해당 지역의 Libary 호출 후
                self.LIBRARY_INFO_JSON = {}
                [
                    self.LIBRARY_INFO_JSON.update({lib["libCode"]: lib})
                    for lib in lib_response
                ]
                cache.set(
                    f"Library_in_{region_code}",
                    json.dumps(self.LIBRARY_INFO_JSON),
                    CACHE_TTL,
                )

                for lib in lib_response:
                    lib.update({"big_region_code": region_code[0:2]})
                    lib.update({"small_region_code": region_code})

                BigRegion_obj, created = BigRegion.objects.get_or_create(
                    big_region_code=region_code[0:2]
                )
                SmallRegion.objects.get_or_create(
                    big_region_code=BigRegion_obj, small_region_code=region_code
                )

                serializer = LibrarySerializer(data=lib_response, many=True)

                if serializer.is_valid():
                    serializer.save()
                else:
                    self.set_JSON_header("W", serializer.errors)

        else:
            self.LIBRARY_INFO_JSON = json.loads(LIBRARY_INFO_JSON)
        self.libcode_list = list(self.LIBRARY_INFO_JSON.keys())
        return

    def book_info(self):
        """
        ISBN을 기반으로 도서의 상세 메타데이터 및 대출 통계 정보를 조회합니다.
        먼저 캐시를 확인하고, 없으면 DB를 조회하며,
        DB에도 없으면 외부 API(도서관정보나루)를 통해 최초 조회 후 저장합니다.
        """
        msg = None
        # 일단은 ISBN13이 들어올것이라고 기대, ISBN10일경우도 추후 만들기
        BOOKINFO_JSON = cache.get(f"ISBN13_{self.ISBN}")
        # BOOKINFO_JSON = None
        if BOOKINFO_JSON is not None:
            self.BOOKINFO_JSON = json.loads(BOOKINFO_JSON)
        else:  # 캐시조회실패
            queryset = Book.objects.filter(isbn13=self.ISBN)

            if queryset.exists():  # DB에 있었음!
                serialized_book = BookSerializer(queryset, many=True).data
                self.BOOKINFO_JSON = [dict(book) for book in serialized_book]
                cache.set(
                    f"ISBN13_{self.ISBN}", json.dumps(self.BOOKINFO_JSON), CACHE_TTL
                )
            else:  # API로 최초조회 -> 당신이 이올에서 처음 이책을 발견했어요!
                book_response = self.LibAPI.search_book_detail_by_ISBN(self.ISBN)
                try:
                    self.BOOKINFO_JSON = [
                        book["book"] for book in book_response["detail"]
                    ]
                    cache.set(
                        f"ISBN13_{self.ISBN}", json.dumps(self.BOOKINFO_JSON), CACHE_TTL
                    )

                    serializer = BookSerializer(data=self.BOOKINFO_JSON[0])
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        logger.warning(f"Serializer validation failed for book data: {serializer.errors}")
                        self.set_JSON_header(
                            "W", serializer.errors
                        )  # Serializer 오류시 logging을 위함
                    msg = "축하합니다! IIOL에서 이 책을 처음 검색하였습니다!"
                except:
                    return False, book_response
        return True, msg

    def get_book_availablity_by_libcode(self):
        """
        앞서 확보한 도서관 목록(libcode_list)을 순회하며,
        각 도서관별로 해당 도서(ISBN)의 소장 여부와 대출 가능 상태를 확인합니다.
        마찬가지로 캐시를 우선적으로 활용하여 응답 지연 시간을 최소화합니다.
        """
        for libcode in self.libcode_list:
            book_availablity_cache = cache.get(f"{libcode}_{self.ISBN}")
            if book_availablity_cache is not None:
                self.LIBRARY_INFO_JSON[libcode]["hasBook"] = book_availablity_cache[0]
                self.LIBRARY_INFO_JSON[libcode][
                    "loanAvailable"
                ] = book_availablity_cache[1]
            else:
                book_availablity = self.LibAPI.search_book_availability_of_lib_by_ISBN(
                    ISBN=self.ISBN, lib_code=libcode
                )
                self.LIBRARY_INFO_JSON[libcode]["hasBook"] = book_availablity["result"][
                    "hasBook"
                ]
                self.LIBRARY_INFO_JSON[libcode]["loanAvailable"] = book_availablity[
                    "result"
                ]["loanAvailable"]

                book_availablity_cache = (
                    book_availablity["result"]["hasBook"],
                    book_availablity["result"]["loanAvailable"],
                )
                cache.set(
                    f"{libcode}_{self.ISBN}",
                    book_availablity_cache,
                    CACHE_TTL,
                )
        return


def get_region_json_with_cache():
    region_json = cache.get("region_json")
    if region_json is None:
        file_path = os.path.join(settings.STATIC_ROOT, "json/region_code.json")
        with open(file_path, "r", encoding="utf-8") as f:
            region_json = json.load(f)
        cache.set("region_json", region_json, CACHE_TTL)
    return region_json


# @ cache_page(60, key_prefix='barcode:html')
def detect_page(request):
    region_json = get_region_json_with_cache()
    return render(
        request,
        "barcode/detect.html",
        {
            "region_json": region_json,
        },
    )


def retrieve_region_code(request):
    region_json = get_region_json_with_cache()
    return JsonResponse(
        data=region_json,
        json_dumps_params={"ensure_ascii": False},
        status=200,
        safe=False,
    )


# 9788956748535
