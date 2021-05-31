from django.contrib import admin
from .models import QrRequest
from .models import CleaningRequest
from .models import RecycableRequest

# Register your models here.
admin.site.register(QrRequest)
admin.site.register(CleaningRequest)
admin.site.register(RecycableRequest)