from django.contrib import admin

from data_provider.models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "room_id", "night_of_stay", "rpg_status", "event_timestamp", "hotel_id"]
    list_display_links = ["id", "room_id"]
    list_filter = ["hotel_id", "rpg_status", "event_timestamp"]
