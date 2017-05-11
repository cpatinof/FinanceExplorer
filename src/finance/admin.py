from django.contrib import admin
from .models import Signal,HistoricalPrice
# Register your models here.

admin.site.register(Signal)
admin.site.register(HistoricalPrice)