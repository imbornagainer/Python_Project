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

    url_tsdb = "http://125.140.110.217:4242/api/query?start=" + starttime + "&end=" + endtime + "&m=avg:origin_data_please" + "%7BMDS_ID=" + str(mid) + "%7D&o=&yrange=%5B0:%5D&wxh=1900x779"
    #print "::: URL PRINT :::", url_tsdb
    tsdbdata = urllib2.urlopen(url_tsdb)

    read_query = tsdbdata.read()
    packets = dataParser(read_query)
    packet = packets.split(',')
    if len(packet)<3:
        return []
    for k in range(len(packet)):
        #print len(packet)
        packetlist.append(packet[k].split(":"))
        tmp = packetlist[k][0]
        #print tmp #시간 정보 유닉스타임!!
        packetlist_filter.append([int(tmp[1:len(tmp) - 1]), float(packetlist[k][1])])
        #print [int(tmp[1:len(tmp) - 1]), float(packetlist[k][1])]

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

    url_tsdb = "http://125.140.110.217:4242/api/query?start=" + starttime + "&end=" + endtime + "&m=avg:origin_data_please" + "%7BMDS_ID=" + in_mdsid + "%7D&o=&yrange=%5B0:%5D&wxh=1900x779"

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
                #print "empty: mdsid: %s" %in_mdsid_list[i]
                break

        if empty_tsdb != 1:  # tsdb is not empty
            retList.append(in_mdsid_list[i])

        #print "retList: %s, len(retList): %s" %(retList, len(retList))
    return retList

"""
TSDB의 데이터 값들을 하루 기준으로 최대 93개의 시간(15분 단위 24시간)을 Key로 하여, 딕셔너리 value에 값들의 합을 저장하는 함수!

"""
def makenewMetric(tmp_tsdb,timedic):
    #result는 하루 총 데이터 15분간격의 93개의 수치가 들어있음
    #timedic은 해당 날의 모든 id의 데이터 합을 저장한다.
    #예 :[[1488294000, 0.0, '01224230502-0101'], [1488294900, 0.0, '01224230502-0101'], [1488295800, 0.0, '01224230502-0101'], [1488296700, 0.0, '01224230502-0101'], [1488297600, 0.0, '01224230502-0101'], [1488298500, 0.0, '01224230502-0101'], [1488299400, 0.0, '01224230502-0101'], [1488300300, 0.0, '01224230502-0101'], [1488301200, 0.0, '01224230502-0101'], [1488302100, 0.0, '01224230502-0101'], [1488303000, 0.0, '01224230502-0101'], [1488303900, 0.0, '01224230502-0101'], [1488304800, 0.0, '01224230502-0101'], [1488305700, 0.0, '01224230502-0101'], [1488306600, 0.0, '01224230502-0101'], [1488307500, 0.0, '01224230502-0101'], [1488308400, 0.0, '01224230502-0101'], [1488309300, 0.0, '01224230502-0101'], [1488310200, 1.100000023841858, '01224230502-0101'], [1488311100, 0.0, '01224230502-0101'], [1488312000, 0.0, '01224230502-0101'], [1488312900, 0.0, '01224230502-0101'], [1488313800, 1.100000023841858, '01224230502-0101'], [1488314700, 0.0, '01224230502-0101'], [1488315600, 0.0, '01224230502-0101'], [1488316500, 0.0, '01224230502-0101'], [1488317400, 0.0, '01224230502-0101'], [1488318300, 0.0, '01224230502-0101'], [1488319200, 0.0, '01224230502-0101'], [1488320100, 0.0, '01224230502-0101'], [1488321000, 0.0, '01224230502-0101'], [1488321900, 1.100000023841858, '01224230502-0101'], [1488322800, 0.0, '01224230502-0101'], [1488323700, 0.0, '01224230502-0101'], [1488324600, 0.0, '01224230502-0101'], [1488325500, 0.0, '01224230502-0101'], [1488326400, 0.0, '01224230502-0101'], [1488327300, 0.0, '01224230502-0101'], [1488328200, 1.100000023841858, '01224230502-0101'], [1488329100, 0.0, '01224230502-0101'], [1488330000, 0.0, '01224230502-0101'], [1488330900, 0.0, '01224230502-0101'], [1488331800, 0.0, '01224230502-0101'], [1488332700, 0.0, '01224230502-0101'], [1488333600, 0.0, '01224230502-0101'], [1488334500, 0.0, '01224230502-0101'], [1488335400, 0.0, '01224230502-0101'], [1488336300, 0.0, '01224230502-0101'], [1488337200, 0.0, '01224230502-0101'], [1488338100, 0.0, '01224230502-0101'], [1488339000, 0.0, '01224230502-0101'], [1488339900, 0.0, '01224230502-0101'], [1488344400, 0.0, '01224230502-0101'], [1488345300, 0.0, '01224230502-0101'], [1488346200, 0.0, '01224230502-0101'], [1488347100, 0.0, '01224230502-0101'], [1488348000, 0.0, '01224230502-0101'], [1488348900, 0.0, '01224230502-0101'], [1488349800, 0.0, '01224230502-0101'], [1488350700, 0.0, '01224230502-0101'], [1488366000, 0.0, '01224230502-0101'], [1488366900, 0.0, '01224230502-0101'], [1488367800, 0.0, '01224230502-0101'], [1488368700, 0.0, '01224230502-0101'], [1488369600, 0.0, '01224230502-0101'], [1488370500, 0.0, '01224230502-0101'], [1488371400, 0.0, '01224230502-0101'], [1488372300, 0.0, '01224230502-0101'], [1488373200, 0.0, '01224230502-0101'], [1488374100, 0.0, '01224230502-0101'], [1488375000, 0.0, '01224230502-0101'], [1488375900, 0.0, '01224230502-0101'], [1488376800, 0.0, '01224230502-0101']]
    #하루안에 최대 93개의 timestamp가 존재 하므로 이 시간을 Key값으로 하는 딕셔너리를 만들어 모든 값들의 합을 구한다.

    for data in tmp_tsdb:

        try:
            timedic[data[0]] = timedic[data[0]] + data[1]
        except:
            timedic[data[0]] = data[1]

    return timedic

# main function
if __name__ == "__main__":

    #가끔씩 많은 요청을 할 경우 연결이 끊길 때가 있음!!! 주의 조금씩 넣기!!###############################
    sttime = '2016110100'
    entime = '2016113023'

    datelist = []
    retTSDB = []
    avglist = []
    c_vglist = []
    culist = []
    result = []

    datelist = calDate(sttime, entime)

    print str(sttime[0:4])+"년 "+str(sttime[4:6])+"월 "+str(sttime[6:8])+"일 부터 "+str(entime[0:4])+"년 "+str(entime[4:6])+"월 "+str(entime[6:8]) +"일 까지 데이터\n"

    #에너지 총량을 구하기 위해 추렸던 MDSID정보#
    mdsid_list =['00-450083471', '00-360000189', '00-360000201','01223187332-0001', '00-450083432', '00-360000228', '00-360000217', '00-360000193', '00-360000181', '00-360000092', '00-360000191', '00-360000196', '00-250071151', '00-250130378', '00-450083464', '00-250059775', '00-250059925', '00-250059956', '00-450083463', '00-250059997', '00-250059999', '00-250068218', '00-250130336', '00-250130363', '00-360000213', '00-360000177', '00-251000081', '00-250071467', '00-250130380', '00-250130344', '00-250071438', '00-250102801', '00-250102798', '00-250102710', '00-360000001', '00-250130335', '00-250059861', '00-250007125', '00-250130307', '00-250070994', '00-250059719', '00-250071087', '00-250130381', '00-250130376', '00-250071451', '00-250102648', '00-250059853', '00-250071028', '00-250130359', '00-250130358', '00-250130357', '00-250130356', '00-250130355', '00-250068197', '00-360000214', '00-251004064', '00-251009025', '00-250071144', '00-250071464', '00-250102644', '00-250071172', '00-250071188', '00-250071368', '00-250071319', '00-250130331', '00-250130338', '00-250130323', '00-250059854', '00-250071181', '00-250071005', '00-250071191', '00-250068232', '00-250068192', '00-250068215', '00-250059947', '00-250071625', '00-250071696', '00-250068198', '00-250059803', '00-250070992', '00-250071057', '00-250068178', '00-360000224', '00-250071186', '00-250071681', '00-250060022', '00-250071550', '00-250059813', '00-250059812', '00-250071659', '00-250071310', '00-250071311', '00-250071336', '00-250071387', '00-360000008', '00-250130342', '00-250071507', '00-250130375', '01224273046-0301', '00-360000281', '00-360000229', '00-250071026', '00-250071032', '00-250059909', '00-360000165', '00-250130333', '00-250071086', '00-450083448', '00-250071104', '00-360000107', '00-360000093', '00-250059998', '00-450083462', '00-250068171', '00-250068164', '00-360000182', '00-360000090', '00-360000005', '00-250068144', '00-250059765', '00-250059836', '00-360000212', '00-250130339', '00-360000014', '00-250071679', '00-251009632', '00-250071549', '00-250071370', '00-250071371']

    print "총 "+str(len(datelist)) +"일 기간의 데이터 넣는중!.....\n"
    #mdsid_list = verifyMDSID(datelist, mdsid_list_full) #http request를 너무 많이 전송해서 연결이 자꾸 끊겨서 검증은 readTSDB함수에 넣어버림


    for j in range(len(datelist)):
        timedic={}
        count=0
        print "DONE : "+ str(datelist[j][0][0:4]) +"-"+str(datelist[j][0][4:6]) +"-"+str(datelist[j][0][6:8])
        for i in range(len(mdsid_list)) :

            tmp_tsdb = readTSDB(datelist[j][0], datelist[j][1],mdsid_list[i])
            if len(tmp_tsdb)==0:
                count=count+1
            else:
                timedic=makenewMetric(tmp_tsdb,timedic)
        #print timedic
        #하루의 모든 아이디별 데이터의 합이 구해지면, tsdb에 새로운 메트릭으로 저장한다.
        for td in timedic.items():
            #print td
            data = {
                "metric": "sum_origin_energy",
                "timestamp": td[0],
                "value": td[1],  # 원본데이터 합
                "tags": {

                    "test":0
                }
            }
            url_t = "http://125.140.110.217:4242/api/put"
            ret = requests.post(url_t, data=json.dumps(data))

        print "     위의 기간에서 총 " + str(len(mdsid_list)) + "개의 MDSID 중, " + str(len(mdsid_list)-count) + "개가 데이터가 있음!!\n"

