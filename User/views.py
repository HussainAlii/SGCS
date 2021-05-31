import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from request.models import QrRequest, requestScanCont
from django.contrib import messages

# Create your views here.
def Decode_Json_Request(request):
    response_json = json.dumps(request.POST)
    data = json.loads(response_json)
    return json.loads(data['serializedData'])


def dashboard(request):
    return render(request,'static/user_dashboard.html',{'title': 'Home','data': getUserReqInfo(request)})

def collection_request(request):
    return render(request,'static/collection-request.html',{'title': 'Collection Request'})

def recycling_request(request):
    return render(request,'static/recycling-request.html',{'title': 'Recycling Request'})

def cleaning_request(request):
    return render(request,'static/cleaning-request.html',{'title': 'Cleaning Request'})

def my_request(request):
    return render(request,'static/my-request.html',{'title': 'My Request'})

def faq_user(request):
    return render(request,'static/faq-user.html',{'title': 'FAQ'})

def about(request):
    return render(request,'static/user_about.html',{'title': 'About'})

def getUserReqInfo(request):
    request = QrRequest.objects.filter(national_number=request.session['username']).values('rStatus', 'cont_id', 'date', 'time', 'post_code').all().order_by('date', 'time')[::-1]
    return request


def setScanned(request):
    if request.method == 'POST':
        requestScanCont(request)
    return HttpResponse("")
