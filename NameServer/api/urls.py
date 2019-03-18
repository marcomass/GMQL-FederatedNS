from django.conf.urls import url, include

from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static


from api.views import CustomObtainAuthToken
from . import views


router = routers.DefaultRouter()
router.register(r'dataset', views.DatasetViewSet)
router.register(r'instance', views.InstanceViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'location', views.LocationViewSet)
router.register(r'authentication', views.AuthenticationViewSet)



urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^token/', CustomObtainAuthToken.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)