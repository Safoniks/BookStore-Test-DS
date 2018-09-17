from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', include('app.admin.urls')),
    url(r'^', include('app.site.urls')),
]
