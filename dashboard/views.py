from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth

from dashboard.utils import validate_dashboard_query
from data_provider.models import Event


class DashboardViewSet(viewsets.ViewSet):
    """
        Retrieves aggregated data on bookings and cancellations for a hotel.

        This API endpoint provides insights into the number of bookings and cancellations
        for a specified hotel over a selected period (day, month, or year). It helps in understanding
        the booking trends and can assist in planning and analysis.
    """
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('hotel_id', openapi.IN_QUERY, description="ID of the hotel", type=openapi.TYPE_INTEGER),
        openapi.Parameter('period', openapi.IN_QUERY, description="Period of the dashboard", type=openapi.TYPE_STRING),
        openapi.Parameter('year', openapi.IN_QUERY, description="Year of the dashboard", type=openapi.TYPE_INTEGER),
    ])
    def list(self, request):
        """
                Handles GET requests to aggregate booking data based on the specified period.

                Parameters:
                - hotel_id (required): The unique identifier of the hotel.
                - period (required): The period for which data is aggregated. Valid values are 'day', 'month', 'year'.
                - year (required): The year for which data is being requested.

                Returns:
                - 200 OK: Successfully returns the aggregated booking and cancellation data.
                - 400 Bad Request: Returns an error if any of the required parameters are missing or invalid.
                - 404 Not Found: Returns an error if the specified hotel does not exist in the system.
        """
        hotel_id = request.query_params.get('hotel_id')
        period = request.query_params.get('period')
        year = request.query_params.get('year')

        error = validate_dashboard_query(hotel_id=hotel_id, period=period, year=year)
        if error:
            return error
        filters = {
            'hotel_id': hotel_id,
            'night_of_stay__year': year,
            'rpg_status': 1
        }

        if period == 'day':
            data = Event.objects.filter(**filters).annotate(date=TruncDay('night_of_stay')).values('date').annotate(
                count=Count('id')).values('date', 'count')
        elif period == 'month':
            data = Event.objects.filter(**filters).annotate(month=TruncMonth('night_of_stay')).values('month').annotate(
                count=Count('id')).values('month', 'count')
        elif period == 'year':
            data = Event.objects.filter(**filters).values('night_of_stay__year').annotate(count=Count('id')).values(
                'night_of_stay__year', 'count')
        else:
            return Response({"error": "Invalid period"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)
