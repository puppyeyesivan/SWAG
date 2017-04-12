import json
import datetime
import urllib.request
import time


d1=datetime.datetime(2016, 1, 1)
d2 = datetime.datetime(2016, 10, 19)
ltn=(d2-d1).days



for i in range (0,ltn):
    starttime=datetime.datetime.strftime( d2 -datetime.timedelta(days=i),"%Y-%m-%d")
    endtime=datetime.datetime.strftime( d2 -datetime.timedelta(days=i)+datetime.timedelta(days=1),"%Y-%m-%d")
    #print(starttime+endtime)
    time.sleep(0.1)
    response = urllib.request.urlopen('https://api-markets.wallstreetcn.com//v1/calendar.json?start='+starttime+'&end='+endtime)
    http=response.read()
    hjson = json.loads(http.decode())



    for i in range (0,len(hjson['results'])):
     country=hjson['results'][i]['country']
     ltime=hjson['results'][i]['localDateTime']
     title=hjson['results'][i]['title'].replace('                                                                        ','')
     act=hjson['results'][i]['actual']
     forcast=hjson['results'][i]['forecast']
     print(title)
