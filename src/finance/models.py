from __future__ import unicode_literals

from django.db import models
import datetime

class Signal(models.Model):
    symbol=models.CharField(max_length=50,primary_key=True,unique=True)
    source=models.CharField(max_length=50)
    name=models.CharField(max_length=200)
    last_pull=models.DateTimeField('date published',default=datetime.datetime.utcfromtimestamp(0))
    def __str__(self):
        return str(self.symbol)
    def __unicode__(self):
        return unicode(self.symbol)

class HistoricalPrice(models.Model):
    signal=models.ForeignKey('Signal',on_delete=models.CASCADE,)
    open=models.FloatField()
    high=models.FloatField()
    low=models.FloatField()
    close=models.FloatField()
    volume=models.FloatField()
    adj_close=models.FloatField()
    time=models.DateTimeField()
    class Meta:
        unique_together = (("signal", "time"),)
    def __str__(self):
        return str(self.signal)+"-"+str(self.time)
    def __unicode__(self):
        return unicode(str(self.signal)+"-"+str(self.time))
    