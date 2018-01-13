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
import inverterinfotest

url = "http://125.140.110.217:4242/api/put"
#url = "http://49.254.13.34:4242/api/put"
response ={}

con = cx_Oracle.connect('keti_user/keti1357!#@125.141.144.149/aimir')
cur = con.cursor()

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



# update 15 minutes, TSDB
def updateMINONE(in_sttime, in_entime,in_mdsid,tagdata):

    starttime = in_sttime   # 기간 시작
    endtime = in_entime     # 기간 종료
    mdsid = in_mdsid        # 스마트미터 아이디

    sql_tmp = "select ELE.LP_TIME, ELE.VALUE_00, ELE.VALUE_15, ELE.VALUE_30, ELE.VALUE_45, ECU.NAME, ECO.LOCATION, ECO.SIC, ELE.MDS_ID, ELE.DEVICE_SERIAL, ECU.CUSTOMERNO, ELE.CHANNEL from EMNV_LP_EM_VIEW  ELE join EMNV_CONTRACT_VIEW ECO on ELE.MDS_ID = ECO.MDS_ID join EMNV_CUSTOMER_VIEW ECU on ECO.CUSTOMERNO = ECU.CUSTOMERNO where (ELE.CHANNEL=1) and (ELE.LP_TIME between '%s' and '%s') and (ELE.MDS_ID='%s') order by ELE.MDS_ID ASC, ELE.LP_TIME ASC" %(starttime, endtime, mdsid)
    minlist = ['00', '15', '30', '45']
    timedic = {0:0.0, 1:0.0, 2:0.0, 3:0.0, 4:0.0} #시간 확인 ?
    lcfm = len(minlist) # 15분 단위 데이터 처리

    day = {} # 측정값 저장
    cur.execute(sql_tmp)

    pout = " sql 실행, 원격서버 Oracle 에서 데이터 수집 "
    sys.stdout.write(pout)
    sys.stdout.flush()

    ix = 0
    count=0
    donecheck=0
    cccc=0
    donecheck = 0

    for result in cur:
        donecheck = donecheck + 1
        result = list(result)   # result, 서버 Oracle DB에서 수집한 데이터

        #print result
        # 또는
        #pout = str(result)
        #sys.stdout.write(pout)
        #sys.stdout.flush()

        for ii in [1,2,3,4]:    # 15분단위 확인해서, 데이터 없으면 0 입력
            if str(result[ii]) == 'None':
                result[ii] = 0.0
        cccc=1

        #날짜 밀림 확인 필요!!
        try:
            day[result[0][0:8]]

        except:
            day[result[0][0:8]] = [0.0, 0.0, 0.0, 0.0, 0.0]

        if count % 24 < 9:
            day[result[0][0:8]][0]=day[result[0][0:8]][0]+result[1]+result[2]+result[3]+result[4]

        elif count % 24 < 12:
            day[result[0][0:8]][1]=day[result[0][0:8]][1]+result[1]+result[2]+result[3]+result[4]

        elif count % 24 <13:
            day[result[0][0:8]][2]=day[result[0][0:8]][2]+result[1]+result[2]+result[3]+result[4]

        elif count % 24 < 18:
            day[result[0][0:8]][3]=day[result[0][0:8]][3]+result[1]+result[2]+result[3]+result[4]

        else :
            day[result[0][0:8]][4]=day[result[0][0:8]][4]+result[1]+result[2]+result[3]+result[4]

        count = count+1
            #print result[0] #1단계

    nuzukdic = {}

    donecount = 0
    if donecheck == 0:
        print "데이터 없음!"
        return donecheck

    for a,v in day.items(): # 24시간 구간설정, 평균
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

            htag = 1
            if(datetime.date(int(a[0:4]),int(a[4:6]),int(a[6:8])).weekday() < 5 ):
                htag=0 # holiday
            if value!=0:
                nuzukdic[hour] = (value + nuzukdic[hour]) / 2.0
                #else:
                    #value=0.0

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
                    "pan_pump":tagdata[3],
                    "customer_id": tagdata[4],
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
                    "pan_pump": tagdata[3],
                    "customer_id": tagdata[4],
                }
                }

            #ret = requests.post(url, data=json.dumps(data))
            #ret = requests.post(url, data=json.dumps(nuzuk_data))

        if cccc == 1:
            print "done sum"

    return donecheck


def go():
        # 2017-5-29 기준
        # 2016년 11월 1일 부터 2017년 2월 28일까지:완료
        # 2017-5-30 기준
        # 2017년 02월 1일 부터 2017년 5월 29일까지
        # 2016년 09월 1일 부터 2016년 11월 1일까지
        sttime = "2017050100"
        entime = "2017050500"

        resultfile=open("log_inverter_kang.txt","a")
        ix=1
        tagdata = ['aa','aa','aa','aa','aa']

        # 인버터의 입력 리스트 파일에는 두부분으로 나누어져 있음
        # inverterinfotest.inverter1 은 40개 보다 작음
        # inverterinfotest.inverter2 는 300개 넘음
        # 이곳을 수정하면 for 루프안에도 inverterinfotest.inverter2 변경 필요
        toendpoint = len(inverterinfotest.inverter)

        for i in range (toendpoint):
            # 미터 아이디
            tagdata[0] = (inverterinfotest.inverter[i][0])
            mds_id = tagdata[0]
            # LED,INVERTER, 형광등, 백열등, 메탈라이드
            tagdata[1] = (inverterinfotest.inverter[i][1])
            # factory, mart, apt, office
            tagdata[2] = (inverterinfotest.inverter[i][2])
            # fan, pump, compressor, blower
            tagdata[3] = (inverterinfotest.inverter[i][3])
            # 등록번호(?)
            tagdata[4] = (inverterinfotest.inverter[i][4])

            print tagdata
            donecheck = updateMINONE(sttime, entime, mds_id, tagdata)
            print donecheck

            resultfile.write(str(mds_id)+","+str(donecheck)+"\n")
            resultfile.flush()

            pout = "ix: %s, mdsid: %s 전체 진행률: %s 퍼센트 진행!" %(ix, mds_id,int(float((ix)/593.0)*100))
            sys.stdout.write(pout)
            sys.stdout.flush()

            # 화면에 메세지 출력할때,
            # 줄이 바뀌지 않고. 한줄에만 덮혀서 출력함

            # pout = "ix: %s, mdsid: %s, donecheck: %d \r" %(ix, mds_id, donecheck)
            # sys.stdout.write(pout)
            # sys.stdout.flush()

            ix=ix+1
            time.sleep(0.001)

        cur.close()
        con.close()


# main function
if __name__ == "__main__":
    print "GO ..."
    #print (datetime.date(2017,06,1).weekday())    # if  > 4 : 주말
    #week = ('Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')
    #print (week[datetime.date(2017,05,30).weekday()])

    go()
    exit('... exiting')
