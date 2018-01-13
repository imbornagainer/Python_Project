# -*- coding: utf-8 -*-
# Author : jeonghoonkang , https://github.com/jeonghoonkang

import time
import datetime
#import cx_Oracle
import os
import sys
import requests
import json
import time, datetime
import numpy as np

import _mds_id
import useTSDB
import socket

url = "http://125.140.110.217:4242/api/query?"
#url = "http://49.254.13.34:4242/api/put"
response ={}

HOST = '125.140.110.217'
PORT = 4242
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

#openTSDB 리턴 예시
#{'metric': 'rc03_simple_data_led', 'aggregateTags': [], 'dps': {'1467301500': 0.9279999732971191, '1467298800': 0.07500000298023224, '1467299700': 0.8870000243186951, '1467302400': 0.9399999976158142, '1467300600': 0.9010000228881836}, 'tags': {'holiday': '0', 'mds_id': '00-250068136', 'led_inverter': 'led'}}
# metric, dps, tags


def DCP(in_sttime, in_mdsid, tsdbclass, _tag):
    #print type(in_sttime) #datetime.date object

    date_str = ''
    date_str = date_str.join(str(in_sttime))
    #print date_str
    date_str = date_str.replace('-','')
    starttime = date_str

    # calculate endtime, in this case, just 1 day after starttime
    date_str = in_sttime + datetime.timedelta(days=1)
    date_str = str(date_str)
    date_str = date_str.replace('-','')
    #print date_str
    endtime = date_str

    mdsid = in_mdsid
    #print starttime, endtime
    tsdbclass._set_time_period(starttime, endtime) 

    #_tag = {'mds_id': str(mds_id)}
    ret_dict = tsdbclass.readTSD(_tag)
    #print ret_dict
    #ret_dict = openTSDB return 값

    if ret_dict == None: 
        #print "omitting data -> wrong METRIC, ID, or no data during that period \n" 
        return 0 

    new_metric = 'rc03_1h_mean_led_test_001'
    __mds_id = str(_tag['mds_id']) # mds_id 를 string으로 만든게 __mds_id

    d = datetime.date(int(starttime[0:4]),int(starttime[4:6]),int(starttime[6:8]))
    unixtime = time.mktime(d.timetuple())
    arr = np.array([[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0],[0.,0]])

    #print len(arr)
    #print len(ret_dict['dps'])

    for __t, __v in ret_dict['dps'].items() :
        #1시간, 3600초 단위로 idex 생성  
        arr_idx = (int(__t) - int(unixtime)) / 3600
        arr[arr_idx][0] += __v
        arr[arr_idx][1] += 1
        #__t = 시간 __v = dps값? 측정값?

    for idx in range(0,25) :
        if arr[idx][1] == 0:
            _buf = "put %s %s %s mdsid=%s\n" %(new_metric, (int)(unixtime) + (3600*idx), 0 , __mds_id)
        else :
            _buf = "put %s %s %s mdsid=%s\n" %(new_metric, (int)(unixtime) + (3600*idx), (arr[idx][0]) / arr[idx][1], __mds_id)
        #print _buf
        sock.sendall(_buf)
        #ret_data = sock.recv(1024)
        #print '.... received', repr(data)

    #print "\n keep running .......\n"
    return 42

def ch2date(_s, _e):
    
    ys = int(_s[:4])
    ms = int(_s[4:6])
    ds = int(_s[6:8])
    ye = int(_e[:4])
    me = int(_e[4:6])
    de = int(_e[6:8])
    sday = datetime.date(ys,ms,ds)
    eday = datetime.date(ye,me,de)    

    return sday, eday


# main function
if __name__ == "__main__":

    sttime = "2016050100"
    entime = "2017050100"

    __url = url
    __st = sttime
    __et = entime

    filename = '_mean_insert_result' + sttime + "to" + entime + ".txt"
    resultfile = open(filename,"w")

    dix = 1
    tagdata = ['aa','aa','aa','aa']
    ids = _mds_id.led_list
    toendpoint = len(ids)

    # DAY _ loop
    # sday 시작일 eday 종료일 mday 시작~종료까지 증가하는 date
    # lds : loop days 
    sday, eday = ch2date(__st, __et)
    mday = sday
    lds = repr(eday - sday)
    lds = lds[lds.index('(')+1:lds.index(')')]

    # TSDB 시작일만 등록 
    tsdbclass = useTSDB.u_ee_tsdb(__url, __st)
    tsdbclass.set_metric('rc03_simple_data_led_v2')

    while (eday != mday) :
        # just day count 
        dix = dix + 1

        # mday 데이터 처리 
        # print mday

        # 모든 MDSiD에 대해서 처리, MDSID는 위의 import _mds_id 에서 읽음 
        for i in range (toendpoint):

            mds_id = ids[i]
            _tag = {'mds_id': str(mds_id)}

            donecheck = DCP(mday, mds_id, tsdbclass, _tag)
            #pout = "  ... inner loop -> i: %s, : total: %s 전체 진행률: %s 퍼센트 진행!  \r" \
            #        %(i, toendpoint, int(float((i)/float(toendpoint))*100))
            #sys.stdout.write(pout)
        time.sleep(0.0001)

        # mday 1일 증가
        mday = mday + datetime.timedelta(days=1)

        pout = " ... main loop -> dix: %s, : lds %s 전체 진행률: %s 퍼센트 진행!  \r" \
                %(dix, lds,int(float((dix)/float(lds))*100))
        sys.stdout.write(pout)
        sys.stdout.flush()
        #resultfile.write(str(mds_id)+","+str(donecheck)+"\n")
        #resultfile.flush()

    sock.close()
    print (" \n ... Finishing copying ... ")
