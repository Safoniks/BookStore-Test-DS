from django.shortcuts import render

from core.models import WebRequest, AuditLog

__all__ = (
    'home',
    'web_requests',
    'book_logs',
)


def home(request):
    template_name = 'admin/content/home.html'
    context = {}
    return render(request, template_name, context)


def web_requests(request):
    template_name = 'admin/content/web_requests.html'

    ordered_requests = WebRequest.objects.all()[:10]
    WebRequest.objects.exclude(pk__in=list(ordered_requests.values_list("id", flat=True))).delete()
    context = {
        'web_requests': ordered_requests
    }
    return render(request, template_name, context)


def book_logs(request):
    template_name = 'admin/content/book_logs.html'

    logs = AuditLog.objects.all().order_by('-action_time')[:20]
    context = {
        'logs': logs
    }
    return render(request, template_name, context)
