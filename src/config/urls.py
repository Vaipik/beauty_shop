from django.conf.urls.static import static
from django.urls import include, path

from config import settings


urlpatterns = [
    path("api/v1/", include("api.v1.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("debug/", include("debug_toolbar.urls"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
