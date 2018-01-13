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
                    "metric": "origin_data_please",
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

        sttime = "2016110100"
        entime = "2017043023"

        filename = 'LED_origin_resultcsv' + sttime + "to" + entime + ".txt"
        resultfile = open(filename, "w")
        ix = 1
        tagdata = ['aa', 'aa', 'aa', 'aa', 'aa']
        led_id = [['00-250102796', '1602250039', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071089', '1601140003', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250060001', '1601140004', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130385', '1601140005', 'led', 'factory', 'smallcompany', 'metal'], ['00-250071424', '1601140006', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059766', '1602010003', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059871', '1602040002', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059708', '1602040003', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071598', '1602040004', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250052077', '1602040007', 'led', 'factory', 'smallcompany', 'fiber'], ['00-250102776', '1602040008', 'led', 'factory', 'smallcompany', 'metal'], ['00-250071373', '1602040010', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071403', '1602150001', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071434', '1602150003', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071308', '1602170004', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071330', '1602170004', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-251004742', '1602170009', 'led', 'factory', 'smallcompany', 'metal'], ['00-250071525', '1602170011', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-460003531', '1602180002', 'led', 'factory', 'bigcompany', 'fiber'], ['00-250071405', '1602180008', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068220', '1602190007', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068226', '1602190007', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059921', '1602190008', 'led', 'etc', 'smallcompany', 'none'], ['00-250059949', '1602190008', 'led', 'etc', 'smallcompany', 'none'], ['00-250068179', '1602190009', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071520', '1602220006', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-450083471', '1602220010', 'led', 'factory', 'bigcompany', 'metal'], ['00-250068178', '1602220012', 'led', 'factory', 'smallcompany', 'metal'], ['00-250071427', '1602220014', 'led', 'factory', 'middlecompany', 'ceramic'], ['00-250071507', '1602220020', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083432', '1602220022', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250071428', '1602220026', 'led', 'apt', 'apt', 'none'], ['00-250070991', '1602220026', 'led', 'apt', 'apt', 'none'], ['00-250071407', '1602220026', 'led', 'apt', 'apt', 'none'], ['00-250130341', '1602220029', 'led', 'apt', 'apt', 'none'], ['00-450083468', '1602220031', 'led', 'factory', 'bigcompany', 'metal'], ['00-250071364', '1602220032', 'led', 'apt', 'apt', 'none'], ['00-250071217', '1602220032', 'led', 'apt', 'apt', 'none'], ['00-250102673', '1602220033', 'led', 'factory', 'bigcompany', 'metal'], ['00-250059834', '1602220035', 'led', 'apt', 'apt', 'none'], ['00-250071449', '1602220038', 'led', 'office', 'bigcompany', 'departmentStore'], ['00-250071440', '1602220038', 'led', 'office', 'bigcompany', 'departmentStore'], ['00-250071453', '1602220038', 'led', 'office', 'bigcompany', 'departmentStore'], ['00-250071548', '1602220042', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250059976', '1602220048', 'led', 'factory', 'smallcompany', 'wood'], ['00-250071459', '1602220051', 'led', 'factory', 'bigcompany', 'fiber'], ['00-250059703', '1602230002', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250130308', '1602230005', 'led', 'office', 'smallcompany', 'building_etc'], ['00-250130375', '1602230010', 'led', 'factory', 'middlecompany', 'food'], ['00-250071057', '1602230021', 'led', 'factory', 'middlecompany', 'food'], ['00-250071032', '1602230027', 'led', 'apt', 'apt', 'none'], ['00-250071026', '1602230027', 'led', 'apt', 'apt', 'none'], ['00-250059909', '1602230032', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250059812', '1602230034', 'led', 'office', 'etc', 'school'], ['00-250071659', '1602230035', 'led', 'office', 'smallcompany', 'building_etc'], ['00-250059912', '1602230036', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130333', '1602230040', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071086', '1602230043', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068185', '1602230047', 'led', 'factory', 'smallcompany', 'wood'], ['00-250071072', '1602230048', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071167', '1602230048', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250130374', '1602230050', 'led', 'apt', 'apt', 'none'], ['00-450083458', '1602230051', 'led', 'office', 'bigcompany', 'building_etc'], ['00-450083404', '1602230051', 'led', 'office', 'bigcompany', 'building_etc'], ['00-450083445', '1602230051', 'led', 'office', 'bigcompany', 'building_etc'], ['00-450083403', '1602230051', 'led', 'office', 'bigcompany', 'building_etc'], ['00-450083448', '1602230051', 'led', 'office', 'bigcompany', 'building_etc'], ['00-250071667', '1602230052', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071700', '1602230052', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071104', '1602230055', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071109', '1602230055', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250130373', '1602230058', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130372', '1602230058', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-450083559', '1602230059', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450086595', '1602230060', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450086594', '1602230062', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000364', '1602230063', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000263', '1602230065', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000347', '1602230065', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450086593', '1602230066', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450086534', '1602230067', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083489', '1602230070', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083492', '1602230073', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083431', '1602230074', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083472', '1602230078', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083490', '1602230079', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000476', '1602230081', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000379', '1602230083', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000369', '1602230084', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083491', '1602230085', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000293', '1602230086', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083430', '1602230089', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000485', '1602230091', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000392', '1602230093', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250130309', '1602230097', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250130343', '1602230098', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250059996', '1602230103', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250071088', '1602230105', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250071168', '1602230105', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250068173', '1602230106', 'led', 'factory', 'smallcompany', 'ceramic'], ['00-250059818', '1602230107', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250059751', '1602230111', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250060002', '1602240001', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250059849', '1602240003', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250059998', '1602240004', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071509', '1602240005', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250130315', '1602240005', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250130318', '1602240005', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250071151', '1602240006', 'led', 'factory', 'smallcompany', 'food'], ['00-250068171', '1602240011', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130378', '1602240012', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130384', '1602240013', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068164', '1602240016', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250068193', '1602240018', 'led', 'apt', 'apt', 'none'], ['00-450083564', '1602240023', 'led', 'office', 'bigcompany', 'departmentStore'], ['00-450083562', '1602240023', 'led', 'office', 'bigcompany', 'departmentStore'], ['00-450083563', '1602240023', 'led', 'office', 'bigcompany', 'departmentStore'], ['00-250059706', '1602240026', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059775', '1602240028', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-460000184', '1602240035', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250059925', '1602240037', 'led', 'factory', 'smallcompany', 'metal'], ['00-250071481', '1602240039', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071550', '1602240039', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059813', '1602240040', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250070992', '1602240044', 'led', 'factory', 'smallcompany', 'wood'], ['00-250059803', '1602240047', 'led', 'factory', 'smallcompany', 'metal'], ['00-250068139', '1602240054', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068198', '1602240054', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071186', '1602240055', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068144', '1602240059', 'led', 'factory', 'smallcompany', 'wood'], ['00-250059765', '1602240061', 'led', 'factory', 'bigcompany', 'ceramic'], ['00-250059836', '1602240061', 'led', 'factory', 'bigcompany', 'ceramic'], ['00-250071681', '1602240072', 'led', 'factory', 'smallcompany', 'wood'], ['00-250068192', '1602240074', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250060022', '1602240075', 'led', 'factory', 'smallcompany', 'wood'], ['00-250068202', '1602240076', 'led', 'factory', 'smallcompany', 'wood'], ['00-250068215', '1602240076', 'led', 'factory', 'smallcompany', 'wood'], ['00-250071624', '1602240081', 'led', 'factory', 'smallcompany', 'wood'], ['00-250059956', '1602240084', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-450083463', '1602240085', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059997', '1602240086', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250059999', '1602240087', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071557', '1602250002', 'led', 'apt', 'apt', 'none'], ['00-250071540', '1602250002', 'led', 'apt', 'apt', 'none'], ['00-250130324', '1602250002', 'led', 'apt', 'apt', 'none'], ['00-250071493', '1602250002', 'led', 'apt', 'apt', 'none'], ['00-250068218', '1602250004', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130336', '1602250006', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130361', '1602250007', 'led', 'factory', 'middlecompany', 'metal'], ['00-250130363', '1602250007', 'led', 'factory', 'middlecompany', 'metal'], ['00-250130367', '1602250007', 'led', 'factory', 'middlecompany', 'metal'], ['00-250130362', '1602250007', 'led', 'factory', 'middlecompany', 'metal'], ['00-250130312', '1602250014', 'led', 'office', 'etc', 'building_etc'], ['00-250130313', '1602250014', 'led', 'office', 'etc', 'building_etc'], ['00-250130370', '1602250015', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-360000177', '1602250017', 'led', 'factory', 'bigcompany', 'fiber'], ['00-250130365', '1602250018', 'led', 'apt', 'apt', 'none'], ['00-250059754', '1602250019', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071694', '1602250019', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250059705', '1602250022', 'led', 'factory', 'smallcompany', 'metal'], ['00-251000081', '1602250024', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250130327', '1602250025', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071467', '1602250026', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130339', '1602250027', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130380', '1602250028', 'led', 'factory', 'middlecompany', 'food'], ['00-250130344', '1602250029', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071438', '1602250032', 'heungwanglamp', 'office', 'bigcompany', 'departmentStore'], ['00-250102801', '1602250039', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250102797', '1602250039', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250102794', '1602250039', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-450083429', '1602250043', 'led', 'office', 'bigcompany', 'building_etc'], ['00-251004421', '1602250044', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250102795', '1602250047', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250102798', '1602250047', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250102800', '1602250047', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130342', '1602250049', 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250102710', '1602250052', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071647', '1602250055', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130335', '1602250062', 'led', 'etc', 'etc', 'none'], ['00-250059992', '1602250063', 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071612', '1602250066', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-360000218', '1602250068', 'led', 'factory', 'bigcompany', 'fiber'], ['00-450086512', '1602250069', 'led', 'etc', 'bigcompany', 'none'], ['00-250071495', '1602250070', 'led', 'factory', 'smallcompany', 'wood'], ['00-250059861', '1602250071', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130345', '1602250076', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130340', '1602250079', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250102620', '1602250092', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250059874', '1602250112', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250102696', '1602250123', 'led', 'apt', 'apt', 'none'], ['00-250130314', '1602250126', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130320', '1602250127', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130317', '1602250129', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071677', '1602250130', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130310', '1602250132', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130321', '1602250135', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250068224', '1602250140', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071432', '1602250153', 'led', 'office', 'bigcompany', 'sangyong'], ['00-250130379', '1602250154', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250059819', '1602250156', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068165', '1602250160', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071090', '1602250164', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130329', '1602250165', 'led', 'apt', 'apt', 'none'], ['00-250071061', '1602250166', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071068', '1602250166', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071066', '1602250167', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071581', '1602250171', 'led', 'apt', 'apt', 'none'], ['00-250068146', '1602250173', 'led', 'office', 'etc', 'school'], ['00-250068148', '1602250173', 'led', 'office', 'etc', 'school'], ['00-250059839', '1602250176', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250059965', '1602250177', 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130306', '1602250184', 'led', 'apt', 'apt', 'none'], ['00-250130326', '1602250184', 'led', 'apt', 'apt', 'none'], ['00-360000016', '1602250186', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-451000482', '1602250186', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250007125', '1602260015', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059858', '1602260017', 'led', 'office', 'smallcompany', 'building_etc'], ['00-250130307', '1602260018', 'led', 'mart', 'etc', 'sangyong'], ['00-250070994', '1602260026', 'heungwanglamp', 'factory', 'smallcompany', 'metal'], ['00-250059719', '1602260027', 'led', 'factory', 'smallcompany', 'metal'], ['00-250059915', '1602260028', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068166', '1602260029', 'led', 'factory', 'smallcompany', 'metal'], ['00-250071085', '1602260035', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071039', '1602260035', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071096', '1602260035', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071025', '1602260039', 'led', 'office', 'apt', 'building_etc'], ['00-250071087', '1602260039', 'led', 'office', 'apt', 'building_etc'], ['00-250130381', '1602260041', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130377', '1602260043', 'led', 'etc', 'bigcompany', 'none'], ['00-250130376', '1602260043', 'led', 'etc', 'bigcompany', 'none'], ['00-250071451', '1602260045', 'heungwanglamp', 'factory', 'middlecompany', 'industryEtc'], ['00-250059852', '1602260049', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250102648', '1602260051', 'led', 'factory', 'bigcompany', 'wood'], ['00-250059853', '1602260052', 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071028', '1602260058', 'led', 'apt', 'apt', 'none'], ['00-250071632', '1602260059', 'led', 'office', 'smallcompany', 'building_etc'], ['00-250059774', '1602260059', 'led', 'office', 'smallcompany', 'building_etc'], ['00-250130356', '1602260064', 'led', 'factory', 'middlecompany', 'metal'], ['00-250130358', '1602260064', 'led', 'factory', 'middlecompany', 'metal'], ['00-250130355', '1602260064', 'led', 'factory', 'middlecompany', 'metal'], ['00-250130359', '1602260064', 'led', 'factory', 'middlecompany', 'metal'], ['00-250130357', '1602260064', 'led', 'factory', 'middlecompany', 'metal'], ['00-250068210', '1602260065', 'led', 'factory', 'bigcompany', 'food'], ['00-250068197', '1602260065', 'led', 'factory', 'bigcompany', 'food'], ['00-250071465', '1602260068', 'led', 'office', 'etc', 'hospital'], ['00-250130369', '1602260072', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071679', '1602260077', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071185', '1602260081', 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071189', '1602260081', 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071312', '1602260084', 'led', 'factory', 'bigcompany', 'ceramic'], ['00-250071310', '1602260084', 'led', 'factory', 'bigcompany', 'ceramic'], ['00-250071311', '1602260084', 'led', 'factory', 'bigcompany', 'ceramic'], ['00-250071336', '1602260084', 'led', 'factory', 'bigcompany', 'ceramic'], ['00-251004064', '1602260085', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-251009025', '1602260085', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071122', '1602260086', 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071126', '1602260086', 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071144', '1602260086', 'led', 'factory', 'smallcompany', 'fiber'], ['00-360000216', '1602260088', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250130383', '1602260091', 'led', 'office', 'bigcompany', 'sangyong'], ['00-250059856', '1602260094', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071414', '1602260095', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071464', '1602260096', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071121', '1602260097', 'led', 'factory', 'smallcompany', 'metal'], ['00-250071004', '1602260097', 'led', 'factory', 'smallcompany', 'metal'], ['00-250071138', '1602260098', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071140', '1602260098', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-251009632', '1602260101', 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071625', '1602260104', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250102644', '1602260112', 'led', 'office', 'smallcompany', 'building_etc'], ['00-250102649', '1602260112', 'led', 'office', 'smallcompany', 'building_etc'], ['00-250071172', '1602260115', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071188', '1602260115', 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-360000075', '1602260118', 'led', 'office', 'smallcompany', 'building_etc'], ['00-250059724', '1602260119', 'led', 'office', 'bigcompany', 'building_etc'], ['00-250071319', '1602260120', 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071368', '1602260120', 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071549', '1602260126', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071370', '1602260128', 'led', 'factory', 'smallcompany', 'metal'], ['00-250071371', '1602260128', 'led', 'factory', 'smallcompany', 'metal'], ['00-250059770', '1602260130', 'led', 'office', 'bigcompany', 'building_etc'], ['00-250071387', '1602260133', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059784', '1602260140', 'led', 'factory', 'middlecompany', 'wood'], ['00-250059982', '1602260140', 'led', 'factory', 'middlecompany', 'wood'], ['00-250130331', '1602260142', 'led', 'apt', 'apt', 'none'], ['00-250130338', '1602260146', 'led', 'apt', 'apt', 'none'], ['00-250071696', '1602260148', 'led', 'apt', 'apt', 'none'], ['00-250059814', '1602260149', 'led', 'apt', 'apt', 'none'], ['00-250059947', '1602260150', 'led', 'apt', 'apt', 'none'], ['00-250130323', '1602260153', 'led', 'apt', 'apt', 'none'], ['00-250059854', '1602260161', 'led', 'apt', 'apt', 'none'], ['00-250071181', '1602260164', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071182', '1602260164', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071005', '1602260166', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071290', '1602260167', 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071175', '1602260170', 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071191', '1602260170', 'led', 'factory', 'smallcompany', 'fiber'], ['00-250068232', '1602260171', 'led', 'factory', 'smallcompany', 'metal']]

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


