import json
import urllib.request as req
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers
from request.models import getWorkerAssignedConts, collectContainerByCoords
from request.models import getContCoordzByWorker as ContCoordzWorker
from worker.models import stopTask as stopTaskModel

# Create your views here.
def Decode_Json_Request(request):
    response_json = json.dumps(request.POST)
    data = json.loads(response_json)
    return json.loads(data['serializedData'])

def dashboard(request):
        # get worker containers
    if "username" in request.session:
        if request.session['username'][0] == "W":
            assignedConts = getWorkerAssignedConts(request.session['username'])
            if assignedConts:
                scaned_container = serializers.serialize('json', assignedConts)
            else:
                scaned_container = None
            home_context = {
                'title': 'Home',
                'scaned_container': scaned_container,
            }
            return render(request, 'static/worker_dashboard.html', home_context)

    return render(request, 'static/worker_dashboard.html')

def faq_user(request):
    return render(request,'static/worker_faq.html',{'title': 'FAQ'})

def about(request):
    return render(request,'static/worker_about.html',{'title': 'About'})

def getContCoordzByWorker(request):
    if request.method == 'POST':
        return HttpResponse(ContCoordzWorker())

def collectContainer(request):
    if request.method == 'POST':
        return HttpResponse(str(collectContainerByCoords(Decode_Json_Request(request),request.session['username'])))


# def stopTask(request):
#     if request.method == 'POST':
#         stopTaskModel(request)
#     return HttpResponse()