import pandas as pd
import pandas_datareader as pdr
import datetime
from . import models
from django.db import transaction,connection

#import os
#import django
#os.environ["DJANGO_SETTINGS_MODULE"] = 'project.settings'
#django.setup()


def get_data():
    print(str(datetime.datetime.now())+" get_data: Start")
    Signals=models.Signal.objects.all()
    end=datetime.datetime.now()
    for Sig in Signals:
        if (Sig.last_pull.date() < end.date()):
            if Sig.source=='yahoo':
                print("\t\ttry get: yahoo signal "+Sig.symbol)
                try:
                    start=Sig.last_pull
                    end=datetime.datetime.now()
                    df=pdr.get_data_yahoo(Sig.symbol,start,end).reset_index()
                    df.rename(columns={
                    u'Date':'time', 
                    u'Open':'open', 
                    u'High':'high', 
                    u'Low':'low', 
                    u'Close':'close', 
                    u'Volume':'volume', 
                    u'Adj Close':'adj_close'
                    }, inplace=True)
                    df['signal']=Sig
                    print("\t\tGot "+str(len(df))+" points, saving")
                    with transaction.atomic():
                        for record in df.to_dict(orient='records'):
                            models.HistoricalPrice.objects.update_or_create(time=record['time'],signal=record['signal'],defaults=record)
                        Sig.last_pull=end
                        Sig.save()
                    print("\t\tSaved")
                except Exception as e: print(e)
            print("\t"+str(Sig)+" Done")
    print("\tEnd")

def ping_job():
    print(str(datetime.datetime.now())+" ping finance")