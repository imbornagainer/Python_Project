# -*- coding: utf-8 -*-
# Author : eunsooLim , https://github.com/eunsooLim
# Author : jeonghoonkang , https://github.com/jeonghoonkang

import pandas as pd
import time
import datetime
import cx_Oracle
import os
import sys
import requests
import json
import argparse
import mdsid_info
from types import *
import oracle_info_161024
import time, datetime
import infotest

#url = "http://125.140.110.217:4242/api/put"
url = "http://49.254.13.34:4242/api/put"
response ={}

con = cx_Oracle.connect('keti_user/keti1357!#@125.141.144.149/aimir')
cur = con.cursor()

timezone=[('00','09'),('09','12'),('12','13'),('13','18'),('18','23')]

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



# update 15 minutes one TSDB
def updateMINONE(in_sttime, in_entime,in_mdsid,tagdata):

        starttime = in_sttime
        endtime = in_entime
        mdsid = in_mdsid

        sql_tmp = "select ELE.LP_TIME, ELE.VALUE_00, ELE.VALUE_15, ELE.VALUE_30, ELE.VALUE_45, ECU.NAME, ECO.LOCATION, ECO.SIC, ELE.MDS_ID, ELE.DEVICE_SERIAL, ECU.CUSTOMERNO, ELE.CHANNEL from EMNV_LP_EM_VIEW  ELE join EMNV_CONTRACT_VIEW ECO on ELE.MDS_ID = ECO.MDS_ID join EMNV_CUSTOMER_VIEW ECU on ECO.CUSTOMERNO = ECU.CUSTOMERNO where (ELE.CHANNEL=1) and (ELE.LP_TIME between '%s' and '%s') and (ELE.MDS_ID='%s') order by ELE.MDS_ID ASC, ELE.LP_TIME ASC" %(starttime, endtime, mdsid)

	minlist = ['00', '15', '30', '45']
        timedic={0:0.0,1:0.0,2:0.0,3:0.0,4:0.0}
	lcfm = len(minlist)
        day={}
        cur.execute(sql_tmp)
        print "sql 추출!"

        ix = 0
        count=0
        donecheck=0
        cccc=0
        donecheck=0
        for result in cur:
            donecheck=donecheck+1
           # print '\n'
            result=list(result)
            for ii in [1,2,3,4]:
                if str(result[ii]) == 'None':
                    result[ii] = 0.0
            cccc=1
            #날짜 밀림 확인 필요!!
            try:
                day[result[0][0:8]]
            except:
                day[result[0][0:8]]=[0.0,0.0,0.0,0.0,0.0]


            #if int(result[0][8:10]) != count%24:#
             #   count = count + 1
              #  continue


            if count%24<9:
                day[result[0][0:8]][0]= day[result[0][0:8]][0]+result[1]+result[2]+result[3]+result[4]
            elif count%24<12:
                day[result[0][0:8]][1] =  day[result[0][0:8]][1] + result[1] + result[2] + result[3] + result[4]

            elif count%24<13:
                day[result[0][0:8]][2] =  day[result[0][0:8]][2] + result[1] + result[2] + result[3] + result[4]

            elif count%24 < 18:
                day[result[0][0:8]][3] =  day[result[0][0:8]][3] + result[1] + result[2] + result[3] + result[4]
            else :
                day[result[0][0:8]][4] =  day[result[0][0:8]][4] + result[1] + result[2] + result[3] + result[4]


            count= count+1
            #print result[0] #1단계
        nuzukdic={}

        #nuzukdic = {0:0.0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,0:20,21:0,22:0,23:0}
        for a,v in day.items():
            v[0]=min(v[0]/9.0,1)
            v[1]=min(v[1]/3.0,1)
            v[2]=min(v[2],1.0)
            v[3]=min(v[3]/5.0,1)
            v[4]=min(v[4]/6.0,1)

            #print a,"--", v
            timedivision=[9,3,1,5,6]
            hourdic={0:'00'}


            value=0.0

            week = ('Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')



            for hour in range(24):
                if hour<9:
                    uxtime = timeTOunixtime(a+'0'+str(hour))
                    value=v[0]
                elif hour < 12:
                    if hour==9:
                        uxtime = timeTOunixtime(a + '0' + str(hour))
                    else:
                        uxtime = timeTOunixtime(a + str(hour))
                    value=v[1]

                elif hour < 13:
                    uxtime = timeTOunixtime(a + str(hour))
                    value=v[2]

                elif hour < 18:
                    uxtime = timeTOunixtime(a + str(hour))
                    value=v[3]

                else :
                    uxtime = timeTOunixtime(a  + str(hour))
                    value=v[4]
                try:
                        nuzukdic[hour]
                except:
                        nuzukdic[hour]=0.0
                #nuzukdic[hour]=(value+nuzukdic[hour])/2.0
                htag = 1
                if(week[datetime.date(int(a[0:4]),int(a[4:6]),int(a[6:8])).weekday()]!='Sun' or week[datetime.date(int(a[0:4]),int(a[4:6]),int(a[6:8])).weekday()]!='Sat'  ):
                    if value!=0:
                        nuzukdic[hour] = (value + nuzukdic[hour]) / 2.0
                    htag=0
                #else:
                    #value=0.0

                data = {
                    "metric": "test_daily_led",
                    "timestamp": uxtime,
                    "value": value,
                    "tags": {
                        "MDS_ID": result[8],
                        "Device_Serial": result[9],
                        "holiday" : htag,
                        "led_inverter" : tagdata[1],
                        "factory_mart" : tagdata[2]
                    }
                }

                nuzuk_data = {
                    "metric": "test_nuzuk_led",
                    "timestamp": uxtime,
                    "value": nuzukdic[hour],
                    "tags": {
                        "MDS_ID": result[8],
                        "Device_Serial": result[9],
                        "holiday": htag,
                        "led_inverter" : tagdata[1],
                        "factory_mart" : tagdata[2]
                    }
                    }

                ret=requests.post(url, data=json.dumps(data))
                ret =requests.post(url, data=json.dumps(nuzuk_data))

                #print "***" + a + str(hour)+" ID: "+ str(result[8])+ " value: "+ str(value)+ "***"
                #print data

        if cccc==1:
            print "done sum"

        return donecheck


# main function
if __name__ == "__main__":
        csv_test = pd.read_csv('LEDtest.csv')  # ,encoding='CP949')

        # 2017-5-29 기준
        # 2016년 10월 1일 부터 2017년 2월 28일까지만 합시다
        sttime = "2016100100"
        entime = "2017022823"

        resultfile=open("resultcsv.txt","w")
        ix=1
        tagdata = ['aa','aa','aa']
        toendpoint = len(infotest.h)

        for i in range (toendpoint):#csv_test.shape[0]):

            tagdata[0] = (infotest.h[i][0])
            mds_id = tagdata[0]

            tagdata[1] = (infotest.h[i][1])  # led,형광등
            tagdata[2] = (infotest.h[i][2])  # 마트,공장

            print tagdata
            donecheck = updateMINONE(sttime, entime, mds_id, tagdata)
            print donecheck
            resultfile.write(str(donecheck))
            resultfile.write("\n")

            print "ix: %s, mdsid: %s" %(ix, mds_id)

            # 화면에 메세지 출력할때,
            # 줄이 바뀌지 않고. 한줄에만 덮혀서 출력함

            # pout = "ix: %s, mdsid: %s, donecheck: %d \r" %(ix, mds_id, donecheck)
            # sys.stdout.write(pout)
            # sys.stdout.flush()

            ix=ix+1

        cur.close()
        con.close()
