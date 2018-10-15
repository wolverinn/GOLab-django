from django.db import models

# Create your models here.

# python manage.py makemigrations
# python manage.py migrate   
class User(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15)
# combo
    is_vip = models.BooleanField(default=False)
    send_to_mail = models.BooleanField(null=True)
    number_of_items = models.IntegerField(null=True)
    check_frequency = models.IntegerField(null=True)
    start_day = models.DateField(null=True)
    time_span = models.IntegerField(null=True)
# restrictions
    monitored_items = models.CharField(max_length=200)
    price_restrictions = models.CharField(max_length=200)
    wear_restrictions = models.CharField(max_length=200)
    rare_restrictions = models.CharField(max_length=200)

class CsgoApi(models.Model):
    buff_api = models.CharField(max_length=20,primary_key=True)
    igxe_api = models.CharField(max_length=20)
    buff_name = models.CharField(max_length=100)
    igxe_name = models.CharField(max_length=100)
    rarity = models.CharField(max_length=10)
    icon_url = models.URLField(null=True)
    catagory = models.CharField(max_length=30,null=True)