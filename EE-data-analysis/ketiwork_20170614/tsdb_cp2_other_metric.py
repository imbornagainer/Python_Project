# -*- coding: utf-8 -*-
# Author : jeonghoonkang , https://github.com/jeonghoonkang

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

def updateCP(in_sttime, in_entime, in_mdsid, tsdbclass, _tag):
    starttime = in_sttime
    endtime = in_entime
    mdsid = in_mdsid

    ret_dict = tsdbclass.readTSD(_tag)
    if ret_dict == None: return 0

    new_metric = 'z_____test00'
    __mds_id = str(_tag['mds_id'])
    
    for __t, __v in ret_dict['dps'].items() : 
        _buf = "put %s %s %s mdsid=%s\n" %(new_metric, __t, __v, __mds_id) 
        print _buf
        sock.sendall(_buf)
        #ret_data = sock.recv(1024)
        #print '.... received', repr(data)

    print "\n keep running .......\n"
    return 42


# main function
if __name__ == "__main__":

    sttime = "2016050100"
    entime = "2017050100"

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

        donecheck = updateCP(sttime, entime, mds_id, tsdbclass, _tag)

        pout = "  ix: %s, mdsid: %s 전체 진행률: %s 퍼센트 진행!  \r" \
                %(ix, mds_id,int(float((ix)/float(toendpoint))*100))
        sys.stdout.write(pout)
        sys.stdout.flush()
        resultfile.write(str(mds_id)+","+str(donecheck)+"\n")
        resultfile.flush()

        ix = ix + 1
    
    sock.close()
    print (" \n ... Finishing copying ... ")
