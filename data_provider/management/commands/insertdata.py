from datetime import datetime
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand
import requests
import csv
from RoomPriceGenie.settings import BASE_DIR, config
from data_provider.models import Event


class Command(BaseCommand):
    help = "Simulate hotel data"

    def handle(self, *args, **options):
        with open(BASE_DIR / "data.csv", mode="r", encoding="utf-8") as file:
            count = 0
            reader = csv.DictReader(file)
            for row in reader:
                if count >= 50:
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
                    f'http://localhost:{config("SVC_PORT")}/api/events/',
                    json=data,
                )
                if response.status_code == 409:
                    self.stdout.write(self.style.ERROR(f"Event with id {data['id']} already exists"))
                elif response.status_code == 201:
                    self.stdout.write(self.style.SUCCESS(f"Inserted data: {data}"))
                    count += 1
                else:
                    self.stdout.write(self.style.ERROR(f"Failed to post data: {data}"))
                    break
        
                
                
        # with open(BASE_DIR / "data.csv", mode="r", encoding="utf-8") as file:
        #     count = 0
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         if count >= 10:
        #             break

        #         if not Event.objects.filter(id=row['id']).exists():
        #             event_timestamp = make_aware(
        #                 datetime.strptime(row['event_timestamp'], '%Y-%m-%d %H:%M:%S')
        #             )
            
        #             night_of_stay = make_aware(
        #                 datetime.strptime(row['night_of_stay'], '%Y-%m-%d')
        #             )
        #             event = Event.objects.create(
        #                 id=row['id'],
        #                 hotel_id=row['hotel_id'],
        #                 event_timestamp=event_timestamp,
        #                 rpg_status=row['status'],
        #                 room_id=row['room_reservation_id'],
        #                 night_of_stay=night_of_stay
        #             )
        #             event.save()
        #             count += 1
