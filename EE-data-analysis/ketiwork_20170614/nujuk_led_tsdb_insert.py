# -*- coding: utf-8 -*-
# Author : eunsooLim , https://github.com/eunsooLim
# Author : jeonghoonkang , https://github.com/jeonghoonkang

#LED_tsdb_insert.py
#SQL 내의 LED 사이트에 대한 가동률, 누적가동률을 계산하여 TSDB에 삽입

import time
import datetime
import cx_Oracle
import os
import sys
import requests
import json
import time, datetime

import _mds_id
import useTSDB


url = "http://125.140.110.217:4242/api/query?"
#url = "http://49.254.13.34:4242/api/put"
response ={}

timezone=[('00','09'),('09','12'),('12','13'),('13','18'),('18','23')]


'''
	### 함수 : timeTOunixtime ### 
	시간 문자열을 유닉스 시간 문자열로 변환  
	parameter (rlt) : 시간 문자열
	return : 유닉스 시간 문자열  
'''

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


#################### 작업중

def updateNUJUK(in_sttime, in_entime, in_mdsid, tsdbclass, _tag):
    starttime = in_sttime
    endtime = in_entime
    mdsid = in_mdsid

    #tsdb url query 필요
    #메트릭은 : rc03_simple_data_led

    ret = tsdbclass.readTSD(_tag)
    print type(ret)

    print ret

    exit()

    minlist = ['00', '15', '30', '45']
    timedic = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
    lcfm = len(minlist)
    day={}
    # 데이터 가져오기 

    ix = 0
    count=0
    donecheck=0
    cccc=0
    donecheck=0

    print "\n keep running .......\n"
    return None


# main function
if __name__ == "__main__":

    sttime = "2016070100"
    entime = "2016070223"

    __url = url
    __st = sttime
    __et = entime

    tsdbclass = useTSDB.u_ee_tsdb(__url, __st, __et)
    tsdbclass.set_metric('rc03_simple_data_led')

    filename = '_data_copy_result' + sttime + "to" + entime + ".txt"
    resultfile = open(filename,"w")

    ix = 1
    tagdata = ['aa','aa','aa','aa']
    ids = _mds_id.led_list
    toendpoint = len(ids)

    for i in range (toendpoint):

        mds_id = ids[i]
        _tag = {'mds_id': str(mds_id)}
        print type(_tag)
        print _tag

        print _tag.items()
        
        donecheck = updateNUJUK(sttime, entime, mds_id, tsdbclass, _tag)

        pout = "  ix: %s, mdsid: %s 전체 진행률: %s 퍼센트 진행!                 \r" %(ix, mds_id,int(float((ix)/float(toendpoint))*100))
        sys.stdout.write(pout)
        sys.stdout.flush()
        resultfile.write(str(mds_id)+","+str(donecheck)+"\n")
        resultfile.flush()

        ix = ix + 1
    
    print (" \n ... Finishing copying ... ")
