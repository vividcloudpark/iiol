from .common import *

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE


CORS_ALLOWED_ORIGINS = [
    "http://thecloudpark.xyz:3001",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
