import json
import math
import random
from itertools import groupby

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from request.models import getUnderProccConts
from worker.models import Worker, WorkerVehicle
from command_center.models import CommandCenter
from vehicle.models import Vehicle as Truck, Map_Vehicle
from command_center.models import CommandCenter as Emp
from User.models import User
import datetime
from container.models import Container, get_qr_code, PostCode, store_containers
from container.models import GetQR
from request.models import QrRequest
from django.db.models import Q
# Create your views here.

def Decode_Json_Request(request):
    response_json = json.dumps(request.POST)
    data = json.loads(response_json)
    return json.loads(data['serializedData'])


def add_worker(request):
    if Worker.objects.count() > 0:
        worker = Worker.objects.values('id').last()
        id = 'W' + str(int(worker['id']) + 1)
    else:
        id = 'W' + str(1)

    if request.method == 'POST':
        if not Worker.objects.filter(username=request.POST['username']).exists():
            Worker(username=request.POST['username'], password=request.POST['password'], role=request.POST['role'],
                   phone_number=request.POST['phone_number'], date_of_birth=request.POST['date'],
                   full_name=request.POST['fullname'],
                   enrol_date=datetime.date.today(),
                   country=request.POST['country']).save()
            print('A new worker has been added')
            return redirect('../add_worker')
        else:
            print('A worker with that name already exists')
            return redirect('../add_worker')

    return render(request, 'static/add_worker.html', {'title': "Add worker", 'id': id})


def dashboard(request):
    return render(request, 'static/dashboard.html',
                  {'title': "home", 'empCount': getEmpCount(), 'userCount': getUserCount(),
                   'contCount': getContainerCount(),'workersCount': Worker.objects.all().count(), 'postCount': getPostCodeCount(), 'todayRecs': getReqByDate(),
                   'genders': getGenderPercentage(), 'country': getCountryPercentage(), 'analytics':serializers.serialize('json', getPostCodeWithContCount())})


def requests(request):
    return render(request, 'static/requests.html', {'title': "requests"})


def requests_frequency(request):
    return render(request, 'static/requests-frequency.html', {'title': "requests frequency"})


def trucks(request):
    return render(request, 'static/trucks.html', {'title': "trucks"})


def collection_time(request):
    return render(request, 'static/collection-time.html', {'title': "collection time"})


def numbers(request):
    return render(request, 'static/numbers.html', {'title': "numbers"})


def add_team(request):
    return render(request, 'static/add-team.html', {'title': "add team"})


def add_employee(request):
    if CommandCenter.objects.count() > 0:
        employee = CommandCenter.objects.values('id').last()
        id = 'E' + str(int(employee['id']) + 1)
    else:
        id = 'E' + str(1)

    if request.method == 'POST':
        if request.POST['role'] == "Admin":
            bAdmin = True
        else:
            bAdmin = False

        if not CommandCenter.objects.filter(username=request.POST['username']).exists():
            CommandCenter(username=request.POST['username'], password=request.POST['password'],
                          role=request.POST['role'],
                          phone_number=request.POST['phone_number'], date_of_birth=request.POST['dob'],
                          full_name=request.POST['fullname'],
                          gender=request.POST['gender'],
                          enrol_date=datetime.date.today(),
                          country=request.POST['country'],
                          isAdmin=bAdmin).save()  # I wanted to use the unary if operator, but python is bad :(
            print('A new command center employee has been added')
            return redirect('../add_employee')
        else:
            print('A worker with that name already exists')
            return redirect('../add_employee')
    return render(request, 'static/add-employee.html', {'title': "add employee", 'id': id})


def add_truck(request):
    if Truck.objects.count() > 0:
        vehicle = Truck.objects.values('id').last()
        id = 'T' + str(int(vehicle['id']) + 1)
    else:
        id = 'T' + str(1)

    if request.method == 'POST':
        Truck(veh_id=request.POST['id'],
              veh_type=request.POST['type'],
              veh_model=request.POST['model'],
              plate_num=request.POST['plate'],
              odometer=request.POST['odomtr'],
              miles=0,
              enrol_date=datetime.date.today()).save()
        return redirect('../add_truck')

    return render(request, 'static/add-truck.html', {'title': "add truck", 'id': id})


def logs(request):
    return render(request, 'static/logs.html', {'title': "logs"})


def generateMap(request):
    scaned_container =[]
    staffMembers = []
    busyTrucksList= WorkerVehicle.objects.filter(veh_id__in=Truck.objects.filter(isAvailable=True).all(), isTaskFinished=False).values("veh_id").distinct().all()
    if "selectedMap" not in request.session: request.session["selectedMap"] = "All"
    if request.session["selectedMap"] == "All":
        containers = serializers.serialize('json', reversed(Container.objects.all()))
        scaned_container = serializers.serialize('json', getUnderProccConts())
    else:
        containers = serializers.serialize('json', reversed(getMapByTruck(request.session["selectedMap"])))
        staffMembers = getStaffMembers(request.session["selectedMap"])

    return render(request, 'static/generateMap.html',
                  {'title': "Generate Map", 'containers': containers, 'scaned_container': scaned_container,"selectedMap": request.session["selectedMap"],"busyTrucksList":busyTrucksList, 'staff':staffMembers})


def getQrCode(request):
    """Creates a single QR Code, then prints it to the console."""
    if request.method == 'POST':
        return HttpResponse(get_qr_code(request), content_type="image/svg")


def getSelectedData(selected):
    return {
        'Emp': Emp.objects.values("phone_number", "full_name", "gender", "country", "enrol_date").all(),
        'Worker': Worker.objects.values("phone_number", "country", "full_name", "enrol_date", "isAvailable").all(),
        "Truck": Truck.objects.values("plate_num", "miles", "veh_type", "odometer", "veh_model", "enrol_date",
                                      "isAvailable").all(),
        "User": User.objects.values("phone_number", "points").all(),
        "QR": Container.objects.values("id", "lat", "lng", "post_code__post_code", "request_count", "QRcode").all(),
        "Postcode": PostCode.objects.values("post_code", "contCount").all()
    }[selected]

def invertTruckIsChecked(request):
    if request.method == 'POST':
        request.session["isCheckedTruck"] = not request.session["isCheckedTruck"]
    return HttpResponse()


def invertWorkerIsChecked(request):
    if request.method == 'POST':
        request.session["isCheckedWorker"] = not request.session["isCheckedWorker"]
    return HttpResponse()


def getQrImg(data):
    QrList = []
    for qr in data:
        QrList.append(GetQR(qr["QRcode"]))
    return QrList

def getScndCont():
    postList = PostCode.objects.all()
    scandList = []
    for post in postList:
        scandList.append(QrRequest.objects.filter(rStatus='Processing',post_code=post.post_code).values('cont_id').count())
    return scandList

def getScndContByPostcode(postcode):
    return QrRequest.objects.filter(rStatus='Processing',post_code=PostCode.objects.filter(post_code=postcode).first().post_code).count()

def archive(request):
    QRimage = None
    Entity = None
    if "isSelected" not in request.session: request.session["isSelected"] = "Emp"
    data = getSelectedData(request.session["isSelected"])
    if request.session["isSelected"] == "QR":
        QRimage = getQrImg(data)
        Entity = zip(data, QRimage)
    elif request.session["isSelected"] == "Postcode":
        totalscanedcont = getScndCont()
        Entity = zip(data, totalscanedcont)
    else:
        Entity = data

    numbers = [CommandCenter.objects.all().count(), Worker.objects.all().count(), Truck.objects.all().count(),
               User.objects.all().count(), Container.objects.all().count(), PostCode.objects.all().count()]
    if "isCheckedWorker" not in request.session: request.session["isCheckedWorker"] = False
    if "isCheckedTruck" not in request.session: request.session["isCheckedTruck"] = False
    return render(request, 'static/archive.html',
                  {'title': "archive", "Entity": Entity, "type": request.session["isSelected"], "nums": numbers,
                   "isCheckedWorker": request.session["isCheckedWorker"],
                   "isCheckedTruck": request.session["isCheckedTruck"]})


def faq(request):
    return render(request, 'static/faq.html', {'title': "faq"})


def about(request):
    return render(request, 'static/about.html', {'title': "about"})

def printQR(request):
    data= getSelectedData('QR')
    QRimage = getQrImg(data)
    QR = zip(data, QRimage)
    return render(request, 'static/printQR.html', {'title': "printQR",'Data':QR})

def updateComCenSelected(request):
    if request.method == 'POST':
        request.session["isSelected"] = Decode_Json_Request(request)["entType"]
    return HttpResponse()


def setAvailability(entity):
    if entity.method == 'POST':
        entity = Decode_Json_Request(entity)
        if entity['entType'] == 'Worker':
            Worker.objects.update(isAvailable=entity['status'])
        else:
            Truck.objects.update(isAvailable=entity['status'])

    return HttpResponse()


def setAvailabilityByEntity(entity):
    if entity.method == 'POST':
        entity = Decode_Json_Request(entity)
        if entity['entType'] == 'Worker':
            status = Worker.objects.filter(username=entity['ID']).values('isAvailable')[0]["isAvailable"]
            status = not status
            Worker.objects.filter(username=entity['ID']).update(isAvailable=bool(status))
        else:
            status = Truck.objects.filter(veh_id=entity['ID']).values('isAvailable')[0]["isAvailable"]
            status = not status
            Truck.objects.filter(veh_id=entity['ID']).update(isAvailable=bool(status))
    return HttpResponse()


def getEmpCount():
    return CommandCenter.objects.all().count()


def getUserCount():
    return User.objects.all().count()


def getContainerCount():
    return Container.objects.filter(~Q(lat='-1.0')).all().count()

def getPostCodeCount():
    return PostCode.objects.all().count()


def getReqByDate():
    return QrRequest.objects.filter(date=datetime.date.today()).all().count()


def getGenderPercentage():
    maleCount = CommandCenter.objects.filter(gender='Male').all().count()
    femaleCount = CommandCenter.objects.filter(gender='Female').all().count()
    malePerc = (maleCount / (maleCount + femaleCount) * 100)
    genderPerc = {'males': "%.2f" % malePerc, 'females': "%.2f" % (100 - malePerc)}
    return genderPerc


def getCountryPercentage():
    wrkerCountSA = Worker.objects.filter(country='Saudi Arabia').all().count() + CommandCenter.objects.filter(
        country='Saudi Arabia').all().count()

    wrkerCountBang = Worker.objects.filter(country='Bangladesh').all().count() + CommandCenter.objects.filter(
        country='Bangladesh').all().count()

    wrkerCountIndia = Worker.objects.filter(country='India').all().count() + CommandCenter.objects.filter(
        country='India').all().count()

    wrkerCountPak = Worker.objects.filter(country='Pakistan').all().count() + CommandCenter.objects.filter(
        country='Pakistan').all().count()

    wrkerCountPhil = Worker.objects.filter(country='Philippines').all().count() + CommandCenter.objects.filter(
        country='Philippines').all().count()

    totalCount = Worker.objects.all().count() + CommandCenter.objects.all().count()  # wrkerCountSA + wrkerCountBang + wrkerCountIndia + wrkerCountPak + wrkerCountPhil

    perOfSA = wrkerCountSA / totalCount * 100

    perOfBang = wrkerCountBang / totalCount * 100

    perOfIndia = wrkerCountIndia / totalCount * 100

    perOfPak = wrkerCountPak / totalCount * 100

    perOfPhil = wrkerCountPhil / totalCount * 100

    countryPer = {'SA': "%.2f" % perOfSA, 'bang': "%.2f" % perOfBang, 'india': "%.2f" % perOfIndia,
                  'pak': "%.2f" % perOfPak, 'phil': "%.2f" % perOfPhil,
                  'other': "%.2f" % (100 - (perOfSA + perOfBang + perOfIndia + perOfPak + perOfPhil))}

    return countryPer


def freeUpWorkers(request):
    WorkerVehicle.objects.filter(isTaskFinished=False).update(isTaskFinished=True)
    Map_Vehicle.objects.filter(isTaskFinished=False).update(isTaskFinished=True)
    #WorkerVehicle.objects.all().delete()
    #Map_Vehicle.objects.all().delete()
    request.session["selectedMap"] = "All"
    messages.info(request, 'Processed successfully!')
    return HttpResponse()


def getAvailableWotkers():
    workersList = Worker.objects.filter(isAvailable=True)
    busyWorkersList = WorkerVehicle.objects.filter(worker_id__in=Worker.objects.filter(isAvailable=True).all(),
                                                   isTaskFinished=False).all()
    availableWorkersList = []

    for worker in workersList:
        isBusy = False
        for busyWorker in busyWorkersList:
            if worker.username == busyWorker.worker_id.username:
                isBusy = True
                break

        if not isBusy:
            availableWorkersList.append(worker)
    return availableWorkersList


def getAvailableTrucks():
    trucksList = Truck.objects.filter(isAvailable=True)
    busyTrucksList = WorkerVehicle.objects.filter(veh_id__in=Truck.objects.filter(isAvailable=True).all(),
                                                  isTaskFinished=False).all()
    availableTrucksList = []

    for truck in trucksList:
        isBusy = False
        for busyTruck in busyTrucksList:
            if truck.veh_id == busyTruck.veh_id.veh_id:
                isBusy = True
                break

        if not isBusy:
            availableTrucksList.append(truck)
    return availableTrucksList

def distribute_workers(workerPerTruck):
    availableWorkersList = getAvailableWotkers()
    availableTrucksList = getAvailableTrucks()

    if len(availableWorkersList) >= int(workerPerTruck):
        if len(availableTrucksList) != 0:
            # choose random truck
            truckChoice = random.choice(availableTrucksList)
            # choose random worker
            group = []
            numberChoice = int(workerPerTruck)
            while (numberChoice):
                workerChoice = random.choice(availableWorkersList)
                if workerChoice not in group:
                    group.append(workerChoice)
                    numberChoice = numberChoice - 1
                else:
                    continue

            for worker in group:
                # add WorkerVehicle
                WorkerVehicle(veh_id=truckChoice, worker_id=worker, isTaskFinished=False).save()
            return distribute_workers(workerPerTruck)
    return availableTrucksList


def distribute_postcodes(lowerBound):
    assignedBusyTrucksList=[]
    filteredAssignedBusyTrucksList =[]
    #get all busy trucks
    for worker_truck in WorkerVehicle.objects.filter(veh_id__in=Truck.objects.filter(isAvailable=True).all(), isTaskFinished=False).values("veh_id").distinct().all():
        assignedBusyTrucksList.append(Truck.objects.filter(veh_id="T"+str(worker_truck["veh_id"])).all())
    # filter busy tucks based on existing of map_vehicle table
    for busyTruck in assignedBusyTrucksList:
        if {'veh_id':busyTruck[0].id} not in Map_Vehicle.objects.filter(isTaskFinished=False).values("veh_id").distinct().all():
            filteredAssignedBusyTrucksList.append(busyTruck)
    if len(filteredAssignedBusyTrucksList) != 0:
        postcodes = PostCode.objects.all().order_by('post_code')
        postcodesList = []
        for postcode in postcodes:
            #number of containers in the postcode
            numberOfCount = postcode.contCount
            if QrRequest.objects.filter(rStatus="Processing", post_code=postcode.post_code).count() ==0:
                continue

            totalPercentage = numberOfCount*lowerBound/100

            if (getScndContByPostcode(postcode.post_code) / postcode.contCount >= totalPercentage) and (postcode.contCount != 0):
                postcodesList.append(postcode)
        dividedNumber = int(len(postcodesList) / len(filteredAssignedBusyTrucksList))
        remainingNumber = len(postcodesList) % len(filteredAssignedBusyTrucksList)
        index = 0
        for truck in filteredAssignedBusyTrucksList:
            for counter in range(dividedNumber):
                Map_Vehicle(veh_id=truck[0],post_code=postcodesList[index]).save()
                index= index + 1

        truckIndex = len(filteredAssignedBusyTrucksList)-1
        if remainingNumber:
            for counter in range(remainingNumber):
                if len(postcodesList) == index:
                    break
                Map_Vehicle(veh_id=filteredAssignedBusyTrucksList[truckIndex][0],post_code=postcodesList[index]).save()
                index= index + 1
                truckIndex = truckIndex -1

            #make sure last truck get all the pain :)
            if truckIndex == 0:
                while index != len(postcodesList)-1:
                    try:
                        Map_Vehicle(veh_id=filteredAssignedBusyTrucksList[truckIndex][0], post_code=postcodesList[index]).save()
                        index = index + 1
                    except: break

def deleteAdditionalMaps():
    for workerVeh in WorkerVehicle.objects.filter(isTaskFinished=False).all():
        isExist = False
        for mapVeh in Map_Vehicle.objects.filter(isTaskFinished=False):
            if workerVeh.veh_id == mapVeh.veh_id:
                isExist = True
                break

        if isExist == False:
            workerVeh.delete()

def generateSectorizedMaps(request):
    messages.info(request, 'Processed successfully!')
    if QrRequest.objects.all().count() > 0 and QrRequest.objects.filter(rStatus="Processing").count() > 0:
        distribute_workers(Decode_Json_Request(request)["workerPerTruck"])
        lowerBound = Decode_Json_Request(request)["lowerBound"]
        distribute_postcodes(int(lowerBound[:len(lowerBound)-1]))
        deleteAdditionalMaps()
    return HttpResponse()

def getMapByTruck(vehId):
    postList = Map_Vehicle.objects.filter(veh_id=vehId, isTaskFinished=False).all()
    my_queryset = Container.objects.filter(id__in=[cont.cont_id_id for cont in QrRequest.objects.filter(post_code__in=[post.post_code_id for post in postList], rStatus='Processing').all()])
    return my_queryset if my_queryset else []

def getStaffMembers(vehId):
    list = []
    for i in WorkerVehicle.objects.filter(veh_id=vehId, isTaskFinished=False).values('worker_id').all():
        list.append(("W"+str(i['worker_id'])))
    return list




def setSelectedMap(request):
    if request.method == 'POST':
        request.session["selectedMap"]=Decode_Json_Request(request)
    return HttpResponse()

def generateContainers(request):
    if request.method == 'POST':
       request =  Decode_Json_Request(request)

       for cont in range(int(request['count'])):
           store_containers()

       print(request['count'])

    return HttpResponse()


def getPostCodeWithContCount():
    postCodeList = PostCode.objects.all()
    return postCodeList
