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
    saupjang_info = pd.read_csv("saupjang_info.csv")  # 사업장정보 csv 파일로 바꾼것!
    inverter_info = pd.read_csv("inverter_info.csv")  # EE자원 엑셀 중 인버터정보를 csv파일로 바꾼것
    led_info = pd.read_csv("led_info.csv")  # EE자원 엑셀 중 led정보를 csv파일로 바꾼것

    list_info = pd.read_csv("insertlist.csv")  # 추천리스트400개#

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
        inverter_id=[]
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
            inverter_id.append(insertdata)  # 인버터 정보 모음리스트에 넣기

    return led_id



# main function
if __name__ == "__main__":
    #2017-06-8일 기준
    #20161101-20170430 까지 진행
    #태그 추가하여 진행-태그정보는 Readme.md에 업데이트!

        sttime = "2016110100"
        entime = "2017043023"
        filename='led_resultcsv'+sttime+"to"+entime+".txt"
        resultfile=open(filename,"w")
        ix=1
        tagdata = ['aa','aa','aa','aa','aa']
        led_id=[['00-250102796', 1602250039L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071089', 1601140003L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250060001', 1601140004L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130385', 1601140005L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250071424', 1601140006L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059766', 1602010003L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059871', 1602040002L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059708', 1602040003L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071598', 1602040004L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250052077', 1602040007L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-250102776', 1602040008L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250071373', 1602040010L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071403', 1602150001L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071434', 1602150003L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071308', 1602170004L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071330', 1602170004L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-251004742', 1602170009L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250071525', 1602170011L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-460003531', 1602180002L, 'led', 'factory', 'bigcompany', 'fiber'], ['00-250071405', 1602180008L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068220', 1602190007L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068226', 1602190007L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059921', 1602190008L, 'led', 'etc', 'smallcompany', 'none'], ['00-250059949', 1602190008L, 'led', 'etc', 'smallcompany', 'none'], ['00-250068179', 1602190009L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071520', 1602220006L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-450083471', 1602220010L, 'led', 'factory', 'bigcompany', 'metal'], ['00-250068178', 1602220012L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250071427', 1602220014L, 'led', 'factory', 'middlecompany', 'ceramic'], ['00-250071507', 1602220020L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083432', 1602220022L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250071428', 1602220026L, 'led', 'apt', 'apt', 'none'], ['00-250070991', 1602220026L, 'led', 'apt', 'apt', 'none'], ['00-250071407', 1602220026L, 'led', 'apt', 'apt', 'none'], ['00-250130341', 1602220029L, 'led', 'apt', 'apt', 'none'], ['00-450083468', 1602220031L, 'led', 'factory', 'bigcompany', 'metal'], ['00-250071364', 1602220032L, 'led', 'apt', 'apt', 'none'], ['00-250071217', 1602220032L, 'led', 'apt', 'apt', 'none'], ['00-250102673', 1602220033L, 'led', 'factory', 'bigcompany', 'metal'], ['00-250059834', 1602220035L, 'led', 'apt', 'apt', 'none'], ['00-250071449', 1602220038L, 'led', 'office', 'bigcompany', 'departmentStore'], ['00-250071440', 1602220038L, 'led', 'office', 'bigcompany', 'departmentStore'], ['00-250071453', 1602220038L, 'led', 'office', 'bigcompany', 'departmentStore'], ['00-250071548', 1602220042L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250059976', 1602220048L, 'led', 'factory', 'smallcompany', 'wood'], ['00-250071459', 1602220051L, 'led', 'factory', 'bigcompany', 'fiber'], ['00-250059703', 1602230002L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250130308', 1602230005L, 'led', 'office', 'smallcompany', 'building_etc'], ['00-250130375', 1602230010L, 'led', 'factory', 'middlecompany', 'food'], ['00-250071057', 1602230021L, 'led', 'factory', 'middlecompany', 'food'], ['00-250071032', 1602230027L, 'led', 'apt', 'apt', 'none'], ['00-250071026', 1602230027L, 'led', 'apt', 'apt', 'none'], ['00-250059909', 1602230032L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250059812', 1602230034L, 'led', 'office', 'etc', 'school'], ['00-250071659', 1602230035L, 'led', 'office', 'smallcompany', 'building_etc'], ['00-250059912', 1602230036L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130333', 1602230040L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071086', 1602230043L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068185', 1602230047L, 'led', 'factory', 'smallcompany', 'wood'], ['00-250071072', 1602230048L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071167', 1602230048L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250130374', 1602230050L, 'led', 'apt', 'apt', 'none'], ['00-450083458', 1602230051L, 'led', 'office', 'bigcompany', 'building_etc'], ['00-450083404', 1602230051L, 'led', 'office', 'bigcompany', 'building_etc'], ['00-450083445', 1602230051L, 'led', 'office', 'bigcompany', 'building_etc'], ['00-450083403', 1602230051L, 'led', 'office', 'bigcompany', 'building_etc'], ['00-450083448', 1602230051L, 'led', 'office', 'bigcompany', 'building_etc'], ['00-250071667', 1602230052L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071700', 1602230052L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071104', 1602230055L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071109', 1602230055L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250130373', 1602230058L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130372', 1602230058L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-450083559', 1602230059L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450086595', 1602230060L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450086594', 1602230062L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000364', 1602230063L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000263', 1602230065L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000347', 1602230065L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450086593', 1602230066L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450086534', 1602230067L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083489', 1602230070L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083492', 1602230073L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083431', 1602230074L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083472', 1602230078L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083490', 1602230079L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000476', 1602230081L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000379', 1602230083L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000369', 1602230084L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083491', 1602230085L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000293', 1602230086L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-450083430', 1602230089L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000485', 1602230091L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-451000392', 1602230093L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250130309', 1602230097L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250130343', 1602230098L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250059996', 1602230103L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250071088', 1602230105L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250071168', 1602230105L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250068173', 1602230106L, 'led', 'factory', 'smallcompany', 'ceramic'], ['00-250059818', 1602230107L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250059751', 1602230111L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250060002', 1602240001L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250059849', 1602240003L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250059998', 1602240004L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071509', 1602240005L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250130315', 1602240005L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250130318', 1602240005L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250071151', 1602240006L, 'led', 'factory', 'smallcompany', 'food'], ['00-250068171', 1602240011L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130378', 1602240012L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130384', 1602240013L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068164', 1602240016L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250068193', 1602240018L, 'led', 'apt', 'apt', 'none'], ['00-450083564', 1602240023L, 'led', 'office', 'bigcompany', 'departmentStore'], ['00-450083562', 1602240023L, 'led', 'office', 'bigcompany', 'departmentStore'], ['00-450083563', 1602240023L, 'led', 'office', 'bigcompany', 'departmentStore'], ['00-250059706', 1602240026L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059775', 1602240028L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-460000184', 1602240035L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250059925', 1602240037L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250071481', 1602240039L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071550', 1602240039L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059813', 1602240040L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250070992', 1602240044L, 'led', 'factory', 'smallcompany', 'wood'], ['00-250059803', 1602240047L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250068139', 1602240054L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068198', 1602240054L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071186', 1602240055L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068144', 1602240059L, 'led', 'factory', 'smallcompany', 'wood'], ['00-250059765', 1602240061L, 'led', 'factory', 'bigcompany', 'ceramic'], ['00-250059836', 1602240061L, 'led', 'factory', 'bigcompany', 'ceramic'], ['00-250071681', 1602240072L, 'led', 'factory', 'smallcompany', 'wood'], ['00-250068192', 1602240074L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250060022', 1602240075L, 'led', 'factory', 'smallcompany', 'wood'], ['00-250068202', 1602240076L, 'led', 'factory', 'smallcompany', 'wood'], ['00-250068215', 1602240076L, 'led', 'factory', 'smallcompany', 'wood'], ['00-250071624', 1602240081L, 'led', 'factory', 'smallcompany', 'wood'], ['00-250059956', 1602240084L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-450083463', 1602240085L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059997', 1602240086L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250059999', 1602240087L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071557', 1602250002L, 'led', 'apt', 'apt', 'none'], ['00-250071540', 1602250002L, 'led', 'apt', 'apt', 'none'], ['00-250130324', 1602250002L, 'led', 'apt', 'apt', 'none'], ['00-250071493', 1602250002L, 'led', 'apt', 'apt', 'none'], ['00-250068218', 1602250004L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130336', 1602250006L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130361', 1602250007L, 'led', 'factory', 'middlecompany', 'metal'], ['00-250130363', 1602250007L, 'led', 'factory', 'middlecompany', 'metal'], ['00-250130367', 1602250007L, 'led', 'factory', 'middlecompany', 'metal'], ['00-250130362', 1602250007L, 'led', 'factory', 'middlecompany', 'metal'], ['00-250130312', 1602250014L, 'led', 'office', 'etc', 'building_etc'], ['00-250130313', 1602250014L, 'led', 'office', 'etc', 'building_etc'], ['00-250130370', 1602250015L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-360000177', 1602250017L, 'led', 'factory', 'bigcompany', 'fiber'], ['00-250130365', 1602250018L, 'led', 'apt', 'apt', 'none'], ['00-250059754', 1602250019L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071694', 1602250019L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250059705', 1602250022L, 'led', 'factory', 'smallcompany', 'metal'], ['00-251000081', 1602250024L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250130327', 1602250025L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071467', 1602250026L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130339', 1602250027L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130380', 1602250028L, 'led', 'factory', 'middlecompany', 'food'], ['00-250130344', 1602250029L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071438', 1602250032L, 'heungwanglamp', 'office', 'bigcompany', 'departmentStore'], ['00-250102801', 1602250039L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250102797', 1602250039L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250102794', 1602250039L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-450083429', 1602250043L, 'led', 'office', 'bigcompany', 'building_etc'], ['00-251004421', 1602250044L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250102795', 1602250047L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250102798', 1602250047L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250102800', 1602250047L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130342', 1602250049L, 'led', 'mart', 'bigcompany', 'departmentStore'], ['00-250102710', 1602250052L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071647', 1602250055L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130335', 1602250062L, 'led', 'etc', 'etc', 'none'], ['00-250059992', 1602250063L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071612', 1602250066L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-360000218', 1602250068L, 'led', 'factory', 'bigcompany', 'fiber'], ['00-450086512', 1602250069L, 'led', 'etc', 'bigcompany', 'none'], ['00-250071495', 1602250070L, 'led', 'factory', 'smallcompany', 'wood'], ['00-250059861', 1602250071L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250130345', 1602250076L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130340', 1602250079L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250102620', 1602250092L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250059874', 1602250112L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250102696', 1602250123L, 'led', 'apt', 'apt', 'none'], ['00-250130314', 1602250126L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130320', 1602250127L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130317', 1602250129L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071677', 1602250130L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130310', 1602250132L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130321', 1602250135L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250068224', 1602250140L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071432', 1602250153L, 'led', 'office', 'bigcompany', 'sangyong'], ['00-250130379', 1602250154L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250059819', 1602250156L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068165', 1602250160L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071090', 1602250164L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130329', 1602250165L, 'led', 'apt', 'apt', 'none'], ['00-250071061', 1602250166L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071068', 1602250166L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071066', 1602250167L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250071581', 1602250171L, 'led', 'apt', 'apt', 'none'], ['00-250068146', 1602250173L, 'led', 'office', 'etc', 'school'], ['00-250068148', 1602250173L, 'led', 'office', 'etc', 'school'], ['00-250059839', 1602250176L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250059965', 1602250177L, 'led', 'mart', 'bigcompany', 'sangyong'], ['00-250130306', 1602250184L, 'led', 'apt', 'apt', 'none'], ['00-250130326', 1602250184L, 'led', 'apt', 'apt', 'none'], ['00-360000016', 1602250186L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-451000482', 1602250186L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250007125', 1602260015L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059858', 1602260017L, 'led', 'office', 'smallcompany', 'building_etc'], ['00-250130307', 1602260018L, 'led', 'mart', 'etc', 'sangyong'], ['00-250070994', 1602260026L, 'heungwanglamp', 'factory', 'smallcompany', 'metal'], ['00-250059719', 1602260027L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250059915', 1602260028L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250068166', 1602260029L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250071085', 1602260035L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071039', 1602260035L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071096', 1602260035L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071025', 1602260039L, 'led', 'office', 'apt', 'building_etc'], ['00-250071087', 1602260039L, 'led', 'office', 'apt', 'building_etc'], ['00-250130381', 1602260041L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250130377', 1602260043L, 'led', 'etc', 'bigcompany', 'none'], ['00-250130376', 1602260043L, 'led', 'etc', 'bigcompany', 'none'], ['00-250071451', 1602260045L, 'heungwanglamp', 'factory', 'middlecompany', 'industryEtc'], ['00-250059852', 1602260049L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250102648', 1602260051L, 'led', 'factory', 'bigcompany', 'wood'], ['00-250059853', 1602260052L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071028', 1602260058L, 'led', 'apt', 'apt', 'none'], ['00-250071632', 1602260059L, 'led', 'office', 'smallcompany', 'building_etc'], ['00-250059774', 1602260059L, 'led', 'office', 'smallcompany', 'building_etc'], ['00-250130356', 1602260064L, 'led', 'factory', 'middlecompany', 'metal'], ['00-250130358', 1602260064L, 'led', 'factory', 'middlecompany', 'metal'], ['00-250130355', 1602260064L, 'led', 'factory', 'middlecompany', 'metal'], ['00-250130359', 1602260064L, 'led', 'factory', 'middlecompany', 'metal'], ['00-250130357', 1602260064L, 'led', 'factory', 'middlecompany', 'metal'], ['00-250068210', 1602260065L, 'led', 'factory', 'bigcompany', 'food'], ['00-250068197', 1602260065L, 'led', 'factory', 'bigcompany', 'food'], ['00-250071465', 1602260068L, 'led', 'office', 'etc', 'hospital'], ['00-250130369', 1602260072L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071679', 1602260077L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071185', 1602260081L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071189', 1602260081L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071312', 1602260084L, 'led', 'factory', 'bigcompany', 'ceramic'], ['00-250071310', 1602260084L, 'led', 'factory', 'bigcompany', 'ceramic'], ['00-250071311', 1602260084L, 'led', 'factory', 'bigcompany', 'ceramic'], ['00-250071336', 1602260084L, 'led', 'factory', 'bigcompany', 'ceramic'], ['00-251004064', 1602260085L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-251009025', 1602260085L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071122', 1602260086L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071126', 1602260086L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071144', 1602260086L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-360000216', 1602260088L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250130383', 1602260091L, 'led', 'office', 'bigcompany', 'sangyong'], ['00-250059856', 1602260094L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071414', 1602260095L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071464', 1602260096L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071121', 1602260097L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250071004', 1602260097L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250071138', 1602260098L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071140', 1602260098L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-251009632', 1602260101L, 'led', 'factory', 'bigcompany', 'industryEtc'], ['00-250071625', 1602260104L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250102644', 1602260112L, 'led', 'office', 'smallcompany', 'building_etc'], ['00-250102649', 1602260112L, 'led', 'office', 'smallcompany', 'building_etc'], ['00-250071172', 1602260115L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-250071188', 1602260115L, 'led', 'factory', 'middlecompany', 'industryEtc'], ['00-360000075', 1602260118L, 'led', 'office', 'smallcompany', 'building_etc'], ['00-250059724', 1602260119L, 'led', 'office', 'bigcompany', 'building_etc'], ['00-250071319', 1602260120L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071368', 1602260120L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071549', 1602260126L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071370', 1602260128L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250071371', 1602260128L, 'led', 'factory', 'smallcompany', 'metal'], ['00-250059770', 1602260130L, 'led', 'office', 'bigcompany', 'building_etc'], ['00-250071387', 1602260133L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250059784', 1602260140L, 'led', 'factory', 'middlecompany', 'wood'], ['00-250059982', 1602260140L, 'led', 'factory', 'middlecompany', 'wood'], ['00-250130331', 1602260142L, 'led', 'apt', 'apt', 'none'], ['00-250130338', 1602260146L, 'led', 'apt', 'apt', 'none'], ['00-250071696', 1602260148L, 'led', 'apt', 'apt', 'none'], ['00-250059814', 1602260149L, 'led', 'apt', 'apt', 'none'], ['00-250059947', 1602260150L, 'led', 'apt', 'apt', 'none'], ['00-250130323', 1602260153L, 'led', 'apt', 'apt', 'none'], ['00-250059854', 1602260161L, 'led', 'apt', 'apt', 'none'], ['00-250071181', 1602260164L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071182', 1602260164L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071005', 1602260166L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071290', 1602260167L, 'led', 'factory', 'smallcompany', 'industryEtc'], ['00-250071175', 1602260170L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-250071191', 1602260170L, 'led', 'factory', 'smallcompany', 'fiber'], ['00-250068232', 1602260171L, 'led', 'factory', 'smallcompany', 'metal']]

        toendpoint = len(led_id)

        for i in range (toendpoint):

            tagdata=led_id[i]
            mds_id=led_id[i][0]
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
