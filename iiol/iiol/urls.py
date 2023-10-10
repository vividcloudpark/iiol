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
from drf_spectacular.views import SpectacularJSONAPIView,SpectacularYAMLAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.urls import path, re_path


app_name = 'iiol'
site_prefix = f'^{settings.FORCE_SCRIPT_NAME[1:]}(.*)$'

urlpatterns = [
    path('', barcode_view.detect_page),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls')),
    path('barcode/', include('barcode.urls')),
    path('library/', include('library.urls')),
    path('books/', include('books.urls')),
    path('mybookwishlist/', include('mybookwishlist.urls')),

]



urlpatterns += [
    # Open API 자체를 조회 : json, yaml,
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    # Open API Document UI로 조회: Swagger, Redoc
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui", ),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc", ),

    # ...
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static('static/',
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
