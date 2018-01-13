# -*- coding: utf-8 -*-

import time as newtime
import datetime
import requests
import json
import sys
import _sanum_kw_ #input list file 사업장번호 / 목표측정량

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
        unixday = newtime.mktime(datetime.datetime.strptime(stime, "%d/%m/%Y").timetuple())
        unixtime = unixday + dechour

        return int(unixtime)

url = "http://125.140.110.217:4242/api/put"
timelist=['2017060100','2016090100','2017022800','2016010100','2016110103']

installsize_list=_sanum_kw_._sanum_kw_list
last = len(installsize_list)
count = 0
for installdata in installsize_list:
    count = count + 1
    sys.stdout.write("   on going = %.1f percentage \r" %float(100 * count / last) )
    sys.stdout.flush()
    for time in timelist:
        uxtime = timeTOunixtime(time)
        data = {
            "metric": "rc_001_target_watt", #2017/6/27 kjh,
            "timestamp": uxtime,
            "value": installdata[1], #설비용량(일정 비율을 곱한..값..)
            "tags": {
                "Saupjang": installdata[0] #사업장 번호->사업자 번호가 아니고 사업장 번호여야 함!!!!!
            }
        }
        #print data
        try:
            ret = requests.post(url, data=json.dumps(data))
        except requests.exceptions.ConnectionError as e:
            print count
            print e
            pass
