# Generated by Django 5.0.3 on 2024-03-21 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_provider', '0002_rename_status_event_rpg_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='room_reservation_id',
            new_name='room_id',
        ),
    ]
