# Generated by Django 4.0.4 on 2022-06-12 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0009_ticketsbought_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketsbought',
            name='ticketName',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Ticket Name'),
        ),
    ]
