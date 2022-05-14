from rest_framework import filters, permissions, status, viewsets

from users.models import Project, Event, Function
from .serializers import ProjectSerializer, EventSerializer, FunctionSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = (AdminOrReadOnly,)
    # pagination_class = LimitOffsetPagination
    # filterset_class = TitleFilter


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class FunctionViewSet(viewsets.ModelViewSet):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer
