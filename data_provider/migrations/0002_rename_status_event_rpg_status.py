# Generated by Django 5.0.3 on 2024-03-21 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_provider', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='status',
            new_name='rpg_status',
        ),
    ]