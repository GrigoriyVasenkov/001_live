from rest_framework import serializers

from users.models import Project, Event, Function


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        exclude = ('id', )


class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        exclude = ('id', )


class FunctionSerializer(serializers.ModelSerializer):
    event_id = EventSerializer(read_only=True)
    
    class Meta:
        model = Function
        exclude = ('id', )