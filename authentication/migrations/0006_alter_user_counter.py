# Generated by Django 4.0.4 on 2022-05-29 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_organizer_displayname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='counter',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
