from django.contrib import admin

# Register your models here.
from .models import TransactionWorker
from .models import TransactionCommandCenter


# Register your models here.
admin.site.register(TransactionWorker)
admin.site.register(TransactionCommandCenter)