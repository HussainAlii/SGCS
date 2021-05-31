from django.urls import path
from .views import home
from .views import getContainer, removeLastContainer, removeAllContainers, get_last_container_id, requestScanCont, remove_container, \
    getContCoordz, getQrCode, collectContainer

urlpatterns = [
    path('', home, name="home"),
    path('ajax/post/getContainer/', getContainer, name="getContainer"),
    path('ajax/request/removeLastContainer/', removeLastContainer, name="removeLastContainer"),
    path('ajax/request/removeAllContainers/', removeAllContainers, name="removeAllContainers"),
    path('ajax/fetch/get_last_container_id/', get_last_container_id, name="get_last_container_id"),
    path('ajax/post/requestScanCont/', requestScanCont, name="requestScanCont"),
    path('ajax/post/remove_container/', remove_container, name="remove_container"),
    path('ajax/post/getQrCode/', getQrCode, name="getQrCode"),
    path('ajax/fetch/getContCoordz/', getContCoordz, name="getContCoordz"),
    path('ajax/post/collectContainer/', collectContainer, name="collectContainer"),
]
