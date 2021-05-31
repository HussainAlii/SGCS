from django.db import models
from container.models import PostCode

# Create your models here.
class Vehicle(models.Model):
    #id is automatically defined
    veh_id = models.CharField(max_length = 128, default = '')
    plate_num = models.TextField()
    miles = models.FloatField()
    veh_type = models.TextField()
    odometer = models.FloatField(null=True, blank=True, default=None)
    veh_model = models.CharField(max_length = 45, default = '')
    enrol_date = models.DateField(default='2007/1/1')
    isAvailable = models.BooleanField(default=True)

class Map_Vehicle(models.Model):
    map_id = models.IntegerField(default=None, null=True, blank=True)
    veh_id = models.ForeignKey(Vehicle, on_delete = models.CASCADE)
    post_code = models.ForeignKey(PostCode, on_delete = models.CASCADE, default='', blank=True)
    isTaskFinished = models.BooleanField(default=False)