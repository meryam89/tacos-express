from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("restaurant.urls")),
    path("compte/", include("accounts.urls")),
    path("", include("orders.urls")),

    path("api/", include("api.urls")),

    path(
        "api/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    path(
        "api/auth/token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),

    path(
        "api/auth/logout/",
        TokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
]


# Permet d'afficher les photos des produits pendant le développement
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )