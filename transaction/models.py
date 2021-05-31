from django.db import models
from command_center.models import CommandCenter
from worker.models import Worker

# Create your models here.
class TransactionCommandCenter(models.Model):
    #id is automatically defined
    login_time = models.TimeField()
    login_date = models.DateField()
    logout_date = models.DateField()
    user_id=models.ForeignKey(CommandCenter,on_delete=models.CASCADE)

class TransactionWorker(models.Model):
    #id is automatically defined
    login_time = models.TimeField()
    login_date = models.DateField()
    logout_date = models.DateField()
    user_id=models.ForeignKey(Worker,on_delete=models.CASCADE)