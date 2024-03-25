from django.db import models


class DashboardData(models.Model):
    hotel_id = models.PositiveIntegerField()
    date = models.DateField()
    bookings_count = models.PositiveIntegerField(default=0)
    cancellations_count = models.PositiveIntegerField(default=0)
    period = models.CharField(max_length=10)

    class Meta:
        unique_together = ('hotel_id', 'date', 'period')

    def __str__(self):
        return (f"Hotel {self.hotel_id} - {self.period} - {self.date} - Bookings: {self.bookings_count}, "
                f"Cancellations: {self.cancellations_count}")
