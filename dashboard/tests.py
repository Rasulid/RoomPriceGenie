from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from data_provider.models import Event
from django.utils import timezone
from datetime import timedelta
from uuid import uuid4


class DashboardViewSetTests(APITestCase):
    def setUp(self):
        Event.objects.create(hotel_id=1, night_of_stay=timezone.now().date(), rpg_status=1, room_id=uuid4())
        Event.objects.create(hotel_id=1, night_of_stay=timezone.now().date() - timedelta(days=1), rpg_status=1,
                             room_id=uuid4())

    def test_dashboard_day(self):
        url = reverse('dashboard-list')
        response = self.client.get(url, {'hotel_id': 1, 'period': 'day', 'year': timezone.now().year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dashboard_month(self):
        url = reverse('dashboard-list')
        response = self.client.get(url, {'hotel_id': 1, 'period': 'month', 'year': timezone.now().year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dashboard_year(self):
        url = reverse('dashboard-list')
        response = self.client.get(url, {'hotel_id': 1, 'period': 'year', 'year': timezone.now().year})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dashboard_invalid_period(self):
        url = reverse('dashboard-list')
        response = self.client.get(url, {'hotel_id': 1, 'period': 'invalid', 'year': timezone.now().year})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
