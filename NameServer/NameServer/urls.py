from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'^admin/', admin.site.urls),
    url('api-auth/', include('rest_framework.urls')),
    #url('/', TemplateView.as_view(template_name='signup.html')),
]