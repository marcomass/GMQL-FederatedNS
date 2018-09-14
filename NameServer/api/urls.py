from django.conf.urls import url, include

from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'dataset', views.DatasetViewSet)
router.register(r'institution', views.InstitutionViewSet)
router.register(r'location', views.LocationViewSet)
router.register(r'authentication', views.AuthenticationViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]