# Generated by Django 4.1.7 on 2023-04-06 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Metr', '0006_task_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='loservalue',
            name='lastFill',
            field=models.BooleanField(default=False),
        ),
    ]
