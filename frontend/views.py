import json
import urllib.request as req
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers
from container.models import Container, store_containers_prototype, remove_all_containers, remove_last_container, getContCount
from container.models import get_last_container_id as getId
from container.models import remove_container as removeContainer
from request.models import QrRequest, getScndCont, getUnderProccConts, collectContainerByCoords
from request.models import requestScanPrototype
from request.models import getContCoordz as ContCoordz
from container.models import get_qr_code


def getQrCode(request):
    """Creates a single QR Code, then prints it to the console."""
    if request.method == 'POST':
        return HttpResponse(get_qr_code(request), content_type="image/svg")

def Decode_Json_Request(request):
    response_json = json.dumps(request.POST)
    data = json.loads(response_json)
    return json.loads(data['serializedData'])

def home(request):
    if request.method == 'POST':
        return  HttpResponse(request)
    else:
        containers = serializers.serialize('json', reversed(Container.objects.all()))
        contList =  getContCount()
        scnd = getScndCont()
        scaned_container = serializers.serialize('json', getUnderProccConts())
        home_context = {
            'title': 'Home',
            'containers': containers,
            'contList': contList,
            'scnd': scnd,
            'scaned_container': scaned_container,           
        } 
        return render(request, 'home/map.html', home_context)


def getContainer(request):
    if request.method == 'POST':
        store_containers_prototype(Decode_Json_Request(request))
        return HttpResponse()
    """
    if request.is_ajax():
        message = "Yes, AJAX!"
    else:
        message = "Not Ajax"
    """

def removeLastContainer(request):
    if request.method == 'POST':
        remove_last_container()
        return HttpResponse()

def removeAllContainers(request):
    if request.method == 'POST':
        remove_all_containers()
        return HttpResponse()

def get_last_container_id(request):
    if request.method == 'POST':
        return HttpResponse(getId())

def requestScanCont(request):
    if request.method == 'POST':
        requestScanPrototype(request)
        return HttpResponse()

def remove_container(request):
    if request.method == 'POST':   
        removeContainer(Decode_Json_Request(request))
        return HttpResponse()

def getContCoordz(request):
    if request.method == 'POST':
        return HttpResponse(ContCoordz())

def collectContainer(request):
    if request.method == 'POST':
        return HttpResponse(str(collectContainerByCoords(Decode_Json_Request(request),'W1')))

