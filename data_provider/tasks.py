import csv
from celery import shared_task
import requests
import logging
from RoomPriceGenie.settings import BASE_DIR, config

logger = logging.getLogger(__name__)


@shared_task
def fill_data_provider_database():
    logger.info("Starting to fill data provider database from csv")
    with open(BASE_DIR / "data.csv", mode="r", encoding="utf-8") as file:
            count = 0
            reader = csv.DictReader(file)
            for row in reader:
                if count >= 100:
                    break
                data = {
                    "id": row["id"],
                    "room_id": row["room_reservation_id"],
                    "night_of_stay": row["night_of_stay"],
                    "rpg_status": row["status"],
                    "event_timestamp": row["event_timestamp"],
                    "hotel_id": row["hotel_id"],
                }
                response = requests.post(
                    f'http://web:{config("SVC_PORT")}/api/events/',
                    json=data,
                )
                if response.status_code == 409:
                    print(f"Event with id {data['id']} already exists")
                elif response.status_code == 201:
                    print(f"Inserted data: {data}")
                    count += 1
                else:
                    print(f"Failed to post data: {data}")
                    break
