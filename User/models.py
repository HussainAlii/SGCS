from django.db import models

# Create your models here.
class User(models.Model):
    #id is automatically defined
    national_number = models.IntegerField(primary_key=True)
    password = models.CharField(max_length = 45)
    points = models.IntegerField(default=0)
    phone_number =models.CharField(max_length=15)
    code = models.CharField(max_length=45, blank=True)

