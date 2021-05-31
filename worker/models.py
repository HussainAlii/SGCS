from django.db import models
from django.utils import timezone
from vehicle.models import Vehicle
from vehicle.models import Map_Vehicle
SessionID = "W1"
# Create your models here.
class Worker(models.Model):
    username = models.CharField(max_length = 128, default = '')
    password = models.CharField(max_length = 45)
    role = models.CharField(blank = True, max_length = 45)
    phone_number =models.CharField(max_length=15)
    code = models.CharField(max_length=45, blank=True)
    date_of_birth = models.DateField()
    country = models.CharField(max_length = 45, default = '')
    full_name = models.CharField(max_length = 128, default = '')
    enrol_date = models.DateField()
    isAvailable = models.BooleanField(default=True)

class WorkerVehicle(models.Model):
    assignment_date_begin = models.DateTimeField(auto_now_add=True)
    assignment_date_end = models.DateTimeField(blank = True,default=None,null=True)
    veh_id = models.ForeignKey(Vehicle, on_delete = models.CASCADE)
    worker_id = models.ForeignKey(Worker, on_delete = models.CASCADE)
    isTaskFinished = models.BooleanField(default=False)


def stopTask(workerId):
    vechicleObj = WorkerVehicle.objects.filter(worker_id=Worker.objects.filter(username=workerId).first()).first().veh_id
    WorkerVehicle.objects.filter(veh_id=vechicleObj, isTaskFinished=False).update(isTaskFinished=True)
    Map_Vehicle.objects.filter(veh_id=vechicleObj,isTaskFinished=False).update(isTaskFinished=True)



