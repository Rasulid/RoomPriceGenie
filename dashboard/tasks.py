from datetime import datetime, timedelta
import requests
import logging
from celery import shared_task
from decouple import config
from dashboard.models import DashboardData

logger = logging.getLogger(__name__)


@shared_task
def fill_dashboard_database():
    data_provider_url = f"http://web:{config('SVC_PORT')}/api/events/"
    end_of_yesterday = datetime.now().replace(
        hour=23, minute=59, second=59, microsecond=59
    )
    start_of_yesterday = end_of_yesterday - timedelta(days=1)
    start_of_yesterday = start_of_yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    params = {
        "updated__gte": start_of_yesterday.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "updated__lte": end_of_yesterday.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    response = requests.get(data_provider_url, params=params)
    if response.status_code == 200:
        events = response.json()
        for event in events:
            print(28, event)
            for hotel_id in set(event['hotel_id'] for event in events):
                hotel_events = [event for event in events if event['hotel_id'] == hotel_id]
                bookings_count = sum(event['rpg_status'] == 1 for event in hotel_events)
                cancellations_count = sum(event['rpg_status'] == 2 for event in hotel_events)

                dashboard_data, created = DashboardData.objects.update_or_create(
                    hotel_id=hotel_id,
                    date=end_of_yesterday,
                    defaults={
                        'bookings_count': bookings_count,
                        'cancellations_count': cancellations_count,
                        'period': 'daily',
                    }
                )
                if dashboard_data:
                    logger.info(f"Updated dashboard data for hotel {hotel_id} for {end_of_yesterday}")
        else:
            logger.error(f"Failed to fetch events: {response.status_code}, Data: {response.content}")
