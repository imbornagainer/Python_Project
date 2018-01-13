# -*- coding: utf-8 -*-
# Author : eunsooLim , https://github.com/eunsooLim
# Author : jeonghoonkang , https://github.com/jeonghoonkang


import time
import datetime
import cx_Oracle
import os
import sys
import requests
import json
import time, datetime
import pandas as pd
import numpy as np


url = "http://125.140.110.217:4242/api/put"
response ={}

con = cx_Oracle.connect('keti_user/keti1357!#@125.141.144.149/aimir')
cur = con.cursor()

# 가동율을 구하기 위한 시간범위 설정, 0~9시, 9~12시, 12~13시, 13~18시, 18~23시
timezone=[('00','09'),('09','12'),('12','13'),('13','18'),('18','23')]

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
def updateMINONE(in_sttime, in_entime,in_mdsid,tagdata):

    starttime = in_sttime
    endtime = in_entime
    mdsid = in_mdsid

    sql_tmp = "select ELE.LP_TIME, ELE.VALUE_00, ELE.VALUE_15, ELE.VALUE_30, ELE.VALUE_45, ECU.NAME, ECO.LOCATION, ECO.SIC, ELE.MDS_ID, ELE.DEVICE_SERIAL, ECU.CUSTOMERNO, ELE.CHANNEL from EMNV_LP_EM_VIEW  ELE join EMNV_CONTRACT_VIEW ECO on ELE.MDS_ID = ECO.MDS_ID join EMNV_CUSTOMER_VIEW ECU on ECO.CUSTOMERNO = ECU.CUSTOMERNO where (ELE.CHANNEL=1) and (ELE.LP_TIME between '%s' and '%s') and (ELE.MDS_ID='%s') order by ELE.MDS_ID ASC, ELE.LP_TIME ASC" %(starttime, endtime, mdsid)

    minlist = ['00', '15', '30', '45']
    timedic={0:0.0,1:0.0,2:0.0,3:0.0,4:0.0}
    lcfm = len(minlist)
    day={}
    cur.execute(sql_tmp)
    print "sql 추출!"

    ix = 0
    count=0
    donecheck=0
    cccc=0
    donecheck=0
    for result in cur:
        donecheck=donecheck+1
       # print '\n'
        result=list(result)
        for ii in [1,2,3,4]:
            if str(result[ii]) == 'None':
                result[ii] = 0.0
        cccc=1
        #날짜 밀림 확인 필요!!
        try:
            day[result[0][0:8]]
        except:
            day[result[0][0:8]] = [0.0, 0.0, 0.0, 0.0, 0.0]

        if count%24<9:
            day[result[0][0:8]][0]= day[result[0][0:8]][0]+result[1]+result[2]+result[3]+result[4]

        elif count%24<12:
            day[result[0][0:8]][1] =  day[result[0][0:8]][1] + result[1] + result[2] + result[3] + result[4]

        elif count%24<13:
            day[result[0][0:8]][2] =  day[result[0][0:8]][2] + result[1] + result[2] + result[3] + result[4]

        elif count%24 < 18:
            day[result[0][0:8]][3] =  day[result[0][0:8]][3] + result[1] + result[2] + result[3] + result[4]
        else :
            day[result[0][0:8]][4] =  day[result[0][0:8]][4] + result[1] + result[2] + result[3] + result[4]


        count= count+1
        #print result[0] #1단계
    nuzukdic={}

    donecount=0
    if donecheck==0:
        print "데이터 없음!"
        return donecheck

    print "\n넣는중........\n"

    for a,v in day.items():
        v[0]=min(v[0]/9.0,1)
        v[1]=min(v[1]/3.0,1)
        v[2]=min(v[2],1.0)
        v[3]=min(v[3]/5.0,1)
        v[4]=min(v[4]/6.0,1)

        #print a,"--", v
        timedivision=[9,3,1,5,6]
        hourdic={0:'00'}

        donecount=donecount+1
        value=0.0

        week = ('Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')



        for hour in range(24):
            if hour<9:
                uxtime = timeTOunixtime(a+'0'+str(hour))
                value=v[0]
            elif hour < 12:
                if hour==9:
                    uxtime = timeTOunixtime(a + '0' + str(hour))
                else:
                    uxtime = timeTOunixtime(a + str(hour))
                value=v[1]

            elif hour < 13:
                uxtime = timeTOunixtime(a + str(hour))
                value=v[2]

            elif hour < 18:
                uxtime = timeTOunixtime(a + str(hour))
                value=v[3]

            else :
                uxtime = timeTOunixtime(a  + str(hour))
                value=v[4]
            try:
                    nuzukdic[hour]
            except:
                    nuzukdic[hour]=0.0

            htag = 0
            if(week[datetime.date(int(a[0:4]),int(a[4:6]),int(a[6:8])).weekday()]=='Sun'):
                htag=1

            elif (week[datetime.date(int(a[0:4]), int(a[4:6]), int(a[6:8])).weekday()] == 'Sat'):
                htag = 1

            else:  #평일일 경우!!
                if value != 0:
                    nuzukdic[hour] = (value + nuzukdic[hour]) / 2.0

            data = {
                "metric": "daily_workingrate",
                "timestamp": uxtime,
                "value": value,
                "tags": {
                    "MDS_ID": result[8],
                    "Saupjang": tagdata[1],
                    "led_inverter" : tagdata[2],
                    "factory_mart" : tagdata[3],
                    "company_size":tagdata[4],
                    "business_type": tagdata[5],
                    "fan_pump":tagdata[6],
                    "holiday": htag,
                }
            }

            nuzuk_data = {
                "metric": "nuzuk_workingrate",
                "timestamp": uxtime,
                "value": nuzukdic[hour],
                "tags": {
                    "MDS_ID": result[8],
                    "Saupjang": tagdata[1],
                    "led_inverter" : tagdata[2],
                    "factory_mart" : tagdata[3],
                    "company_size":tagdata[4],
                    "business_type": tagdata[5],
                    "fan_pump":tagdata[6],
                    "holiday": htag,
                }
                }

            ret=requests.post(url, data=json.dumps(data))
            ret =requests.post(url, data=json.dumps(nuzuk_data))


            """if(int((float(donecount)*100/float(donecheck)))%10==0 and hour==23):
                 print "***" + str(int((float(donecount)/float(donecheck))*10000)) +"% 진행중...  ***"
                 if(float(donecount)/float(donecheck))*10000 > 99 :
                     print "조금만 기다려 주세요."""""



    return donecheck
def make_id_use_excel():
    led_id = []
    inverter_id = []
    saupjang_info = pd.read_csv("saupjang_info.csv")  # 사업장정보 csv 파일로 바꾼것!
    inverter_info = pd.read_csv("inverter_info.csv")  # EE자원 엑셀 중 인버터정보를 csv파일로 바꾼것
    led_info = pd.read_csv("led_info.csv")  # EE자원 엑셀 중 led정보를 csv파일로 바꾼것

    list_info = pd.read_csv("insertlist.csv")  # 추천리스트400개

    # 사업장정보,엘이디인버터 엑셀들에서 얻을 수 있는 정보들을 영어로 바꾸기 위한 사전!
    dictionary = {"공장": "factory", "일반건물": "office", "마트": "mart", "공동주택": "apt", "대형마트": "mart", "기타": "etc",  # 용도
                  "대기업": "bigcompany", "중견": "middlecompany", "중소": "smallcompany", "비영리법인": "etc", "해당없음": "etc",
                  "병원": "hospital",  # 사업장구분
                  "금속": "metal", "산업기타": "industryEtc", "건물기타": "building_etc", "제지목재": "wood", "요업": "ceramic",
                  "백화점": "departmentStore", "섬유": "fiber", "학교": "school", "식품": "food", "화공": "ceramic",
                  "상용": "sangyong",  # 세부용도
                  "LED": "led", "인버터": "inverter", "형광등": "heungwanglamp", "메탈할라이드": "metalhalide",  # 품목
                  np.NaN: "none", "블로워": "blower", "컴프래서": "compressor", "펌프": "pump", "팬": "fan", }  # 부하형태

    for id in list_info.iterrows():  # 추천리스트400개
        insertdata = []
        if id[1][0] == 1:  # default1_led2_inverter3 -사업장엑셀에있는지(파란색),엘이디(빨간색),인버터(보라색)
            # 사업장엑셀에 정보가 있는 경우
            info_data = saupjang_info[saupjang_info['사업장번호'] == id[1][2]]  # 사업장 아이디 일치하는 것 찾기
            # pandas 시리즈 객체의 value추출법! :sieries object.values[index]
            insertdata.append(id[1][1])  # mdsid
            insertdata.append(id[1][2])  # 사업장번호
            insertdata.append(dictionary[info_data['품목'].values[0]])  # 인버터,led정보
            insertdata.append(dictionary[info_data['용도'].values[0]])  # 공장 마트 정보
            insertdata.append(dictionary[info_data['사업장구분'].values[0]])  # 중소기업 대기업정보
            insertdata.append(dictionary[info_data['세부용도'].values[0]])  # 섬유,금속 정보

            if dictionary[info_data['품목'].values[0]] == 'led':
                led_id.append(insertdata)  # 엘이디 정보 모음리스트에 넣기

            else:  # 인버터의 경우 팬,블로워정보는 빈칸으로 두기(정보를 찾을 수 없어서)
                insertdata.append('none')  # 팬,블로워정보 -없을 때에는 none으로 대체함! 빈 데이터는 tsdb에 들어가지 않는다!!!!!!!!!!!!
                inverter_id.append(insertdata)  # 인버터 정보 모음리스트에 넣기

        elif id[1][0] == 2:  # 엘이디 엑셀에 정보가 있는 경우
            info_data = led_info[led_info['계량기시리얼넘버'] == (id[1][1])]  # mdsid로 검색해 일치하는 것 찾기!!
            insertdata.append(id[1][1])  # mdsid
            insertdata.append(id[1][2])  # 사업장번호
            insertdata.append(dictionary[info_data['계측설비형태'].values[0]])  # led/형광등/메탈할라이드
            insertdata.append(dictionary[info_data['건물용도'].values[0]])  # 공장,마트
            insertdata.append(dictionary[info_data['기업유형(사업장)'].values[0]])  # 대기업,중견기업

            info_data = saupjang_info[saupjang_info['사업장번호'] == id[1][2]]  # 사업장 아이디 일치하는 것 찾기->세부정보 채우기
            if len(info_data) > 0:  # 사업장 엑셀에 정보가 있는 경우
                insertdata.append(dictionary[info_data['세부용도'].values[0]])
            else:
                insertdata.append('none')

            led_id.append(insertdata)  # 엘이디 정보 모음리스트에 넣기

        else:  # 인버터 엑셀에 정보가 있는 경우
            info_data = inverter_info[inverter_info['계량기시리얼넘버'] == str(id[1][1])]  # mdsid로 검색해 일치하는 것 찾기!!
            insertdata.append(id[1][1])  # mdsid
            insertdata.append(id[1][2])  # 사업장번호
            insertdata.append('inverter')
            insertdata.append(dictionary[info_data['건물용도'].values[0]])  # 공장,마트
            insertdata.append('none')  # 인버터엑셀에는 대기업/중견/의 기업정보가 없다.사업장에서 검색해서 체워야함!!
            buha = dictionary[info_data['부하형태'].values[0]]

            info_data = saupjang_info[saupjang_info['사업장번호'] == id[1][2]]  # 사업장 아이디 일치하는 것 찾기
            if len(info_data) > 0:  # 사업장 엑셀에 정보가 있는 경우 세부용도추가
                insertdata.append(dictionary[info_data['세부용도'].values[0]])
                insertdata[3] = dictionary[info_data['사업장구분'].values[0]]  # 기업정보가 존재하면 빈값에서 값 바꿔주기
            else:
                insertdata.append('none')

            insertdata.append(buha)  # 순서를 지키기 위해 부하형태(팬,펌프,,)는 맨마지막에 넣기
            inverter_id.append(insertdata)  # 인버터 정보 모음리스트에 넣기#

    return inverter_id

# main function
if __name__ == "__main__":
    #2017-06-8일 기준
    #20161101-20170430 까지 진행
    #태그 추가하여 진행-태그정보는 Readme.md에 업데이트!

        sttime = "2016110100"
        entime = "2017043023"
        filename='INVERTER_resultcsv'+sttime+"to"+entime+".txt"
        resultfile=open(filename,"w")
        ix=1
        tagdata = ['aa','aa','aa','aa','aa']
        inverter_id=[['01223208835-0301', 1602220044L, 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['01224230502-0101', 1602160002L, 'inverter', 'factory', 'bigcompany', 'metal', 'none'], ['00-360000247', 1602160002L, 'inverter', 'bigcompany', 'none', 'metal', 'blower'], ['00-360000189', 1602220018L, 'inverter', 'factory', 'bigcompany', 'ceramic', 'none'], ['00-360000226', 1602220018L, 'inverter', 'factory', 'bigcompany', 'ceramic', 'none'], ['01223187332-0001', 1602220019L, 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['00-360000201', 1602220019L, 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['00-360000228', 1602220023L, 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['01224230450-0301', 1602220027L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01220533054-0301', 1602220027L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000244', 1602220027L, 'inverter', 'bigcompany', 'none', 'departmentStore', 'none'], ['00-360000238', 1602220027L, 'inverter', 'bigcompany', 'none', 'departmentStore', 'none'], ['01223208826-0301', 1602220034L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208847-0301', 1602220034L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000152', 1602220034L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000156', 1602220034L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000194', 1602220037L, 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['00-360000020', 1602220041L, 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['01220543054-0301', 1602220043L, 'inverter', 'mart', 'bigcompany', 'building_etc', 'none'], ['00-360000233', 1602220043L, 'inverter', 'bigcompany', 'none', 'building_etc', 'pump'], ['01220172969-0301', 1602220043L, 'inverter', 'mart', 'bigcompany', 'building_etc', 'none'], ['00-360000236', 1602220043L, 'inverter', 'bigcompany', 'none', 'building_etc', 'pump'], ['01223208825-0301', 1602220044L, 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['00-360000202', 1602220044L, 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['00-360000205', 1602220044L, 'inverter', 'office', 'bigcompany', 'departmentStore', 'none'], ['00-360000032', 1602220045L, 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['01223208829-0301', 1602230004L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208779-0301', 1602230004L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208832-0301', 1602230004L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000157', 1602230004L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000159', 1602230004L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000172', 1602230004L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-450083522', 1602230006L, 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['01223208800-0301', 1602230007L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208855-0301', 1602230007L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000187', 1602230007L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000199', 1602230007L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208786-0301', 1602230008L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223208790-0301', 1602230008L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000155', 1602230008L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000160', 1602230008L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01224273046-0301', 1602230012L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000281', 1602230012L, 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['01223239889-0301', 1602230016L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000183', 1602230016L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239881-0301', 1602230018L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000197', 1602230018L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000217', 1602230018L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000229', 1602230023L, 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['01223239886-0301', 1602230024L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239888-0301', 1602230024L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000181', 1602230024L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000193', 1602230024L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223181047-0301', 1602230025L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239883-0301', 1602230025L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['01223239890-0301', 1602230025L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000166', 1602230025L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000153', 1602230025L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000092', 1602230026L, 'inverter', 'factory', 'smallcompany', 'fiber', 'none'], ['00-360000025', 1602230033L, 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000165', 1602230038L, 'inverter', 'etc', 'smallcompany', 'none', 'none'], ['00-450083417', 1602230042L, 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['00-450083419', 1602230042L, 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['00-450083461', 1602230042L, 'inverter', 'bigcompany', 'none', 'departmentStore', 'fan'], ['00-360000196', 1602230049L, 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000191', 1602230049L, 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000086', 1602230095L, 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['01224230548-0301', 1602230100L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-450086602', 1602230100L, 'inverter', 'bigcompany', 'none', 'departmentStore', 'pump'], ['00-360000004', 1602230101L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000127', 1602230101L, 'inverter', 'mart', 'bigcompany', 'departmentStore', 'none'], ['00-360000093', 1602240002L, 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000107', 1602240002L, 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-450083462', 1602240008L, 'inverter', 'middlecompany', 'none', 'industryEtc', 'none'], ['00-450083464', 1602240014L, 'inverter', 'smallcompany', 'none', 'industryEtc', 'blower'], ['00-360000182', 1602240019L, 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000231', 1602240019L, 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000090', 1602240022L, 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000005', 1602240025L, 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000264', 1602240031L, 'inverter', 'middlecompany', 'none', 'metal', 'fan'], ['00-360000224', 1602240042L, 'inverter', 'factory', 'smallcompany', 'food', 'none'], ['00-360000242', 1602250003L, 'inverter', 'middlecompany', 'none', 'industryEtc', 'pump'], ['00-360000212', 1602250005L, 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-360000213', 1602250009L, 'inverter', 'factory', 'smallcompany', 'industryEtc', 'none'], ['00-450083469', 1602250042L, 'inverter', 'middlecompany', 'none', 'industryEtc', 'pump'], ['00-360000001', 1602250058L, 'inverter', 'factory', 'middlecompany', 'industryEtc', 'none'], ['01224273096-0301', 1602250067L, 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['01224273066-0301', 1602250067L, 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['00-450083467', 1602250067L, 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['00-450083466', 1602250067L, 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['01224272979-0301', 1602250067L, 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['01224272939-0301', 1602250067L, 'inverter', 'office', 'bigcompany', 'sangyong', 'none'], ['00-450086604', 1602250067L, 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['00-450083465', 1602250067L, 'inverter', 'bigcompany', 'none', 'sangyong', 'fan'], ['00-360000235', 1602250085L, 'inverter', 'bigcompany', 'none', 'wood', 'pump'], ['00-360000282', 1602250085L, 'inverter', 'bigcompany', 'none', 'wood', 'pump'], ['00-360000214', 1602260070L, 'inverter', 'etc', 'etc', 'none', 'none'], ['00-360000185', 1602260082L, 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000203', 1602260082L, 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000209', 1602260082L, 'inverter', 'factory', 'bigcompany', 'industryEtc', 'none'], ['00-360000008', 1602260135L, 'inverter', 'factory', 'smallcompany', 'fiber', 'none']]
        toendpoint = len(inverter_id)

        for i in range (toendpoint):

            tagdata=inverter_id[i]
            mds_id=inverter_id[i][0]
            # Oracle -> OpenTSDB 기능 실행
            donecheck = updateMINONE(sttime, entime, mds_id, tagdata)
            if donecheck > 0:
                print "들어간 데이터 량"+ str(donecheck)

            resultfile.write(str(mds_id)+","+str(donecheck)+"\n")

            print "ix: %s, mdsid: %s 전체 진행률: %s 퍼센트 진행!" %(ix, mds_id,int(float((ix)/float(toendpoint))*100.0))
            resultfile.flush()

            # 화면에 메세지 출력할때,
            # 줄이 바뀌지 않고. 한줄에만 덮혀서 출력함

            # pout = "ix: %s, mdsid: %s, donecheck: %d \r" %(ix, mds_id, donecheck)
            # sys.stdout.write(pout)
            # sys.stdout.flush()

            ix=ix+1

        cur.close()
        con.close()
