from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=settings.STATIC_URL + "/index.html")),
    url(r'^api/', include('api.urls')),
    url(r'^admin/', admin.site.urls),
    url('api-auth/', include('rest_framework.urls')),

    #url(r'^docs/', include('rest_framework_docs.urls')),
]