from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


def validate_dashboard_query(hotel_id: int, period: str, year: str):
    if not hotel_id:
        raise ValidationError({"error": "hotel_id required parameters"})
    if not period:
        raise ValidationError({"error": "period is required"})
    if not year:
        raise ValidationError({"error": "year is required and must be a number"})

    return None
