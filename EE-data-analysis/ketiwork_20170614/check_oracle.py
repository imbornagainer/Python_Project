#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import cx_Oracle
import os
import sys
import requests
import json
import argparse
import urllib2
from types import *

import _input_list_17_0829 as _mds_id

url = "http://125.140.110.217:4242/api/put"
response ={}

con = cx_Oracle.connect('keti_user/keti1357!#@125.141.144.149/aimir')
cur = con.cursor()

data_cnt = 0

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
def updateMINONE(in_sttime, in_entime, in_mdsid, tagdata):
        global data_cnt
        starttime = in_sttime
        endtime = in_entime
        mdsid = in_mdsid

        sql_tmp = "select ELE.LP_TIME, ELE.VALUE_00, ELE.VALUE_15, ELE.VALUE_30, ELE.VALUE_45, ECU.NAME, ECO.LOCATION, ECO.SIC, ELE.MDS_ID, ELE.DEVICE_SERIAL, ECU.CUSTOMERNO, ELE.CHANNEL from EMNV_LP_EM_VIEW  ELE join EMNV_CONTRACT_VIEW ECO on ELE.MDS_ID = ECO.MDS_ID join EMNV_CUSTOMER_VIEW ECU on ECO.CUSTOMERNO = ECU.CUSTOMERNO where (ELE.CHANNEL=1) and (ELE.LP_TIME between '%s' and '%s') and (ELE.DEVICE_SERIAL='%s') order by ELE.MDS_ID ASC, ELE.LP_TIME ASC" %(starttime, endtime, mdsid[0])

	minlist = ['00', '15', '30', '45']
	lcfm = len(minlist)

        cur.execute(sql_tmp)

        ix = 0

        for result in cur:
            data_cnt = data_cnt + 1

            print " count ---------------->", data_cnt

            print (' there is data in oracle')
            print result
            return 

            ix += 1
            if (ix % 100 == 0) : time.sleep(0.00001)
            #print result

            for i in range(lcfm):

                if str(result[i+1]) == 'None':
                    m_value = 0.0
                else:
                    m_value = result[i+1]

                uxtime = timeTOunixtime(result[0] + minlist[i]) #ELE.YYYYMMDDHH
                # YYYY [0:4], MM [4:6], DD [6:8], HH [8:10], m[10:12]
                week = ('Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')
                #print "(updateMINONE) ix: %s, i: %s, mdsid: %s, ymd: %s, uxtime: %s, value: %s" 
                #%(ix, i, result[8], (result[0]+minlist[i]), uxtime, m_value)

                htag = 0
                if (week[datetime.date(int(result[0][0:4]), int(result[0][4:6]), int(result[0][6:8])).weekday()] == 'Sun'):
                    htag = 1
                elif (week[datetime.date(int(result[0][0:4]), int(result[0][4:6]), int(result[0][6:8])).weekday()] == 'Sat'):
                    htag = 1

                data = {
                    "metric": __m,
                    "timestamp": uxtime,
                    "value": m_value,
                    "tags": {
                        "mds_id": result[8],
                        #"measure_gl": str(tagdata[1]),
                        "led_inverter": "led",
                        #"factory_mart": tagdata[2],
                        #"company_size": tagdata[3],
                        #"business_type": tagdata[4],
                        "holiday": htag,
                    }
                        #"Saupjang": tagdata[1],
                }

                try: 
                    data=json.dumps(data)
                    #print (data)
                    #ret = requests.post(url, data)
                    #print (ret)
                except urllib2.HTTPError as e: 
                    error_msg = e.read()
                    print ( "exception during requests HTTP", error_msg)

        return 42

# main function
if __name__ == "__main__":

        #user shoud input 
        sttime = "2016090100"
        entime = "2016100100"
    

        __m = "no_meaning"

        filename = '_check_progress_' + sttime + "to" + entime + ".txt"
        resultfile = open(filename, "w")
        ix = 1
        tagdata = ['aa', 'aa', 'aa', 'aa']

        #user shoud input 
        #input dictionary
        id_list = _mds_id.modem_list

        # 411
        toendpoint = len(id_list)

        for i in range(toendpoint):
            mds_id = id_list[i]
            tagdata = None

            # Oracle -> OpenTSDB 기능 실행
            donecheck = updateMINONE(sttime, entime, mds_id, tagdata)
            if donecheck > 0:
                print "들어간 데이터 량" + str(donecheck)

            resultfile.write(str(mds_id)+ "," + str(donecheck) + "\n")
            pout = " ix: %s/%s, mdsid: %s 전체 진행률: %s 퍼센트 진행! \n" % (ix, toendpoint, mds_id, int(float((ix) / float(toendpoint)) * 100.0))

            print pout
            #sys.stdout(pout)
            #sys.stdout.flush()
            ix = ix+1
            resultfile.flush()

	cur.close()
	con.close()


