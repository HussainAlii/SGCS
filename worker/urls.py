from django.urls import path
from .views import about, faq_user, dashboard, collectContainer
from request.models import getContCoordzByWorker


urlpatterns = [
    path('', dashboard, name="worker_dashboard"),
    path('faq/', faq_user, name="worker_faq"),
    path('about/', about, name="worker_about"),
    #path('ajax/fetch/getContCoordzByWorker/', getContCoordzByWorker, name="getContCoordzByWorker"),
    path('ajax/post/collectContainer/', collectContainer, name="collectContainer"),
    # path('ajax/request/stopTask/', stopTask, name="stopTask"),

]
