import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from accounts.regions import region_data, region_name, valid_region
from .provider import Data4Library, LibraryApiError
from .validators import normalize_isbn


@require_GET
def home(request):
    return render(request, "catalog/home.html", {
        "regions": region_data(),
        "profile_region": getattr(request.user, "region_code", "") if request.user.is_authenticated else "",
    })


@require_POST
def search(request):
    try:
        payload = json.loads(request.body or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "요청을 읽을 수 없습니다."}, status=400)
    if not isinstance(payload, dict):
        return JsonResponse({"error": "요청 형식이 올바르지 않습니다."}, status=400)

    try:
        isbn13 = normalize_isbn(str(payload.get("isbn13", "")))
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    region_code = str(payload.get("region_code", ""))
    if not valid_region(region_code):
        return JsonResponse({"error": "검색할 시·군·구를 선택해 주세요."}, status=400)

    try:
        result = Data4Library().search(isbn13, region_code)
    except LookupError as exc:
        return JsonResponse({"error": str(exc)}, status=404)
    except LibraryApiError as exc:
        status = 503 if "키가 설정" in str(exc) else 502
        return JsonResponse({"error": str(exc)}, status=status)

    result["region_name"] = region_name(region_code)
    result["isbn13"] = isbn13
    return JsonResponse(result, json_dumps_params={"ensure_ascii": False})


@require_GET
def regions(request):
    return JsonResponse(region_data(), json_dumps_params={"ensure_ascii": False})
