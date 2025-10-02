from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView
)
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
        path("admin/", admin.site.urls),
        path(
                "api/airport/",
                include(
                        "airport_api.urls",
                        namespace="airport-api"
                )
        ),
        path("api/user/", include("user.urls", namespace="user")),
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
                "api/schema/swagger/",
                SpectacularSwaggerView.as_view(url_name="schema"),
                name="swagger"
        ),
        path(
                "api/schema/redoc/",
                SpectacularRedocView.as_view(url_name="schema"),
                name="redoc"
        ),
        path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)