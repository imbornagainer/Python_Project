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
from types import *

url = "http://125.140.110.217:4242/api/put"
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
def updateMINONE(in_sttime, in_entime, in_mdsid,tagdata):
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
                # YYYY [0:4], MM [4:6], DD [6:8], HH [8:10], m[10:12]
                week = ('Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')
                #print "(updateMINONE) ix: %s, i: %s, mdsid: %s, ymd: %s, uxtime: %s, value: %s" %(ix, i, result[8], (result[0]+minlist[i]), uxtime, m_value)
                ix += 1

                htag = 0
                if (week[datetime.date(int(result[0][0:4]), int(result[0][4:6]), int(result[0][6:8])).weekday()] == 'Sun'):
                    htag = 1

                elif (week[datetime.date(int(result[0][0:4]), int(result[0][4:6]), int(result[0][6:8])).weekday()] == 'Sat'):
                    htag = 1

                data = {
                    "metric": "origin_data_inverter_smk",
                    "timestamp": uxtime,
                    "value": m_value,
                    "tags": {
                        "MDS_ID": result[8],
                        "Saupjang": tagdata[1],
                        "led_inverter": tagdata[2],
                        "factory_mart": tagdata[3],
                        "company_size": tagdata[4],
                        "business_type": tagdata[5],
                        "holiday": htag,
                    }
                }

                ret = requests.post(url, data=json.dumps(data))


# main function
if __name__ == "__main__":

        sttime = "2016110300"
        entime = "2016112700"

        filename = 'INV_origin_resultcsv' + sttime + "to" + entime + ".txt"
        resultfile = open(filename, "w")
        ix = 1
        tagdata = ['aa', 'aa', 'aa', 'aa', 'aa']
        led_id = [['00-360000244', '1602220027', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000247', '1602160002', 'inverter', 'bigcompany', 'none', 'metal', 'blower'], ['00-360000086', '1602230095', 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['01220543054-0301', '1602220043', 'inverter', 'mart', 'bigcompany', 'building_etc', 'none'], ['00-360000242', '1602250003', 'inverter', 'middlecompany', 'none', 'industryEtc', 'pump'], ['01224230502-0101', '1602160002', 'inverter', 'factory', 'bigcompany', 'metal', 'none'], ['00-450083462', '1602240008', 'inverter', 'middlecompany', 'none', 'industryEtc', 'none'], ['00-450083461', '1602230042', 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['00-450083467', '1602250067', 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['01223208835-0301', '1602220044', 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['00-450083465', '1602250067', 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['00-450083464', '1602240014', 'inverter', 'smallcompany', 'none', 'industryEtc', 'blower'], ['01223239890-0301', '1602230025', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-450083469', '1602250042', 'inverter', 'middlecompany', 'none', 'industryEtc', 'pump'], ['00-360000238', '1602220027', 'inverter', 'bigcompany', 'none', 'departmentStore', 'none'], ['01224272979-0301', '1602250067', 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['00-360000032', '1602220045', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000231', '1602240019', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000233', '1602220043', 'inverter', 'bigcompany', 'none', 'building_etc', 'pump'], ['00-360000235', '1602250085', 'inverter', 'bigcompany', 'none', 'wood', 'pump'], ['00-360000236', '1602220043', 'inverter', 'bigcompany', 'none', 'building_etc', 'pump'], ['00-360000090', '1602240022', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000093', '1602240002', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000092', '1602230026', 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['00-360000127', '1602230101', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208825-0301', '1602220044', 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['01224273046-0301', '1602230012', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000001', '1602250058', 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['00-360000004', '1602230101', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000005', '1602240025', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-450086604', '1602250067', 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['00-360000008', '1602260135', 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['01224230450-0301', '1602220027', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-450086602', '1602230100', 'inverter', 'bigcompany', 'none', 'departmentStore', 'pump'], ['01224272939-0301', '1602250067', 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['00-360000264', '1602240031', 'inverter', 'middlecompany', 'none', 'metal', 'fan'], ['00-360000160', '1602230008', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239889-0301', '1602230016', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-450083522', '1602230006', 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['01224273096-0301', '1602250067', 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['01224230548-0301', '1602230100', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000155', '1602230008', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000156', '1602220034', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000157', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000152', '1602220034', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000153', '1602230025', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000159', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01220533054-0301', '1602220027', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208855-0301', '1602230007', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208786-0301', '1602230008', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208847-0301', '1602220034', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-450083466', '1602250067', 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['01223208800-0301', '1602230007', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239888-0301', '1602230024', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000201', '1602220019', 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['00-360000202', '1602220044', 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['00-360000203', '1602260082', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000205', '1602220044', 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['00-360000209', '1602260082', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['01223239881-0301', '1602230018', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000172', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208829-0301', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000213', '1602250009', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000191', '1602230049', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000193', '1602230024', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000217', '1602230018', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000196', '1602230049', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000197', '1602230018', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000199', '1602230007', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223187332-0001', '1602220019', 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['01220172969-0301', '1602220043', 'inverter', 'mart', 'bigcompany', 'building_etc', 'none'], ['00-450083419', '1602230042', 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['01223208826-0301', '1602220034', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000165', '1602230038', 'inverter', 'etc', 'smallcompany', 'none', 'none'], ['00-360000281', '1602230012', 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['00-360000282', '1602250085', 'inverter', 'bigcompany', 'none', 'wood', 'pump'], ['00-360000166', '1602230025', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-450083417', '1602230042', 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['01223208832-0301', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000183', '1602230016', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000182', '1602240019', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000181', '1602230024', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000187', '1602230007', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000185', '1602260082', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000212', '1602250005', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000189', '1602220018', 'inverter', 'factory', 'bigcompany', 'ceramic', 'none'], ['01224273066-0301', '1602250067', 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['00-360000194', '1602220037', 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['01223208790-0301', '1602230008', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000214', '1602260070', 'inverter', 'etc', 'etc', 'none', 'none'], ['01223208779-0301', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239883-0301', '1602230025', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239886-0301', '1602230024', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223181047-0301', '1602230025', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000107', '1602240002', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000025', '1602230033', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000020', '1602220041', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000228', '1602220023', 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['00-360000229', '1602230023', 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['00-360000226', '1602220018', 'inverter', 'factory', 'bigcompany', 'ceramic', 'none'], ['00-360000224', '1602240042', 'inverter', 'factory', 'smallcompany', 'food', 'none']]

        toendpoint = len(led_id)

        for i in range(toendpoint):

            tagdata = led_id[i]
            mds_id = led_id[i][0]
            # Oracle -> OpenTSDB 기능 실행
            donecheck = updateMINONE(sttime, entime, mds_id, tagdata)
            if donecheck > 0:
                print "들어간 데이터 량" + str(donecheck)

            resultfile.write(str(mds_id) + "," + str(donecheck) + "\n")

            print "ix: %s, mdsid: %s 전체 진행률: %s 퍼센트 진행!" % (ix, mds_id, int(float((ix) / float(toendpoint)) * 100.0))
            ix=ix+1
            resultfile.flush()

	cur.close()
	con.close()


