# Generated by Django 4.2.7 on 2024-01-09 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserveatapp', '0004_alter_ambianceimg_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambianceimg',
            name='image',
            field=models.ImageField(upload_to='media'),
        ),
    ]
