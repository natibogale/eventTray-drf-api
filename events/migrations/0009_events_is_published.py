# Generated by Django 4.0.4 on 2022-05-14 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]