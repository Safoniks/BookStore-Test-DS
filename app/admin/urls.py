from django.conf.urls import url

from . import views

app_name = 'admin'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^web-requests/$', views.web_requests, name='web_requests'),
    url(r'^book-logs/$', views.book_logs, name='book_logs'),
]
