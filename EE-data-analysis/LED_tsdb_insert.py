# -*- coding: utf-8 -*-
# Author : eunsooLim , https://github.com/eunsooLim
# Author : jeonghoonkang , https://github.com/jeonghoonkang

#LED_tsdb_insert.py
#SQL 내의 LED 사이트에 대한 가동률, 누적가동률을 계산하여 TSDB에 삽입

import time
import datetime
import cx_Oracle
import os
import sys
import requests
import json
import time, datetime
import ledinfotest

url = "http://125.140.110.217:4242/api/put"
#url = "http://49.254.13.34:4242/api/put"
response ={}

con = cx_Oracle.connect('keti_user/keti1357!#@125.141.144.149/aimir')
cur = con.cursor()

timezone=[('00','09'),('09','12'),('12','13'),('13','18'),('18','23')]


'''
	### 함수 : timeTOunixtime ### 
	시간 문자열을 유닉스 시간 문자열로 변환  
	parameter (rlt) : 시간 문자열
	return : 유닉스 시간 문자열  
'''

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


'''
	### 함수 : updateMINONE ### 
	해당 사이트에 대한 해당 기간의 전력 데이터를 TSDB로부터 가져와 시간대별 평균가동률, 누적가동률을 계산, 데이터들을 TSDB에저장  
  	parameter1 (in_sttime) : 기간의 시작 시간(YYYYMMDDHH)
	parameter2 (in_entime) : 기간의 종료 시간(YYYYMMDDHH)
	parameter3 (in_mdsid) : 사이트의 검침기 아이디
	parameter4 (tagdata) : 해당 사이트에 대한 테그 데이터
	return (donecheck) : 누리텔레콤에서 가져온 데이터의 열(colunm) 수 
'''
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
	
	#1시간 간격의 각 데이터 행(row)에 대해 반복 
        for result in cur:
            donecheck=donecheck+1
            result=list(result)
		
            for ii in [1,2,3,4]:
                if str(result[ii]) == 'None':
                    result[ii] = 0.0
            cccc=1
	
            try:
                day[result[0][0:8]]
            except:
                day[result[0][0:8]]=[0.0,0.0,0.0,0.0,0.0]

		
		 # 0-8/9-11/12/13-17/18-23시 간격으로 분리,  각 간격의 데이터 총합 계산 
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
        nuzukdic={}

	#데이터가 없을 경우 리턴 
        donecount=0
        if donecheck == 0:
            print "데이터 없음!"
            return donecheck

        print "\n넣는중........\n"
	
	#각 시간 간격의 평균
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


		# 평균, 누적평균 데이터를 TSDB에 삽입 : 24개 / 1일 (한 시간 간격)
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

		#토, 일요일을 제외하고 데이터를 누적
                htag = 0
                if (week[datetime.date(int(a[0:4]), int(a[4:6]), int(a[6:8])).weekday()] == 'Sun'):
                    htag = 1

                elif (week[datetime.date(int(a[0:4]), int(a[4:6]), int(a[6:8])).weekday()] == 'Sat'):
                    htag = 1

                else:  # 평일일 경우!!
                    if value != 0:#누적진행
                        nuzukdic[hour] = (value + nuzukdic[hour]) / 2.0

                data = {
                    "metric": "test_daily_led",
                    "timestamp": uxtime,
                    "value": value,
                    "tags": {
                        "MDS_ID": result[8],
                        "Device_Serial": result[9],
                        "holiday" : htag,
                        "led_inverter" : tagdata[1],
                        "factory_mart" : tagdata[2],
                        "customer_id": tagdata[3]
                    }
                }

                nuzuk_data = {
                    "metric": "test_nuzuk_led",
                    "timestamp": uxtime,
                    "value": nuzukdic[hour],
                    "tags": {
                        "MDS_ID": result[8],
                        "Device_Serial": result[9],
                        "holiday": htag,
                        "led_inverter" : tagdata[1],
                        "factory_mart" : tagdata[2],
                        "customer_id": tagdata[3]
                    }
                    }

                ret=requests.post(url, data=json.dumps(data))
                ret =requests.post(url, data=json.dumps(nuzuk_data))

                """if(int((float(donecount)*100/float(donecheck)))%10==0 and hour==23): #led 하나의 진행사항 체크
                     print "***" + str(int((float(donecount)/float(donecheck))*10000)) +"% 진행중...  ***"
                     if(float(donecount)/float(donecheck))*10000 > 99 :
                         print "조금만 기다려 주세요."""""


        return donecheck


# main function
if __name__ == "__main__":

        # 2017-5-29 기준
        # 2016년 11월 1일 부터 2017년 2월 28일까지:완료
        # 2017-5-30 기준
        # 2017년 02월 1일 부터 2017년 5월 29일까지
        # 2016년 09월 1일 부터 2016년 11월 1일까지
        # 2017-05-31  기준
	# 2016년 11월 1일  부터 2016년  12월 31 까지 휴일추가
	sttime = "2016110100"
        entime = "2016123123"

        filename='LED_resultcsv'+sttime+"to"+entime+".txt"

        led_resultfile=open(filename,"w")
        ix=1
        tagdata = ['aa','aa','aa','aa']
        toendpoint = len(ledinfotest.led)

        for i in range (toendpoint):

            tagdata[0] = (ledinfotest.led[i][0])#mds_id ->MDSID를 이용해서 누리텔레콤오라클에서 데이터 추출
            mds_id = tagdata[0]

            tagdata[1] = (ledinfotest.led[i][1])  # led,형광등
            tagdata[2] = (ledinfotest.led[i][2])  # 마트,공장
            tagdata[3] = (ledinfotest.led[i][3])  # 아이디



            print tagdata
            donecheck = updateMINONE(sttime, entime, mds_id, tagdata)
            if donecheck>0:
                print "들어간 데이터 량"+ str(donecheck)
            led_resultfile.write(str(mds_id)+","+str(donecheck)+"\n")
            print "ix: %s, mdsid: %s 전체 진행률: %s 퍼센트 진행!" %(ix, mds_id,int(float((ix)/float(toendpoint))*100))
            led_resultfile.flush()
            # 화면에 메세지 출력할때,
            # 줄이 바뀌지 않고. 한줄에만 덮혀서 출력함

            # pout = "ix: %s, mdsid: %s, donecheck: %d \r" %(ix, mds_id, donecheck)
            # sys.stdout.write(pout)
            # sys.stdout.flush()

            ix=ix+1

        cur.close()
        con.close()
