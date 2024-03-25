from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from .models import Event
from .serializer import EventSerializer


class EventListCreateView(generics.ListCreateAPIView):
    """
        List and create events for hotels.

        This view provides the ability to list all events, with optional filtering by hotel ID and event status,
        and to create new events. It supports filtering events based on their timestamps and night of stay.
    """
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["hotel_id", "rpg_status"]

    def get_queryset(self):
        """
                Optionally filters events by 'updated__gte', 'updated__lte', 'night_of_stay__gte', and 'night_of_stay__lte'
                query parameters in the URL.

                Returns:
                    - Queryset of Event objects, possibly filtered and ordered by event timestamp.
        """
        queryset = Event.objects.all().order_by("-event_timestamp")

        updated__gte = self.request.query_params.get("updated__gte")

        if updated__gte:
            queryset = queryset.filter(event_timestamp__gte=updated__gte)

        updated__lte = self.request.query_params.get("updated__lte")
        if updated__lte:
            queryset = queryset.filter(event_timestamp__lte=updated__lte)

        night_of_stay__gte = self.request.query_params.get("night_of_stay__gte")
        if night_of_stay__gte:
            queryset = queryset.filter(night_of_stay__gte=night_of_stay__gte)

        night_of_stay__lte = self.request.query_params.get("night_of_stay__lte")
        if night_of_stay__lte:
            queryset = queryset.filter(night_of_stay__lte=night_of_stay__lte)

        return queryset

    def create(self, request, *args, **kwargs):
        """
               Creates a new event instance.

               The request data is validated against the EventSerializer.
               If an event with the given ID already exists, a 409 Conflict response is returned.

               Returns:
                   - HTTP 201 Created if the event is successfully created.
                   - HTTP 409 Conflict if an event with the provided ID already exists.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)
        except IntegrityError:
            return Response(
                {"error": "event with this id already exists"}, status=409
            )
