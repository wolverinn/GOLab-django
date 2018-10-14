from django.db import models

# Create your models here.

# python manage.py makemigrations
# python manage.py migrate   
class User(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=30)
    email = models.EmailField
    phone = models.CharField(max_length=15)
# combo
    is_vip = models.BooleanField
    send_to_mail = models.BooleanField
    number_of_items = models.IntegerField
    check_frequency = models.IntegerField
    start_day = models.DateField
    time_span = models.IntegerField
# restrictions
    monitored_items = models.CharField(max_length=200)
    price_restrictions = models.CharField(max_length=200)
    wear_restrictions = models.CharField(max_length=200)
    rare_restrictions = models.CharField(max_length=200)

class CsgoApi(models.Model):
    buff_api = models.CharField(max_length=20,primary_key=True)
    igxe_api = models.CharField(max_length=20)