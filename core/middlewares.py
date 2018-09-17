import sys
import json
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from core.models import WebRequest

from app.site.urls import app_name as site_app_name


__all__ = (
    'WebRequestMiddleware',
)


class WebRequestMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        current_url = request.resolver_match.view_name

        if not settings.IS_SAVING_HTTP_REQUESTS \
                or site_app_name not in current_url \
                or request.path.endswith('/favicon.ico'):
            return response

        try:
            self.save(request, response)
            pass
        except Exception as e:
            print(sys.stderr, "Error saving request log", e)
        return response

    def save(self, request, response):
        meta = request.META.copy()
        remote_addr_fwd = None

        if 'HTTP_X_FORWARDED_FOR' in meta:
            remote_addr_fwd = meta['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()

        web_request = {
            'host': request.get_host(),
            'path': request.path,
            'method': request.method,
            'uri': request.build_absolute_uri(),
            'status_code': response.status_code,
            'user_agent': meta.pop('HTTP_USER_AGENT', None),
            'remote_addr': meta.pop('REMOTE_ADDR', None),
            'remote_addr_fwd': remote_addr_fwd,
            'cookies': None if not request.COOKIES else json.dumps(request.COOKIES),
            'get': None if not request.GET else json.dumps(request.GET),
            'post': None if not request.POST else json.dumps(request.POST),
            'is_secure': request.is_secure(),
            'is_ajax': request.is_ajax()
        }
        WebRequest.objects.create(request=web_request)
