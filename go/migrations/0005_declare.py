# Generated by Django 2.1.1 on 2018-10-13 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('go', '0004_auto_20181010_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='Declare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('igxe_link', models.URLField(null=True)),
                ('buff_link', models.URLField(null=True)),
            ],
        ),
    ]
