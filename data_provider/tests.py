from decouple import config
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Event


class EventAPITests(APITestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        Event.objects.all().delete()
        super().tearDown()

    def test_create_event_success(self):
        url = reverse('event-list-create')
        data = {
            'id': 1,
            'room_id': '0498d45a-263c-433c-90d5-aee300bfec37',
            'night_of_stay': '2022-08-01',
            'rpg_status': 1,
            'event_timestamp': '2022-07-31T12:00:40+05:00',
            'hotel_id': 2607
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().id, 1)

    def test_create_event_failure_due_to_duplicate_id(self):
        Event.objects.create(
            id=1,
            room_id='0498d45a-263c-433c-90d5-aee300bfec37',
            night_of_stay='2022-08-01',
            rpg_status=1,
            event_timestamp='2022-07-31T12:00:40+05:00',
            hotel_id=2607
        )

        url = reverse("event-list-create")
        data = {
            'id': 1,
            'room_id': '0498d45a-263c-433c-90d5-aee300bfec37',
            'night_of_stay': '2022-08-02',
            'rpg_status': 2,
            'event_timestamp': '2022-08-01T13:00:40+05:00',
            'hotel_id': 2607
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(Event.objects.count(), 1)
