# Generated by Django 2.1.1 on 2018-10-09 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('go', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='csgoapi',
            name='icon_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='check_frequency',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_vip',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='number_of_items',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='send_to_mail',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='start_day',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='time_span',
            field=models.IntegerField(null=True),
        ),
    ]
