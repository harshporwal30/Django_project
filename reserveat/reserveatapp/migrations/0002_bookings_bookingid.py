# Generated by Django 4.2.7 on 2024-01-20 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserveatapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='bookingid',
            field=models.CharField(default='', max_length=200),
        ),
    ]