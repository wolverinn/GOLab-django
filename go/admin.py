from django.contrib import admin
from go import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.CsgoApi)
admin.site.register(models.Declare)