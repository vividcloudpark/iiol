import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta

import requests
from django.utils import timezone


class LibraryApiError(Exception):
    pass


class Data4Library:
    base_url = "https://data4library.kr/api/"

    def __init__(self, auth_key=None, timeout=6):
        self.auth_key = auth_key if auth_key is not None else os.getenv("LIBRARY_API_KEY", "")
        self.timeout = timeout

    def _request(self, endpoint, **params):
        if not self.auth_key:
            raise LibraryApiError("도서관 검색 API 키가 설정되지 않았습니다.")
        query = {"authKey": self.auth_key, "format": "json", **params}
        try:
            response = requests.get(self.base_url + endpoint, params=query, timeout=self.timeout)
            response.raise_for_status()
            body = response.json().get("response", {})
        except (requests.RequestException, ValueError, AttributeError) as exc:
            raise LibraryApiError("도서관 정보나루에 연결하지 못했습니다.") from exc
        if body.get("error") or body.get("errorCode") not in (None, "", 0, "0"):
            raise LibraryApiError("도서관 정보나루에서 검색을 처리하지 못했습니다.")
        return body

    @staticmethod
    def _list(value, item_key=None):
        if not value:
            return []
        values = value if isinstance(value, list) else [value]
        if item_key:
            return [item.get(item_key, {}) for item in values if isinstance(item, dict)]
        return values

    def _library_availability(self, isbn13, library):
        lib_code = str(library.get("libCode", ""))
        if not lib_code:
            return None, None
        try:
            data = self._request("bookExist", libCode=lib_code, isbn13=isbn13).get("result", {})
            return self._bool(data.get("hasBook")), self._bool(data.get("loanAvailable"))
        except LibraryApiError:
            return True, None

    @staticmethod
    def _bool(value):
        if value is True or value == 1 or str(value).lower() in {"y", "true", "1"}:
            return True
        if value is False or value == 0 or str(value).lower() in {"n", "false", "0"}:
            return False
        return None

    def search(self, isbn13, region_code):
        detail = self._request("srchDtlList", isbn13=isbn13, loaninfoYN="Y")
        detail_rows = self._list(detail.get("detail"), "book")
        if not detail_rows:
            raise LookupError("해당 ISBN의 도서 정보를 찾지 못했습니다.")
        book = detail_rows[0]

        libraries = []
        seen_codes = set()
        page = 1
        while page <= 25:
            holdings = self._request(
                "libSrchByBook",
                isbn=isbn13,
                region=region_code[:2],
                dtl_region=region_code,
                pageNo=page,
                pageSize=100,
            )
            current = self._list(holdings.get("libs"), "lib")
            new_libraries = [lib for lib in current if str(lib.get("libCode", "")) not in seen_codes]
            libraries.extend(new_libraries)
            seen_codes.update(str(lib.get("libCode", "")) for lib in new_libraries)
            try:
                total = int(holdings.get("numFound", 0))
            except (TypeError, ValueError):
                total = 0
            if not current or not new_libraries or (total and len(libraries) >= total) or len(current) < 100:
                break
            page += 1

        availability = {}
        with ThreadPoolExecutor(max_workers=16) as pool:
            futures = {
                pool.submit(self._library_availability, isbn13, library): str(library.get("libCode", ""))
                for library in libraries
            }
            for future in as_completed(futures):
                availability[futures[future]] = future.result()

        results = []
        for library in libraries:
            code = str(library.get("libCode", ""))
            has_book, loan_available = availability.get(code, (True, None))
            results.append({
                "code": code,
                "name": library.get("libName", "이름 미제공"),
                "address": library.get("address", ""),
                "homepage": library.get("homepage", ""),
                "has_book": has_book if has_book is not None else True,
                "loan_available": loan_available,
            })
        as_of = (timezone.localdate() - timedelta(days=1)).isoformat()
        return {"book": book, "libraries": results, "availability_as_of": as_of}
