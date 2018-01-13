#get_tsdb
# -*- coding: utf-8 -*-

## tsdb에서 데이터 받아와 exel에 저장

import time
import datetime
import os
import sys
import requests
import json
import argparse
import calendar
import urllib2
import ledinfotest
from operator import itemgetter, attrgetter
import datetime
import xlsxwriter

url = "http://125.7.128.53:4242/api/put"

'''
## 함수 : timeList
입력 받은 시간 값들 사이의 1분 단위 시간들의 리스트 반환
parameter1 (in_st) : 시작 시각
parameter2 (in_et) : 종료 시각
parameter3 (in_min) : ?
반환 (t_list) : 시간 값들의 리스트
'''
def timeList(in_st, in_et, in_min):
    t_list = []

    tc = in_min / 60
    lc = (int(in_et) - int(in_st)) * tc

    for i in range(lc + 1):
        if i < 10:
            in_time = in_st[0:8] + '0' + str(i)
        else:
            in_time = in_st[0:8] + str(i)

        t_list.append(int(timeTOunixtime(in_time)))

    return t_list


"""
## 함수 : dataParser
메트릭을 파싱하여 반환
"""
def dataParser(s):
    s = s.split("{")
    # print data
    i = 0
    j = len(s)

    if j > 2:
        s = s[3].replace("}", "")
        s = s.replace("]", "")
    else:
        return '0:0,0:0'
    return s



'''
## 함수 : readTSDB
특정 시간의 TSDB값 반환
parameter1 (in_st) : 시작 시각
parameter2 (in_et) : 종료 시각
parameter3 (mid) : 미터기 아이디
반환 (packetlist_filter) : database 값 리스트(list)
'''
def readTSDB(in_st, in_et, mid):
    packetlist = []  # split :
    packetlist_filter = []  # integer

    # YYYY/MM/DD-HH:00:00
    starttime = "%s/%s/%s-%s:00:00" % (in_st[0:4], in_st[4:6], in_st[6:8], in_st[8:10])
    endtime = "%s/%s/%s-%s:00:00" % (in_et[0:4], in_et[4:6], in_et[6:8], in_et[8:10])

    url_tsdb = "http://125.140.110.217:4242/api/query?start=" + starttime + "&end=" + endtime + "&m=avg:test_daily_led" + "%7BMDS_ID=" + str(mid) + "%7D&o=&yrange=%5B0:%5D&wxh=1900x779"
    #print "::: URL PRINT :::", url_tsdb
    tsdbdata = urllib2.urlopen(url_tsdb)

    read_query = tsdbdata.read()
    packets = dataParser(read_query)
    packet = packets.split(',')

    for k in range(len(packet)):
        packetlist.append(packet[k].split(":"))
        tmp = packetlist[k][0]
        packetlist_filter.append([int(tmp[1:len(tmp) - 1]), float(packetlist[k][1])])

    #mid 추가
    for k in range(len(packetlist_filter)):
        packetlist_filter[k].append(mid)

    return packetlist_filter


'''
## 함수 : dateInt
문자열 date를 정수형으로 변환
parameter1 (in_time) : 문자형 date 값
parameter2 (mdh) : 연, 월, 일, 시간의 분류 (y, m, d, h)
반환 (re_mdh) : 변환 된 정수
'''
def dateInt(in_time, mdh):
    # year
    if mdh == 'y':
        re_mdh = int(in_time[0:4])

    # month
    if mdh == 'm':
        if in_time[4] == '0':
            re_mdh = int(in_time[5])
        else:
            re_mdh = int(in_time[4:6])
    # day
    elif mdh == 'd':
        if in_time[6] == '0':
            re_mdh = int(in_time[7])
        else:
            re_mdh = int(in_time[6:8])
    # hour
    elif mdh == 'h':
        if in_time[8] == '0':
            re_mdh = int(in_time[9])
        else:
            re_mdh = int(in_time[8:10])

    return re_mdh



'''
## 함수 : twodigitZero
한자리 정수 에 0을 추가
'''
def twodigitZero(in_num):
    if in_num < 10:
        re_num = '0' + str(in_num)
    else:
        re_num = str(in_num)

    return re_num



'''
## 함수 : nextDate
다음 "연, 월, 일"을 계산
parameter1 (in_time) : 문자형 date 값
parameter2 (in_mdh) : 연, 월, 일, 시간의 분류 (y, m, d, h)
반환 (re_mdh) : 계산 된 다음 날
'''
def nextDate(in_time, in_mdh):
    # next year
    if in_mdh == 'y':
        int_year = dateInt(in_time, 'y')
        next_year = int_year + 1

        re_mdh = str(next_year) + '010000'  # next year/01/01/00

    # next month
    if in_mdh == 'm':
        int_month = dateInt(in_time, 'm')
        next_month = twodigitZero(int_month + 1)

        re_mdh = in_time[0:4] + next_month + '00' + in_time[8:10]  # next month/01/01

    # next day
    elif in_mdh == 'd':
        int_day = dateInt(in_time, 'd')
        next_day = twodigitZero(int_day + 1)

        re_mdh = in_time[0:6] + next_day + in_time[8:10]

    return re_mdh


'''
## 함수 : calDate
특정 시간 사이에 날짜들을 연월일시간(YYMMDDhh)을 반환
parameter1 (sttime) : 시작 시각
parameter2 (ettime) : 종료 시각
반환 (re_datelist) : 날짜 리스트
'''
def calDate(sttime, ettime):
    w_sttime = sttime
    w_ettime = ettime
    tmp_w_sttime = w_sttime[0:8]

    first_loop = 0
    re_datelist = []
    #print "(calDate) DEBUG: sttime: %s, ettime: %s" % (sttime, ettime)

    while 1:

        if first_loop > 0:
            if w_ettime == ettime:
                #print "(calDate) while loop finished ..."
                break
            else:
                w_sttime = nextDate(w_sttime, 'd')
                tmp_w_sttime = w_sttime[0:8]  # ymd

        w_ettime = tmp_w_sttime + '23'

        if w_ettime == ettime:
            first_loop = 1
            re_datelist.append([w_sttime, w_ettime])
            break

        else:  # start time != end time
            if dateInt(ettime, 'y') == dateInt(w_sttime, 'y'):  # same year
                if dateInt(ettime, 'm') > dateInt(w_sttime, 'm'):  # different month

                    # check the last day of start month
                    w_st_calr = calendar.monthrange(int(w_sttime[0:4]), dateInt(w_sttime, 'm'))

                    if dateInt(w_sttime, 'd') == w_st_calr[1]:  # current day == the last day of stday
                        # next month
                        re_datelist.append([w_sttime, tmp_w_sttime + '23'])
                        w_sttime = nextDate(w_sttime, 'm')
                        first_loop = 1
                        continue

            else:  # different year

                tmp_w_sttime = w_sttime[0:4]  # year

                w_st_calr = calendar.monthrange(int(w_sttime[0:4]), dateInt(w_sttime, 'm'))

                if dateInt(w_sttime, 'd') == w_st_calr[1]:  # current day == the last day of stday
                    re_datelist.append([w_sttime, w_ettime])

                    if dateInt(w_sttime, 'm') == 12:  # 12 month
                        # next year
                        w_sttime = nextDate(w_sttime, 'y')
                        tmp_w_sttime = w_sttime[0:8]
                        first_loop = 1
                        continue

                    else:
                        # next month
                        w_sttime = nextDate(w_sttime, 'm')
                        tmp_w_sttime = w_sttime[0:8]
                        first_loop = 1
                        continue

            first_loop = 1

        re_datelist.append([w_sttime, w_ettime])


    return re_datelist



'''
## 함수 : calDate
시간을 유닉스 시간으로 변환
parameter1 (rlt) : 시간 문자열 (YYYYMMDDHH)
반환 (unixtime) : 변환된 유닉스 시간 문자열
'''

def timeTOunixtime(rlt):
    # YYY [0:4]), MM [4:6]), DD 6:8], HH [8:10]
    stime = "%s/%s/%s" % (rlt[6:8], rlt[4:6], rlt[0:4])
    h = rlt[8:10]

    # unixtime need to have 1 sec unit scale
    dechour = int(h) * 60 * 60
    unixday = time.mktime(datetime.datetime.strptime(stime, "%d/%m/%Y").timetuple())
    unixtime = unixday + dechour
    return unixtime

'''
def timeTOunixtime(rlt):
        # YYYY [0:4], MM [4:6], DD [6:8], HH [8:10], m[10:12]
        stime = "%s/%s/%s" % (rlt[6:8], rlt[4:6], rlt[0:4])
        h = rlt[8:10]

        if len(rlt) == 10:  # without minutes
            m = '00'
        else:
            m = rlt[10:12]

        # unixtime need to have 1 sec unit scale
        dechour = int(h) * 60 * 60
        dechour += int(m) * 60
        unixday = time.mktime(datetime.datetime.strptime(stime, "%d/%m/%Y").timetuple())
        unixtime = unixday + dechour

        return unixtime
'''

'''
## 함수 : checkTSDB
미터기 아이디 리스트에서 데이터베이스에 데이터가 있는지 여부를 확인
parameter1 (in_st) : 시작 시각
parameter2 (in_et) : 종료 시각
parameter2 (in_mdsid) : 미터기 아이디
반환 (empty_flag) : 비어있을 경우 1 / 비어있지 않을 경우 0 
'''
def checkTSDB(in_st, in_et, in_mdsid):
    # YYYY/MM/DD-HH:00:00
    starttime = "%s/%s/%s-%s:00:00" % (in_st[0:4], in_st[4:6], in_st[6:8], in_st[8:10])
    endtime = "%s/%s/%s-%s:00:00" % (in_et[0:4], in_et[4:6], in_et[6:8], in_et[8:10])

    url_tsdb = "http://125.140.110.217:4242/api/query?start=" + starttime + "&end=" + endtime + "&m=avg:test_daily_led" + "%7BMDS_ID=" + in_mdsid + "%7D&o=&yrange=%5B0:%5D&wxh=1900x779"

    #print "url_tesdb print : ", url_tsdb
    tsdbdata = urllib2.urlopen(url_tsdb)
    read_query = tsdbdata.read()

    if read_query == '[]':  # check valid matric
        empty_flag = 1
    else:
        empty_flag = 0

    return empty_flag


'''
## 함수 : save_exc
입력 데이터를 엑셀 문서로 저장
column[0]:time / column[1]:value / column[2]:m_id
parameter1 (__vdata) : 데이터 리스트 ([[a, b, c],[d, e, f], ...])
parameter2 (st_time) : 시작 시각
parameter3 (ed_time) : 종료 시각
반환 () : 없음
'''
def save_exc (__vdata, st_time, ed_time):
    __t = str(datetime.datetime.now())
    workbook = xlsxwriter.Workbook('TSDB_' + st_time + '_' + ed_time + '_' +__t+'.xlsx')
    worksheet = workbook.add_worksheet()

    row = 1
    col = 0

    worksheet.write(0, 0, 'time')
    worksheet.write(0, 1, 'value')
    worksheet.write(0, 2, 'm_id')

    for item in (__vdata):
        for col in range(3) :
            worksheet.write(row, col, item[col])
        row += 1
    workbook.close()



'''
## 함수 : verifyMDSID
해당 데이터 리스트에 아이디들이 비어 있는지 확인
parameter1 (in_datelist) : 시각 리스트
parameter2 (in_mdsid_list) : 미터기 아이디 리스트
반환 (retList) : 비어있지 않은 아이디 리스트
'''
def verifyMDSID(in_datelist, in_mdsid_list):
    retList = []

    for i in range(len(in_mdsid_list)):  # number of mdsid list
        for j in range(len(in_datelist)):  # number of date
            empty_tsdb = checkTSDB(in_datelist[j][0], in_datelist[j][1], in_mdsid_list[i])

            if empty_tsdb == 1:
                print "empty: mdsid: %s" %in_mdsid_list[i]
                break

        if empty_tsdb != 1:  # tsdb is not empty
            retList.append(in_mdsid_list[i])

        print "retList: %s, len(retList): %s" %(retList, len(retList))
    return retList


# main function
if __name__ == "__main__":

    sttime = '2016110100'
    entime = '2016113023'

    datelist = []
    retTSDB = []
    avglist = []
    c_vglist = []
    culist = []
    result = []

    datelist = calDate(sttime, entime)

    print datelist

    mdsid_list_full = []
    mdsid_list_full_nverter=[['01223208835-0301', '1602220044', 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['01224230502-0101', '1602160002', 'inverter', 'factory', 'bigcompany', 'metal', 'none'], ['00-360000247', '1602160002', 'inverter', 'bigcompany', 'none', 'metal', 'blower'], ['00-360000189', '1602220018', 'inverter', 'factory', 'bigcompany', 'ceramic', 'none'], ['00-360000226', '1602220018', 'inverter', 'factory', 'bigcompany', 'ceramic', 'none'], ['01223187332-0001', '1602220019', 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['00-360000201', '1602220019', 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['00-360000228', '1602220023', 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['01224230450-0301', '1602220027', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01220533054-0301', '1602220027', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000244', '1602220027', 'inverter', 'bigcompany', 'none', 'departmentStore', 'none'], ['00-360000238', '1602220027', 'inverter', 'bigcompany', 'none', 'departmentStore', 'none'], ['01223208826-0301', '1602220034', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208847-0301', '1602220034', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000152', '1602220034', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000156', '1602220034', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000194', '1602220037', 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['00-360000020', '1602220041', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['01220543054-0301', '1602220043', 'inverter', 'mart', 'bigcompany', 'building_etc', 'none'], ['00-360000233', '1602220043', 'inverter', 'bigcompany', 'none', 'building_etc', 'pump'], ['01220172969-0301', '1602220043', 'inverter', 'mart', 'bigcompany', 'building_etc', 'none'], ['00-360000236', '1602220043', 'inverter', 'bigcompany', 'none', 'building_etc', 'pump'], ['01223208825-0301', '1602220044', 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['00-360000202', '1602220044', 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['00-360000205', '1602220044', 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['00-360000032', '1602220045', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['01223208829-0301', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208779-0301', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208832-0301', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000157', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000159', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000172', '1602230004', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-450083522', '1602230006', 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['01223208800-0301', '1602230007', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208855-0301', '1602230007', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000187', '1602230007', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000199', '1602230007', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208786-0301', '1602230008', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208790-0301', '1602230008', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000155', '1602230008', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000160', '1602230008', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01224273046-0301', '1602230012', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000281', '1602230012', 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['01223239889-0301', '1602230016', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000183', '1602230016', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239881-0301', '1602230018', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000197', '1602230018', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000217', '1602230018', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000229', '1602230023', 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['01223239886-0301', '1602230024', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239888-0301', '1602230024', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000181', '1602230024', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000193', '1602230024', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223181047-0301', '1602230025', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239883-0301', '1602230025', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239890-0301', '1602230025', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000166', '1602230025', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000153', '1602230025', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000092', '1602230026', 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['00-360000025', '1602230033', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000165', '1602230038', 'inverter', 'etc', 'smallcompany', 'none', 'none'], ['00-450083417', '1602230042', 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['00-450083419', '1602230042', 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['00-450083461', '1602230042', 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['00-360000196', '1602230049', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000191', '1602230049', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000086', '1602230095', 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['01224230548-0301', '1602230100', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-450086602', '1602230100', 'inverter', 'bigcompany', 'none', 'departmentStore', 'pump'], ['00-360000004', '1602230101', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000127', '1602230101', 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000093', '1602240002', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000107', '1602240002', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-450083462', '1602240008', 'inverter', 'middlecompany', 'none', 'industryEtc', 'none'], ['00-450083464', '1602240014', 'inverter', 'smallcompany', 'none', 'industryEtc', 'blower'], ['00-360000182', '1602240019', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000231', '1602240019', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000090', '1602240022', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000005', '1602240025', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000264', '1602240031', 'inverter', 'middlecompany', 'none', 'metal', 'fan'], ['00-360000224', '1602240042', 'inverter', 'factory', 'smallcompany', 'food', 'none'], ['00-360000242', '1602250003', 'inverter', 'middlecompany', 'none', 'industryEtc', 'pump'], ['00-360000212', '1602250005', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000213', '1602250009', 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-450083469', '1602250042', 'inverter', 'middlecompany', 'none', 'industryEtc', 'pump'], ['00-360000001', '1602250058', 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['01224273096-0301', '1602250067', 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['01224273066-0301', '1602250067', 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['00-450083467', '1602250067', 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['00-450083466', '1602250067', 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['01224272979-0301', '1602250067', 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['01224272939-0301', '1602250067', 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['00-450086604', '1602250067', 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['00-450083465', '1602250067', 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['00-360000235', '1602250085', 'inverter', 'bigcompany', 'none', 'wood', 'pump'], ['00-360000282', '1602250085', 'inverter', 'bigcompany', 'none', 'wood', 'pump'], ['00-360000214', '1602260070', 'inverter', 'etc', 'etc', 'none', 'none'], ['00-360000185', '1602260082', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000203', '1602260082', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000209', '1602260082', 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000008', '1602260135', 'inverter', 'factory', 'smallcompany', 'fiber', 'none']]
    for i in range(len(mdsid_list_full_nverter)):
        mdsid_list_full.append(mdsid_list_full_nverter[i][0])

    print mdsid_list_full
    print len(mdsid_list_full_nverter)

    # valid mdsid
    mdsid_list = verifyMDSID(datelist, mdsid_list_full)


    for j in range(len(datelist)):
        for i in range(len(mdsid_list)) :
            tmp_tsdb = readTSDB(datelist[j][0], datelist[j][1],mdsid_list[i])
            #print tmp_tsdb
            result = result + tmp_tsdb
    #print result
    #save_exc(result,sttime,entime)


