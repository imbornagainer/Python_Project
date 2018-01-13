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
import mdsid_info
from types import *
import oracle_info_161024

url = "http://49.254.13.34:4242/api/put"
response ={}

con = cx_Oracle.connect('keti_user/keti1357!#@125.141.144.149/aimir')
cur = con.cursor()

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
def updateMINONE(in_sttime, in_entime, in_mdsid):
        starttime = in_sttime
        endtime = in_entime
        mdsid = in_mdsid

        sql_tmp = "select ELE.LP_TIME, ELE.VALUE_00, ELE.VALUE_15, ELE.VALUE_30, ELE.VALUE_45, ECU.NAME, ECO.LOCATION, ECO.SIC, ELE.MDS_ID, ELE.DEVICE_SERIAL, ECU.CUSTOMERNO, ELE.CHANNEL from EMNV_LP_EM_VIEW  ELE join EMNV_CONTRACT_VIEW ECO on ELE.MDS_ID = ECO.MDS_ID join EMNV_CUSTOMER_VIEW ECU on ECO.CUSTOMERNO = ECU.CUSTOMERNO where (ELE.CHANNEL=1) and (ELE.LP_TIME between '%s' and '%s') and (ELE.MDS_ID='%s') order by ELE.MDS_ID ASC, ELE.LP_TIME ASC" %(starttime, endtime, mdsid)

	minlist = ['00', '15', '30', '45']
	lcfm = len(minlist)

        cur.execute(sql_tmp)

        ix = 0

        for result in cur:

		for i in range(lcfm):


			if str(result[i+1]) == 'None':
				m_value = 0.0
			else:
				m_value = result[i+1]

                	uxtime = timeTOunixtime(result[0] + minlist[i]) #ELE.YYYYMMDDHH

                	print "(updateMINONE) ix: %s, i: %s, mdsid: %s, ymd: %s, uxtime: %s, value: %s" %(ix, i, result[8], (result[0]+minlist[i]), uxtime, m_value)
	               	ix += 1

                	data = {
				"metric" : "rc001.EE.15m.MDS_ID_"+result[8],
                        	"timestamp" : uxtime,
                        	"value" : m_value,
                        	"tags" : {
                                	"MDS_ID" : result [8],
                               		"Device_Serial" : result[9]
                        	}
                	}

                	ret = requests.post(url, data=json.dumps(data))

#               print ret


# main function
if __name__ == "__main__":

        sttime = "2017022400"
        entime = "2017030123"

	lc = len(oracle_info_161024.oracle_mdsid_info)

	ix = 0

	for i in range(lc):
		mds_id = oracle_info_161024.oracle_mdsid_info[i][0]
		updateMINONE(sttime, entime, mds_id)
		print "ix: %s, mdsid: %s" %(ix, mds_id)
		ix += 1

	cur.close()
	con.close()

