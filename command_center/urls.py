from django.urls import path
from .views import add_worker, dashboard, requests,about,faq,archive,logs,add_truck,add_team, add_employee, numbers, collection_time, trucks, requests_frequency, updateComCenSelected,\
    setAvailability, setAvailabilityByEntity, invertTruckIsChecked, invertWorkerIsChecked, generateMap,getQrCode,freeUpWorkers, generateSectorizedMaps,setSelectedMap, generateContainers,printQR
urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('add_worker/', add_worker, name="add_worker"),
    path('requests/', requests, name="requests"),
    path('generateMap/', generateMap, name="generateMap"),
    path('about/', about, name="about"),
    path('faq/', faq, name="faq"),
    path('printQR/', printQR, name="printQR"),
    path('archive/', archive, name="archive"),
    path('logs/', logs, name="logs"),
    path('add_truck/', add_truck, name="add_truck"),
    path('add_team/', add_team, name="add_team"),
    path('add_employee/', add_employee, name="add_employee"),
    path('numbers/', numbers, name="numbers"),
    path('collection_time/', collection_time, name="collection_time"),
    path('trucks/', trucks, name="trucks"),
    path('requests_frequency/', requests_frequency, name="requests_frequency"),
    path('generateMap/ajax/post/getQrCode/', getQrCode, name="getQrCode"),
    path('generateMap/ajax/request/freeUpWorkers/', freeUpWorkers, name="freeUpWorkers"),
    path('generateMap/ajax/post/generateSectorizedMaps/', generateSectorizedMaps, name="generateSectorizedMaps"),
    path('generateMap/ajax/post/setSelectedMap/', setSelectedMap, name="setSelectedMap"),
    path('archive/ajax/post/updateComCenSelected/', updateComCenSelected, name="updateComCenSelected"),
    path('archive/ajax/post/setAvailability/', setAvailability, name="setAvailability"),
    path('archive/ajax/post/setAvailabilityByEntity/', setAvailabilityByEntity, name="setAvailabilityByEntity"),
    path('archive/ajax/request/invertTruckIsChecked/', invertTruckIsChecked, name="invertTruckIsChecked"),
    path('archive/ajax/request/invertWorkerIsChecked/', invertWorkerIsChecked, name="invertWorkerIsChecked"),
    path('archive/ajax/post/generateContainers/', generateContainers, name="generateContainers"),


]
