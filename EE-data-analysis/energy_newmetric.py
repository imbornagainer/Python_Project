# -*- coding: utf-8 -*-
import pandas as pd
import time
import datetime
import requests
import json

def timeTOunixtime (rlt):
        #YYYY [0:4], MM [4:6], DD [6:8], HH [8:10], m[10:12]
        stime = "%s/%s/%s" %(rlt[6:8], rlt[4:6], rlt[0:4])
        h = rlt[8:10]

	if len(rlt) == 10: # without minutes
		m = '00'
	else:
        	m = rlt[10:12]

        #unixtime need to have 1 sec unit scale
        dechour = int(h)*60*60
        dechour += int(m)*60
        unixday = time.mktime(datetime.datetime.strptime(stime, "%d/%m/%Y").timetuple())
        unixtime = unixday + dechour

        return int(unixtime)

url = "http://125.140.110.217:4242/api/put"


response ={}
timelist=['2017060100','2016090100']
for time in timelist:
    uxtime = timeTOunixtime(time)
    data = {
        "metric": "energy",
        "timestamp": uxtime,
        "value": 430, #계측용량 혹은 설비용량(일정 비율을 곱한..값..)
        "tags": {
            "Saupjang": '1602220019' #사업장 번호->사업자 번호가 아니고 사업장 번호여야 함!!!!!

        }
    }
    ret = requests.post(url, data=json.dumps(data))

