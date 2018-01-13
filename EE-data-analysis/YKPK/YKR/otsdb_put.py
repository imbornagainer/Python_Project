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
import socket
import math
import csv
from decimal import Decimal

url = "http://125.140.110.217:4242/api/query?"
#url = "http://49.254.13.34:4242/api/put"
response ={}
_test_dict = {}
HOST = '125.140.110.217'
PORT = 4242
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def update():

    #ret_dict = tsdbclass.readTSD(_tag)
    #if ret_dict == None: return 0

    __mds_id = '00-000000000' # test용

    _unixtime = 1462028400

    _dict_list = []
    _data_dict = {}
    for i in range(1,11):
        reader = csv.reader(open('_data_dict.csv'))
        for row in reader:
            key = long(row[0])
            _data_dict[key] = Decimal(row[i])
        _dict_list.append(_data_dict.copy())
        _data_dict.clear()
        print "  reading csv data ", i

    print "\n Start Test .......\n"

    _time_list = []
    _temp_list = []
    
    print " Total data length =", (len(_dict_list) * len(_dict_list[0]))
    print

    for list_idx in range(0,10):
        timeStart = time.time()
        for idx in range(0,100000) :
            __t = idx + 1462028400
            __v = _dict_list[list_idx][__t]
            _buf = "put %s %s %s mdsid=%s\n" %('z__test_sp_8' + str(list_idx), __t, __v, __mds_id)
            #print _buf
            sock.sendall(_buf)
        timeEnd = time.time()
        print " insert start time =", timeStart
        print " insert done time =", timeEnd
        ctime = timeEnd - timeStart
        print " 100,000 insert Runtime duration =", ctime, "seconds"
        print
        #print str(list_idx+1) + " Set" + " time Done"
        _temp_list.append(ctime)

    _avg = sum(_temp_list) / 10.0
    print " Avg ="+ str(_avg)
    _temp_list[:] = []

    return 42

# main function
if __name__ == "__main__":

    __url = url
    print
    timestamp = time.localtime()
    print " " + time.asctime(timestamp)

    donecheck = update()

    sock.close()
    print (" \n ... Finishing , Closing ... ")
