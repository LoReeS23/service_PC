# Generated by Django 3.2.7 on 2021-09-17 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_app', '0016_motherboard_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='graphiccard',
            name='price',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]