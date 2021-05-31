from django.urls import path
from .views import faq_user, my_request, collection_request, recycling_request, cleaning_request, about, dashboard, \
    getUserReqInfo, setScanned

urlpatterns = [
    path('collection_request/ajax/request/setScanned/', setScanned, name="setScanned"),
    path('collection_request/ajax/post/setScanned/', setScanned, name="setScanned"),
    path('', dashboard, name="user_dashboard"),
    path('faq_user/', faq_user, name="faq_user"),
    path('my_request/', my_request, name="my_request"),
    path('collection_request/', collection_request, name="collection_request"),
    path('recycling_request/', recycling_request, name="recycling_request"),
    path('cleaning_request/', cleaning_request, name="cleaning_request"),
    path('about/', about, name="user_about"),
    path('my_request/ajax/request/getUserReqInfo', getUserReqInfo, name="getUserReqInfo"),

]
