from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path(r'', include('app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
