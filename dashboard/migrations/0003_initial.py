# Generated by Django 5.0.3 on 2024-03-19 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0002_delete_dashboardevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_id', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('bookings_count', models.PositiveIntegerField(default=0)),
                ('cancellations_count', models.PositiveIntegerField(default=0)),
                ('period', models.CharField(max_length=10)),
            ],
            options={
                'unique_together': {('hotel_id', 'date', 'period')},
            },
        ),
    ]