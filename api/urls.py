from django.urls import include, path
from rest_framework import routers

from .views import ProjectViewSet, EventViewSet, FunctionViewSet

router_v1_0 = routers.DefaultRouter()
router_v1_0.register('project', ProjectViewSet)
router_v1_0.register('event', EventViewSet)
router_v1_0.register('function', FunctionViewSet)


urlpatterns = [
    path('', include(router_v1_0.urls)),
]
