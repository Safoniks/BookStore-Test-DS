from django.conf.urls import url

from . import views

app_name = 'site'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add/$', views.add_book, name='add_book'),
    url(r'^(?P<pk>\d+)/$', views.book_detail, name='book_detail'),
    url(r'^(?P<pk>\d+)/delete/$', views.delete_book, name='delete_book'),
]
