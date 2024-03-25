from django.db import models
from django.utils import timezone


class Event(models.Model):
    RPG_STATUS_CHOICES = (
        (1, "Booking"),
        (2, "Cancellation"),
    )
    id = models.BigAutoField(primary_key=True)
    room_id = models.UUIDField()
    night_of_stay = models.DateField()
    rpg_status = models.PositiveSmallIntegerField(choices=RPG_STATUS_CHOICES)
    event_timestamp = models.DateTimeField(default=timezone.now)
    hotel_id = models.PositiveIntegerField()

    created_at = models.DateTimeField(default=timezone.now)
    added_to_dashboard = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room_id} - {self.get_rpg_status_display()}"
