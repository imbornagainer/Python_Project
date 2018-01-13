# -*- coding: utf-8 -*-
# Author : jeonghoonkang , https://github.com/jeonghoonkang

### TO DO : LTE Number로 변경해서 처리해야함
### 오라클DB가 아닌 OpenTSDB에서 데이터를 읽어와야함
    
import time
import datetime
#import cx_Oracle
import os
import sys
import requests
import argparse
import json
import time, datetime
import numpy as np
import socket

import sys
sys.path.append("../../lib")
import useTSDB

import _input_list_17_0904 as _ids

url = "http://125.140.110.217:4242/api/query?"
#url = "http://49.254.13.34:4242/api/put"
response ={}
zero_list = [['0',0]]
HOST = '125.140.110.217'
PORT = 4242
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def parse_args():
    parser=argparse.ArgumentParser(description="how to run, insert TSDB SW",\
            usage='use "%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-st", "--starttime", default=20160701, help="input start time")
    parser.add_argument("-et", "--endtime", default=20170501, help="input end time")
    parser.add_argument("-sp", "--startpoint", default=0, help="start point of\
            input list(group of meter IDs) ")
    args = parser.parse_args()
    return args

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
    __mds_id = str(_tag['modem_num']) # mds_id 를 string으로 만든게 __mds_id

    if ret_dict == None:
        i = 0
        for i in range(0,len(zero_list)):
            if zero_list[i][0] == __mds_id :
                zero_list[i][1] += 1
                return 0
            else :
                pass
        # 작성형식 [id, 데이터없는 날짜수]            
        zero_list.append([__mds_id,1])
        return 0

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

    arg = parse_args()

    sttime = "2016070100"
    entime = "2017050100"
    __st = sttime
    __et = entime

    if (arg.starttime != None) : sttime = arg.starttime
    if (arg.endtime != None) : entime = arg.endtime
    spoint_index = arg.startpoint
    print ("   " + "processing ... ")
    print ("  ", sttime, entime, spoint_index)

    __m = "rc05_operation_tag_v3"

    filename = '_zero_no_data_result' + sttime + "to" + entime + ".txt"
    resultfile = open(filename,"a")

    dix = 1
    tagdata = ['aa','aa','aa','aa']

    #input dictionary
    #important : this is input file, make it clear which the input data
    #id_tag = _ids.modem_list

    ids = _ids.modem_list
    toendpoint = len(ids)

    # DAY _ loop
    # sday 시작일 eday 종료일 mday 시작~종료까지 증가하는 date
    # lds : loop days
    sday, eday = ch2date(__st, __et)
    mday = sday
    lds = repr(eday - sday)
    lds = lds[ lds.index( '(' )+1 : lds.index( ')' ) ]

    # TSDB 시작일만 등록
    tsdbclass = useTSDB.u_ee_tsdb(url, __st)
    tsdbclass.set_metric(__m)

    while (eday != mday) :
        # just day count
        dix = dix + 1

        # mday 데이터 처리
        # print mday

        # 모든 MDSiD에 대해서 처리, MDSID는 위의 import _mds_id 에서 읽음
        for i in range (toendpoint):

            serial_id = ids[i]
            s_id = str(serial_id[0])
            #중요: 빈칸이 제일 앞에 있으면 TSDB read 시에 에러남
            if (s_id[0] == ' ') : s_id = s_id[1:]
            #print "  >>", s_id
            _tag = { 'modem_num': s_id }

            donecheck = DCP(mday, serial_id, tsdbclass, _tag)
        time.sleep(0.0001)

        # mday 1일 증가
        mday = mday + datetime.timedelta(days=1)

        pout = " ... main loop -> dix: %s, : lds %s 전체 진행률: %s 퍼센트 진행!  \r" \
                %(dix, lds,int(float((dix)/float(lds))*100))
        sys.stdout.write(pout)
        sys.stdout.flush()
        resultfile.write(pout)
        resultfile.flush()
    fname = '_out_list.py'
    f = open(fnanme,'w')
    f.write('zero_list = ')
    f.write(str(zero_list))
    f.write('\n\n')

    sock.close()
    print (" \n ... Finishing copying ... check file ", fname)

    
