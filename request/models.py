import datetime
import json
import django
from django.contrib import messages
from django.db import models
from User.models import User
import math
import collections
from container.models import Container, getContCount, getContByZipcode
from itertools import groupby
from worker.models import WorkerVehicle, Worker, stopTask
from vehicle.models import Map_Vehicle, Vehicle

import datetime
# Create your models here.
from container.models import PostCode, createPostCode
def Decode_Json_Request(request):
    response_json = json.dumps(request.POST)
    data = json.loads(response_json)
    return json.loads(data['serializedData'])

class QrRequest(models.Model):
    #id is automatically defined
    rStatus= models.CharField(max_length=45)
    date = models.DateField()
    time = models.TimeField()
    national_number = models.ForeignKey(User, on_delete=models.CASCADE)
    cont_id = models.ForeignKey(Container, on_delete=models.CASCADE)
    RpW = models.IntegerField(default=0)
    post_code = models.IntegerField(default=0)

def getUnderProccConts():
    return QrRequest.objects.filter(rStatus = 'Processing')

def collectContainerByCoords(data, workerId):
    scannedContainers = QrRequest.objects.filter(rStatus = 'Processing').all()
    lat = data["lat"]
    lng = data["lng"]
    contId = None
    dist2d = 9999
    for coords in scannedContainers:
        contLat = coords.cont_id.lat
        contLng = coords.cont_id.lng
        currentdist2d = math.sqrt((lat-contLat)**2 + (lng-contLng)**2)
        if currentdist2d < dist2d:
            dist2d = currentdist2d
            contId = coords.cont_id.id
    assignAsCollected(contId,workerId)
    return contId

def assignAsCollected(id,worker_id):
    QrRequest.objects.filter(rStatus = 'Processing', cont_id=id).update(rStatus="Collected")
    #make sure if it is the last container for the worker
    if len(getWorkerAssignedConts(worker_id)) == 0:
        stopTask(worker_id)

def getScndCont():
    scannedCans = QrRequest.objects.filter(rStatus='Processing').values('cont_id')
    postCodeList = []

    for i in scannedCans:
        postCode = Container.objects.filter(id=i['cont_id']).values('post_code').first()
        postCodeList.append(postCode['post_code'])

    freqList = {value: len(list(freq)) for value, freq in groupby(sorted(postCodeList))}

    return freqList


def getWorkerAssignedConts(id):
    worker = Worker.objects.filter(username=id).first()
    if WorkerVehicle.objects.filter(worker_id=worker,isTaskFinished=False).all().count() > 0:
        vehId= WorkerVehicle.objects.filter(worker_id=worker,isTaskFinished=False).values("veh_id").first()['veh_id']
        postList = Map_Vehicle.objects.filter(veh_id=vehId, isTaskFinished=False).all()
        my_queryset = Container.objects.filter(id__in=[cont.cont_id_id for cont in QrRequest.objects.filter(post_code__in=[post.post_code_id for post in postList], rStatus='Processing').all()])
        return my_queryset if my_queryset else []
    return []

def getScndContByZipcode(scannedContList):

    scannedCans = QrRequest.objects.filter(rStatus='Processing').values('cont_id')
    postCodeList = []

    for i in scannedCans:
        postCode = Container.objects.filter(id=i['cont_id']).values('post_code').first()
        postCodeList.append(postCode['post_code'])

    freqList = {value: len(list(freq)) for value, freq in groupby(sorted(postCodeList))}

    return freqList

def requestScanCont(request):
    decodedRec = Decode_Json_Request(request)
    cont = Container.objects.filter(QRcode=decodedRec['code']).first()
    if cont:
        if cont.lat == -1:
            if decodedRec['lat'] == -1 or decodedRec['postcode'] == 404:
                messages.error("We Could Not Get Your Current Location :(")
                return False
            createPostCode(decodedRec['postcode'])
            Container.objects.filter(QRcode=decodedRec['code']).update(lat = decodedRec['lat'], lng = decodedRec['lng'], post_code=PostCode.objects.filter(post_code=decodedRec['postcode']).first())
    else:
        messages.error(request, 'Invalid code :(!')
        return False

    qrReq = QrRequest.objects.filter( cont_id__QRcode= decodedRec['code'], rStatus = 'Processing').first()
    container = Container.objects.filter(QRcode=decodedRec['code']).values("post_code").first()
    if not container:
        messages.error(request, 'Invalid code :(!')
        return False
    zipcode = container["post_code"]

    if not qrReq:
        container = Container.objects.filter(QRcode=decodedRec['code'])
        dummyUser = User.objects.filter(national_number=request.session['username']).first()
        container.update(request_count=container.values("request_count").first()["request_count"]+1)
        QrRequest(rStatus = 'Processing', date = datetime.date.today(), time = datetime.datetime.now(), national_number = dummyUser, cont_id =container.first(), post_code= container.values('post_code_id').first()["post_code_id"]).save()
        obj = User.objects.filter(national_number=dummyUser.national_number).values('points').first()
        obj['points'] +=1
        User.objects.filter(national_number=dummyUser.national_number).update(points = obj['points'])
        request.session['points'] = User.objects.filter(national_number=request.session['username']).values("points").first().get('points')
        messages.success(request, 'Your Request is being processed ;)')
        return True
    messages.error(request, 'This Container Is Already Scanned')
    return False

def requestScanPrototype(request):
    request = Decode_Json_Request(request)
    qrReq = QrRequest.objects.filter(cont_id=request['id'], rStatus='Processing').first()
    if not qrReq:
        dummyUser = User.objects.first()
        cont = Container.objects.filter(id=request['id']).first()
        QrRequest(rStatus=request['status'], date='2021-02-21', time='11:16:01', national_number=dummyUser,
                  cont_id=cont).save()
        return True
    return False

    
#Retrieves the coordinates of scanned containers
def getContCoordz():
    contList = QrRequest.objects.filter(rStatus='Processing').all()
    coordzList = ""

    for i in contList:
       containerCoordz = ""
       containerCoordz+=str(i.cont_id.lng)+","+str(i.cont_id.lat)
       coordzList+=containerCoordz+";"
    return coordzList

#Retrieves the coordinates of scanned containers for each worker
def getContCoordzByWorker(request):
    contList = getWorkerAssignedConts(request.session['username'])
    coordzList = ""

    for i in contList:
       containerCoordz = ""
       containerCoordz+=str(i.cont_id.lng)+","+str(i.cont_id.lat)
       coordzList+=containerCoordz+";"
    return coordzList
 


class RecycableRequest(models.Model):
    # id is automatically defined
    rStatus = models.CharField(max_length=45)
    date = models.DateField()
    time = models.TimeField()
    national_number = models.ForeignKey(User,on_delete=models.CASCADE)

class CleaningRequest(models.Model):
    # id is automatically defined
    rStatus = models.CharField(max_length=45)
    date = models.DateField()
    time = models.TimeField()
    national_number = models.ForeignKey(User,on_delete=models.CASCADE)
