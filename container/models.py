import string
import random

from django.db import models
from container.QR.qrcodegen import QrCode
from django.core import serializers
# Create your models here.

# Create your models here.
class PostCode(models.Model):
    post_code = models.IntegerField(primary_key=True)
    contCount = models.IntegerField()

class Container(models.Model):
    # id is automatically defined
    id = models.IntegerField(primary_key=True)
    lat = models.FloatField(default= -1)
    lng = models.FloatField(default= -1)
    capacity = models.IntegerField(default="1")
    request_count = models.IntegerField(default="0")
    post_code = models.ForeignKey(PostCode, on_delete=models.CASCADE, default='', blank=True, null=True)
    QRcode = models.CharField(max_length=45, default='', blank=True)
def createPostCode(postCodeNumber):
    #if postcode does not exist in system
    postCodeFiltered = PostCode.objects.filter(post_code=postCodeNumber)
    if postCodeFiltered.count()==0:
        # create post code
        postCodeFiltered = PostCode(post_code=postCodeNumber, contCount=1)
        postCodeFiltered.save()
    else:
        postCodeFiltered = postCodeFiltered.first()
        postCodeFiltered.contCount = int(postCodeFiltered.contCount) + 1
        postCodeFiltered.save()

    return postCodeFiltered

def getContCount():
    return PostCode.objects.all().order_by('post_code')

def getContByZipcode(postObjList):
    for zipcode in postObjList:
        Container.objects.filter(post_code=zipcode).all()
    return

def store_containers_prototype(containerObj):
    # if container does not exist in DB:

    while True:
        code = ''.join(random.choice(string.ascii_letters) for _ in range(6))
        QrCodeCount = Container.objects.filter(QRcode=code).count()
        if QrCodeCount == 0:
            post = createPostCode(int(containerObj["zip_code"]))
            Container(lat=containerObj["lat"], lng=containerObj["lng"], post_code=post, QRcode=code).save()
            break

def store_containers():
    # if container does not exist in DB:
    while True:
        code = ''.join(random.choice(string.ascii_letters) for _ in range(6))
        QrCodeCount = Container.objects.filter(QRcode=code).count()
        if QrCodeCount == 0:
            Container(QRcode=code).save()
            break

def remove_container(container):
    # reduce contContainer in postCode
    cont = Container.objects.filter(id = container['id']).first()
    postCodeFiltered = PostCode.objects.filter(post_code=cont.post_code.post_code).first()
    postCodeFiltered.contCount = int(postCodeFiltered.contCount) - 1
    postCodeFiltered.save()
    # removing container
    cont.delete()

def remove_last_container():
    #reduce contContainer in postCode
    lastContainer = Container.objects.last()
    postCodeFiltered = PostCode.objects.filter(post_code=lastContainer.post_code.pk).first()
    postCodeFiltered.contCount = int(postCodeFiltered.contCount) - 1
    postCodeFiltered.save()
    # removing container
    lastContainer.delete()

def remove_all_containers():
    Container.objects.all().delete()
    for post_code in  PostCode.objects.all():
        post_code.contCount = 0
        post_code.save()
    return getContCount()

def get_last_container_id():
    if Container.objects.all().count() == 0:
        return 0
    return Container.objects.values('id').last()["id"]

def get_qr_code(request):
    """Creates a single QR Code, then prints it to the console."""
    if request.method == 'POST':
        #text = "1"  # User-supplied Unicode text
        errcorlvl = QrCode.Ecc.HIGH  # Error correction level
        # Make and print the QR Code symbol
        qrcodeContainer = Container.objects.filter(id=request.POST.get("id", "")).first().QRcode
        qr = QrCode.encode_text(qrcodeContainer, errcorlvl).to_svg_str(4)
        return qr

def GetQR(qr):
    errcorlvl = QrCode.Ecc.HIGH  # Error correction level
    return QrCode.encode_text(qr, errcorlvl).to_svg_str(4)[138::]


# def getScndCont():
#     postCodes = PostCode.objects.values('post_code')
#     contIds = {}
    
#     for i in postCodes:
#         contIds.append(Container.objects.values_list('pk', post_code = i))


