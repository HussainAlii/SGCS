from django.db import models

# Create your models here.
class CommandCenter(models.Model):
    #id is automatically defined
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    role = models.CharField(max_length=45)
    phone_number =models.CharField(max_length=15)
    code=models.CharField(max_length=45,blank=True, default="")
    full_name = models.CharField(max_length=128, default='')
    gender = models.CharField(max_length=128, default='')
    country = models.CharField(max_length = 45, default = '')
    date_of_birth = models.DateField()
    enrol_date = models.DateField()
    isAdmin = models.BooleanField(default=False)
