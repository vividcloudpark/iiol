import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .provider import Data4Library
from .validators import normalize_isbn


class IsbnValidationTests(TestCase):
    def test_accepts_valid_isbn_with_separators(self):
        self.assertEqual(normalize_isbn("978-89-5469-904-4"), "9788954699044")

    def test_rejects_regular_ean13(self):
        with self.assertRaises(ValueError):
            normalize_isbn("1923055034006")

    def test_rejects_isbn_reserved_music_prefix(self):
        with self.assertRaises(ValueError):
            normalize_isbn("9790123456785")

    def test_rejects_invalid_check_digit(self):
        with self.assertRaises(ValueError):
            normalize_isbn("9788962475218")


class SearchEndpointTests(TestCase):
    def test_guest_home_renders_region_selector_and_camera_actions(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="province-select"')
        self.assertContains(response, 'capture="environment"')

    def post_search(self, isbn="9788954699044", region="31023"):
        return self.client.post(
            reverse("search"),
            data=json.dumps({"isbn13": isbn, "region_code": region}),
            content_type="application/json",
        )

    def test_guest_can_search_and_get_library_results(self):
        payload = {
            "book": {"bookname": "테스트 책", "authors": "작가", "publisher": "출판사"},
            "libraries": [{
                "code": "LIB-1", "name": "분당 도서관", "address": "성남시", "homepage": "",
                "has_book": True, "loan_available": False,
            }],
            "availability_as_of": "2026-09-23",
        }
        with patch("catalog.views.Data4Library.search", return_value=payload):
            response = self.post_search()
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["region_name"], "경기도 성남시 분당구")
        self.assertEqual(body["libraries"][0]["loan_available"], False)

    def test_invalid_isbn_is_rejected_before_provider_call(self):
        with patch("catalog.views.Data4Library.search") as search:
            response = self.post_search(isbn="1923055034006")
        self.assertEqual(response.status_code, 400)
        search.assert_not_called()

    def test_unknown_region_is_rejected(self):
        response = self.post_search(region="99999")
        self.assertEqual(response.status_code, 400)

    def test_missing_api_key_returns_service_unavailable(self):
        with patch.dict("os.environ", {"LIBRARY_API_KEY": ""}):
            response = self.post_search()
        self.assertEqual(response.status_code, 503)


class ProviderTests(TestCase):
    @patch("catalog.provider.requests.get")
    def test_request_keeps_api_key_in_query_parameters(self, get):
        response = get.return_value
        response.json.return_value = {"response": {"detail": []}}
        api = Data4Library(auth_key="test-key")
        api._request("srchDtlList", isbn13="9788954699044")
        self.assertEqual(get.call_args.kwargs["params"]["authKey"], "test-key")
        self.assertTrue(get.call_args.args[0].startswith("https://"))

    def test_search_combines_book_holding_and_availability_data(self):
        api = Data4Library(auth_key="test-key")
        with patch.object(api, "_request") as request:
            request.side_effect = [
                {"detail": {"book": {"bookname": "테스트 책"}}},
                {"numFound": 1, "libs": {"lib": {
                    "libCode": "LIB-1", "libName": "분당도서관", "address": "성남시 분당구",
                }}},
                {"result": {"hasBook": "Y", "loanAvailable": "N"}},
            ]
            result = api.search("9788954699044", "31023")

        self.assertEqual(result["book"]["bookname"], "테스트 책")
        self.assertEqual(result["libraries"][0]["name"], "분당도서관")
        self.assertTrue(result["libraries"][0]["has_book"])
        self.assertFalse(result["libraries"][0]["loan_available"])
        self.assertEqual(request.call_args_list[1].kwargs["dtl_region"], "31023")
