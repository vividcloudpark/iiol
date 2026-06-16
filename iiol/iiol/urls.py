"""iiol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import barcode.views as barcode_view
import iiol.views as iiol_view
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularYAMLAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.urls import path, re_path


app_name = "iiol"

# 서버 환경에 따라 URL Prefix(예: /api)가 필요할 경우를 대비한 Prefix 정규표현식 변수.
site_prefix = f"^{settings.FORCE_SCRIPT_NAME[1:]}(.*)$"

urlpatterns = [
    # 루트('/') 경로 접속 시 기본적으로 바코드 스캔/검색 페이지로 매핑
    path("", barcode_view.detect_page),
    
    # Django 기본 관리자 페이지 라우팅
    path("admin/", admin.site.urls),
    
    # DRF API 인증을 위한 라우팅
    path("api-auth/", include("rest_framework.urls")),
    
    # 사용자 계정(로그인/회원가입 등) 관련 라우팅 ('accounts/urls.py' 참조)
    path("accounts/", include("accounts.urls")),
    
    # 바코드 감지 및 도서/도서관 검색 관련 라우팅 ('barcode/urls.py' 참조)
    path("barcode/", include("barcode.urls")),
    
    # 도서관 정보 조회 관련 라우팅 ('library/urls.py' 참조)
    path("library/", include("library.urls")),
    
    # 도서 정보 조회 관련 라우팅 ('books/urls.py' 참조)
    path("books/", include("books.urls")),
    
    # 내 도서 위시리스트 관련 라우팅 ('mybookwishlist/urls.py' 참조)
    path("mybookwishlist/", include("mybookwishlist.urls")),
    
    # 컨테이너 오케스트레이션(LB 등) 헬스체크용 라우팅
    path("healthcheck/", iiol_view.health_check),
]


urlpatterns += [
    # drf-spectacular를 이용한 OpenAPI 스키마 생성 및 조회 엔드포인트
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),  # JSON 형식 스키마
    path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"), # YAML 형식 스키마
    
    # OpenAPI 문서를 시각적으로 보여주는 Swagger UI 엔드포인트
    path(
        "docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema-json"),
        name="swagger-ui",
    ),
    
    # OpenAPI 문서를 문서형식으로 깔끔하게 보여주는 Redoc 엔드포인트
    path(
        "docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema-json"),
        name="redoc",
    ),
]

# 개발 및 서비스 환경에서 정적 파일(JS, CSS, 이미지 등)과 미디어 파일을 서빙하기 위한 설정 추가
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static("static/", document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns += [
            path("__debug__/", include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
