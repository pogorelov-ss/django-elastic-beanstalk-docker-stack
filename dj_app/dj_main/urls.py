
from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.http import HttpResponse


def health_check_view(request):
    return HttpResponse(status=200)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^health-check/$', health_check_view),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

api_urls = [
]

urlpatterns += api_urls
