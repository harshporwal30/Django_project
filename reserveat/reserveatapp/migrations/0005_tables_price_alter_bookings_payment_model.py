# Generated by Django 4.2.7 on 2024-01-21 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserveatapp', '0004_bookings_payment_model_bookings_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tables',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='payment_model',
            field=models.CharField(default='PayPal', max_length=200),
        ),
    ]
