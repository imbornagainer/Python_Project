#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
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

import _input_list_17_0904 as _mds_id

url = "http://125.140.110.217:4242/api/put"
response ={}
m = ''
con = cx_Oracle.connect('keti_user/keti1357!#@125.141.144.149/aimir')
cur = con.cursor()

def parse_args():
    parser=argparse.ArgumentParser(description="how to run, insert TSDB SW",\
            usage='use "%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-st", "--starttime", default='20160701', help="input start time")
    parser.add_argument("-et", "--endtime", default='20160702', help="input end time")
    parser.add_argument("-sp", "--startpoint", default=0, help="start point of\
            input list(group of meter IDs) ")
    args = parser.parse_args()
    return args

def timeTOunixtime (rlt):
        #YYYY [0:4], MM [4:6], DD [6:8], HH [8:10], m[10:12]
        stime = "%s/%s/%s" %(rlt[6:8], rlt[4:6], rlt[0:4])
        h = rlt[8:10]

	if len(rlt) == 10:
         m = '00';
	else:
        	m = rlt[10:12]

        #unixtime need to have 1 sec unit scale
        dechour = int(h)*60*60
        dechour += int(m)*60
        unixday = time.mktime(datetime.datetime.strptime(stime, "%d/%m/%Y").timetuple())
        unixtime = unixday + dechour

        return int(unixtime)


# update 15 minutes one TSDB
def updateMINONE(tindex, in_sttime, in_entime, in_mdsid, tagdata):
        starttime = in_sttime
        endtime = in_entime
        mdsid = in_mdsid
        serialid = tagdata
        #print type(serialid)

        #sql_tmp = "select ELE.LP_TIME, ELE.VALUE_00, ELE.VALUE_15, ELE.VALUE_30, ELE.VALUE_45, ECU.NAME, ECO.LOCATION, ECO.SIC, ELE.MDS_ID, ELE.DEVICE_SERIAL, ECU.CUSTOMERNO, ELE.CHANNEL from EMNV_LP_EM_VIEW  ELE join EMNV_CONTRACT_VIEW ECO on ELE.MDS_ID = ECO.MDS_ID join EMNV_CUSTOMER_VIEW ECU on ECO.CUSTOMERNO = ECU.CUSTOMERNO where (ELE.CHANNEL=1) and (ELE.LP_TIME between '%s' and '%s') and (ELE.DEVICE_SERIAL='%s') order by ELE.DEVICE_SERIAL ASC, ELE.LP_TIME ASC" %(starttime, endtime, serialid[0])

        sql_tmp = "SELECT LP_TIME, VALUE_00, VALUE_15, VALUE_30, VALUE_45, MDS_ID, DEVICE_SERIAL, WRITEDATE, CONTRACT_ID FROM EMNV_LP_EM_VIEW ELE WHERE ('%s' <= ELE.LP_TIME AND ELE.LP_TIME <= '%s') AND ELE.CHANNEL = 1 AND ELE.DEVICE_SERIAL = '%s'" %(starttime, endtime, serialid[0])

	minlist = ['00', '15', '30', '45']
	lcfm = len(minlist)
        cur.execute(sql_tmp)

        ix = tindex

        for result in cur:
            ix += 1
            if (ix % 10 == 0) : 
                time.sleep(0.0001)
                print (result)

            for i in range(lcfm):

                if str(result[i+1]) == 'None':
                    m_value = 0.0
                else:
                    m_value = result[i+1]

                uxtime = timeTOunixtime(result[0] + minlist[i]) #ELE.YYYYMMDDHH
                # YYYY [0:4], MM [4:6], DD [6:8], HH [8:10], m[10:12]
                week = ('Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')
                if (ix % 2 == 0) : 
                    print ("(insert DB) ix: %s, i: %s, serial-ID: %s, ymd: %s,uxtime: %s, metric: %s"\
                    %(tindex, i, result[6], (result[0]+minlist[i]), uxtime, __m))
                print (result[0]+minlist[i])
                exit()

                htag = 0
                if (week[datetime.date(int(result[0][0:4]),\
                    int(result[0][4:6]), int(result[0][6:8])).weekday()] == 'Sun'):
                    htag = 1
                elif (week[datetime.date(int(result[0][0:4]),\
                    int(result[0][4:6]), int(result[0][6:8])).weekday()] == 'Sat'):
                    htag = 1

                data = {
                    "metric": __m,
                    "timestamp": uxtime,
                    "value": m_value,
                    "tags": {
                        "_mds_id": result[5],
                        "modem_num": result[6],
                        "load": "all",
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
                    ret = requests.post(url, data)
                    #print (ret)
                except urllib2.HTTPError as e: 
                    error_msg = e.read()
                    print ( "exception during requests HTTP", error_msg)

        return 42

if __name__ == "__main__":

        arg = parse_args()

        sttime = "2016070100"
        entime = "2017070100"

        if (arg.starttime != None) : sttime = arg.starttime
        if (arg.endtime != None) : entime = arg.endtime
        spoint_index = arg.startpoint
        print ("   " + "processing ... ")
        print ("  ", sttime, entime, spoint_index)

        __m = "rc04_simple_load_data_v1"

        filename = '_progress_serial' + sttime + "to" + entime + ".txt"
        resultfile = open(filename, "a")
        ix = 1
        tagdata = ['01220800653', '01220824131', '01220800754', '01220435097', '01220674104', '01224224145', '01220674127', '01220824133', '01220435017', '01224230474', '01220435137', '01220435096', '01220800670', '01220800666', '01220434991', '01220474138', '01224230503', '01220674054', '01224224148', '01224230475', '01224224146', '01224224137', '01220674137', '01220674059', '01220800665', '01220674126', '01220435087', '01220674124', '01220674132', '01220800616', '01220674131', '01220800605', '01220800760', '01220674072', '01220674143', '01220435120', '01220800759', '01220674158', '01220800639', '01220674148', '01220674057', '01220435112', '01220674074', '01220435048', '01220674092', '01220800673', '01220674097', '01220800667', '01220674063', '01220800725', '01224230497', '01220674129', '01220674103', '01220800629', '01224224126', '01224224143', '01224224147', '01224230492', '01220674066', '01224230462', '01224230498', '01220674091', '01220674158', '01220800715', '01220674062', '01220674068', '01220435110', '01220435075', '01220824145', '01222718541', '01222699985', '01222649986 ', '01222789985 ', '01222669984', '01222598541 ', '01222677452', '01222699541', '01222799989', '01222749987 ', '01222789987', '01222577541 ', '01222708541', '01222726543', '01222731541', '01222744759', '01222719985', '01222671541 ', '01222628541', '01222757452', '01222627543', '01222588541 ', '01222709987 ', '01222649989', '01222729984'] 

        #input dictionary
        #important : this is input file, make it clear which the input data
        led_tag = _mds_id.add_list

        toendpoint = len(led_tag)
        print ("   total length=", toendpoint, "start id order =", spoint_index)
        assert toendpoint > int(spoint_index), " reduce the spoint_index number "

        sp = int(spoint_index)
        for i in range(sp, toendpoint):
            mds_id = led_tag[i]
            tagdata = None

            # Oracle -> OpenTSDB 기능 실행
            donecheck = updateMINONE(i, sttime, entime, mds_id, tagdata)
            if donecheck > 0:
                print ("들어간 데이터 량" + str(donecheck))

            resultfile.write(str(mds_id) + "," + str(donecheck) + "\n")
            pout = "    ix: %s/%s, mdsid: %s 전체 진행률: %s 퍼센트 진행! \rr " % (ix, toendpoint, mds_id, int(float((ix) / float(toendpoint)) * 100.0))
            sys.stdout.write(pout)
            sys.stdout.flush()
            ix = ix+1
            resultfile.flush()

	cur.close()
	con.close()


