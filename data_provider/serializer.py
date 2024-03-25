from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)
    class Meta:
        model = Event
        fields = ('id', 'room_id', 'night_of_stay', 'rpg_status', 'event_timestamp', 'hotel_id')
