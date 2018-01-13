# -*- coding: utf-8 -*-
# Author : https://github.com/eunsooLim
# Author : https://github.com/jeonghoonkang

from __future__ import print_function 
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
import save_list_2_excel

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


def readTSDB(in_st, in_et, mid,led_inverter):

    # YYYY/MM/DD-HH:00:00
    starttime = "%s/%s/%s-%s:00:00" % (in_st[0:4], in_st[4:6], in_st[6:8], in_st[8:10])
    endtime = "%s/%s/%s-%s:00:00" % (in_et[0:4], in_et[4:6], in_et[6:8], in_et[8:10])

    url_tsdb = "http://localhost:4242/api/query?start=" + starttime + "&end=" + endtime + "&m=sum:"+ led_inverter+ "{MDS_ID=" + mid + "}"

    try:
        tsdbdata = urllib2.urlopen(url_tsdb)

        read_query = tsdbdata.read()
        packets = dataParser(read_query)
        packet = packets.split(',')
        if packet[0] !='0:0': #데이터 check!!!
            DATA_CHECK[mid]=1
            NO_DATA_CHECK[mid]=0
            print ("t", end=' '),
        else :
            if DATA_CHECK[mid] == 1: 
                return 
            NO_DATA_CHECK[mid] = 1
            # if exception occur,
    except:
        NO_DATA_CHECK[mid] = 1
        print (" no data " + str(mid))

    packet = None
    time.sleep(0.05)



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

    if ( ettime[-2:] != '23' ) : exit( "please make sure 23, of the end day time, like 2017110723")

    first_loop = 0
    re_datelist = []
    #print "(calDate) DEBUG: sttime: %s, ettime: %s" % (sttime, ettime)

    while 1:
        if first_loop > 0:
            if w_ettime == ettime:
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


# main function
if __name__ == "__main__":

    sttime = '2016110100' #기간 설정!!
    entime = '2016110123' #should be 23 (last hour)

    datelist = []

    DATA_CHECK={} # 데이터가 있는지 없는지 체크
    NO_DATA_CHECK={} # 데이터가 있는지 없는지 체크
    datelist = calDate(sttime, entime) #기간 에 대한 시간 리스트 만들기

    #임의의 MDS_ID들!!->엘이디 406개 (사전계측용량이 있는 것들)
    led_MDSID_list=['00-250071531', '00-250130341', '00-250130340', '00-250130343', '00-250130342', '00-250130345', '00-250130344', '00-250068220', '00-250068221', '00-250068224', '00-250068225', '00-250068226', '00-250068227', '00-250068229', '00-250060000', '00-250060001', '00-250060002', '00-250130323', '00-250130338', '00-250130339', '00-250130335', '00-250130331', '00-250071407', '00-250071405', '00-250071403', '00-250071153', '00-250068134', '00-250068135', '00-250068136', '00-250068137', '00-250071408', '00-250071409', '00-450083448', '00-450083445', '00-450083446', '00-250071140', '00-250071121', '00-250068148', '00-250071122', '00-250071126', '00-250068141', '00-250068140', '00-250068143', '00-250068145', '00-250068144', '00-250068146', '00-250071308', '00-250071659', '00-250059992', '00-250059996', '00-250059997', '00-250059998', '00-250059999', '00-250071495', '00-250102710', '00-250071394', '00-250071392', '00-250059823', '00-250071012', '00-250071575', '00-250070999', '00-250130385', '00-250130384', '00-250070994', '00-250071370', '00-250130380', '00-250059860', '00-250059861', '00-250071151', '00-250059798', '00-450086528', '00-250059768', '00-25-0059761', '00-250059765', '00-250071681', '00-250059766', '00-250071359', '00-250130374', '00-250130375', '00-250130376', '00-250130377', '00-250130378', '00-250130379', '00-250068170', '00-250068171', '00-250068172', '00-250068173', '00-250068175', '00-250068176', '00-250068177', '00-250068178', '00-250068179', '00-250068189', '00-250068188', '00-250068185', '00-250068180', '00-250068182', '00-250071025', '00-250071026', '00-250071459', '00-250071451', '00-250071029', '00-250071453', '00-250071183', '00-250071182', '00-250071181', '00-250071186', '00-250071185', '00-250071184', '00-250071189', '00-250071188', '00-250071052', '00-250071055', '00-250071057', '00-250068071', '00-360000245', '00-360000241', '00-250071330', '00-250059948', '00-250071624', '00-250071625', '00-250059945', '00-250059947', '00-251004742', '00-250071525', '00-250071527', '00-250071521', '00-250071520', '00-250059835', '00-250059720', '00-250059836', '00-250059724', '00-250059839', '00-250068232', '00-250068231', '00-250068230', '00-450086517', '00-450086512', '00-250059754', '00-250059751', '00-250130327', '00-250130326', '00-250130325', '00-250130324', '00-250059758', '00-250130321', '00-250130320', '00-250071144', '00-250071414', '00-250071417', '00-250071416', '00-250052077', '00-250059819', '00-250071667', '00-250059989', '00-250071661', '00-250071700', '00-250059982', '00-250071464', '00-250071465', '00-250071467', '00-250071468', '00-250071469', '00-250068139', '00-250102649', '00-250102648', '00-250102644', '00-250130307', '00-250071068', '00-250070992', '00-250071061', '00-250071066', '00-250059816', '00-250071005', '00-250059775', '00-250070991', '00-250071369', '00-250071368', '00-250059871', '00-250059873', '00-250071364', '00-250059875', '00-250059874', '00-250059975', '00-250059976', '00-250059818', '00-250059703', '00-250071696', '00-250068193', '00-250059783', '00-250059814', '00-250059784', '00-250059813', '00-250059789', '00-250059812', '00-250071518', '00-250059705', '00-250071510', '00-250059718', '00-250059719', '00-250059807', '00-460003531', '00-250059717', '00-250130363', '00-250130362', '00-250130361', '00-250130367', '00-250130365', '00-250130369', '00-250130368', '00-250068162', '00-250068161', '00-250068160', '00-250068167', '00-250068166', '00-250068165', '00-250068164', '00-250068169', '00-250071059', '00-251008570', '00-250068219', '00-250059849', '00-250071428', '00-250071032', '00-250071031', '00-250071030', '00-250071424', '00-250071039', '00-250071427', '00-450083463', '00-250068149', '00-250071109', '00-250071104', '00-250071632', '00-250071088', '00-250071089', '00-250071086', '00-250071087', '00-250071192', '00-250071085', '00-250059949', '00-250102776', '00-250071336', '00-250071550', '00-250071557', '00-250071558', '00-250071559', '00-250059841', '00-250059928', '00-250059848', '00-250059926', '00-250059925', '00-250059921', '00-250060022', '00-450086506', '00-450086503', '00-250130318', '00-250130312', '00-250130313', '00-250130310', '00-250130316', '00-250130317', '00-250130314', '00-250130315', '00-250071172', '00-250071170', '00-250071171', '00-250071176', '00-250071175', '00-250059780', '00-250071493', '00-25-0071065', '00-250071373', '00-360000177', '00-250068208', '00-250068207', '00-250068202', '00-250068203', '00-250068201', '00-360000216', '00-250071677', '00-250071679', '00-250071678', '00-360000218', '00-250071442', '00-251000081', '00-250071073', '00-250071072', '00-250071074', '00-250059887', '00-250071217', '00-250130381', '00-250071218', '00-250071356', '00-250071357', '00-250071355', '00-250059961', '00-250059960', '00-250059965', '00-250059964', '00-250059968', '00-250071622', '00-250130383', '00-250071509', '00-250071507', '00-250071504', '00-250059709', '00-250059708', '00-250130358', '00-250130359', '00-250130356', '00-250130357', '00-250059701', '00-250130355', '00-250059707', '00-250071692', '00-250059811', '00-250059704', '00-250059715', '00-250059803', '00-250059801', '00-250071438', '00-250071004', '00-250059834', '00-250071432', '00-250071434', '00-450083458', '00-250068158', '00-250068159', '00-250068157', '00-250068154', '00-250068153', '00-250068150', '00-250071319', '00-250071640', '00-250071312', '00-250071310', '00-250071311', '00-250071097', '00-250071096', '00-250071091', '00-250071090', '00-250071099', '00-250071098', '00-250071481', '00-250052085', '00-250070993', '00-250071371', '00-250071372', '00-250130382', '00-250071694', '00-250007125', '00-250071540', '00-250071549', '00-250071548', '00-250059853', '00-250059852', '00-250059851', '00-250059856', '00-250059855', '00-250059854', '00-250059859', '00-250059858', '00-250059916', '00-250059917', '00-250059915', '00-250071138', '00-250059706', '00-250059770', '00-250130306', '00-250059777', '00-250059774', '00-250071699', '00-250059778', '00-250130309', '00-250130308', '00-250071647', '00-251008614', '00-250068192', '00-250068218', '00-250068196', '00-250068197', '00-250068210', '00-250068198', '00-250068212', '00-250068215', '00-250068217', '00-250071190', '00-250071191', '00-250071440', '00-250071449', '00-450083404', '00-450083403', '00-250102620', '00-250071168', '00-250071165', '00-250071167', '00-250071166', '00-250071582', '00-250071581', '00-250071612', '00-250059959', '00-250059956', '00-250059957', '00-250059954', '00-250071290']


        #['00-250071531','00-250130341','00-250130340', '00-250130343', '00-250130342', '00-250130345', '00-250130344', '00-250068220', '00-250068221', '00-250068224']

    #인버터인지 led인지 확인해야 함!!!!!!!! 메트릭 이름이 다르다!!!!

    led_inverter='origin_data_led_smk' # LED
    #led_inverter='origin_data_inverter_smk' # 인버터

    print ("총 "+str(len(datelist))+"일의 기간 동안에서 조사중입니다. 기다려 주세요!!\n")
    for j in range(len(datelist)):


        for i in range(len(led_MDSID_list)):

            readTSDB(datelist[j][0], datelist[j][1], led_MDSID_list[i],'origin_data_led_smk')

        print ("조사 완료 : " + str(datelist[j][0][0:4]) + "-" + str(datelist[j][0][4:6]) + "-" + str(datelist[j][0][6:8]))

    num = DATA_CHECK.__len__()
    print ("총 "+str(len(led_MDSID_list))+"개의 MDS ID 리스트 중에서,,,,"+str(num)+"개가 TSDB에 존재한다!\n")

    #DATA_CHECK 는 해당 기간동안 TSDB에 한번이라도 데이터가 있다면(데이터가 0.0일지라도), id 모음!!

    data_yes_list_in_tsdb=[] # TSDB에 데이터가 있는 MDSID 리스트!!
    for id in DATA_CHECK.items():
        data_yes_list_in_tsdb.append(id[0])
    print ("TSDB에 데이터가 있는 MDSID 리스트!!")

    print
    print (data_yes_list_in_tsdb) # TSDB에 데이터가 있는 MDSID 리스트!!
    
    no_data_list_in_tsdb=[] # TSDB에 데이터가 있는 MDSID 리스트!!
    #엑셀파일생성, 리스트 저장
    cfile = save_list_2_excel.excell_class()    
    cfile.save_list_2_exl('__data_list_%s' %num, data_yes_list_in_tsdb)

    for id in NO_DATA_CHECK.items():
        if NO_DATA_CHECK[id[0]] == 1: no_data_list_in_tsdb.append(id[0])
    
    print ("TSDB No Data  MDSID 리스트!!")
    print (no_data_list_in_tsdb)
    
    num = len(no_data_list_in_tsdb)
    cfile.save_list_2_exl('__nodata_list_%s' %num, no_data_list_in_tsdb)
    
    print ("총 "+str(len(led_MDSID_list))+"개의 MDS ID 리스트 중에서,,,,"+str(num)+"개 no data \n")





