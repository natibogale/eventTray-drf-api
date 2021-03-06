# Generated by Django 4.0.4 on 2022-05-20 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_remove_events_date_joined_events_date_added_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=150, verbose_name='City')),
                ('country', models.CharField(default='Ethiopia', max_length=150, verbose_name='Country')),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.AddField(
            model_name='venues',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Added'),
        ),
        migrations.AddField(
            model_name='venues',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.cities', verbose_name='City'),
        ),
    ]
