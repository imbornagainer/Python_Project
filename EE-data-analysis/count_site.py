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
import ledinfotest


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
    #pout = " sql 실행, 원격서버 Oracle 에서 데이터 수집 "
    #sys.stdout.write(pout)
    #sys.stdout.flush()

    ix = 0
    count=0
    donecount = 0
    cccc=0
    donecheck = 0

    for result in cur:
        donecheck = donecheck + 1
        return 1

    if donecheck == 0:
        return donecheck # 데이터가 없으면 donechek = 0 으로 리턴

    return donecheck


def go():

        print "workding..."
        volubility = len(sys.argv)
        _t_string_ = " ".join(sys.argv)
        _t_type_ = "led"

        if volubility > 1:
            _t_string = sys.argv[1]
            if (_t_string_.find("led") > -1 ) :
                _t_type_ = "led"
                print "  sys.argv[%d], type = LED" %(1)
            elif (_t_string_.find("inverter") > -1 ) :
                _t_type_ = "inverter"
                print "  sys.argv[%d], type = INVERTER" %(1) ,
        else :
            print (" no input # starting with init variables ....  ")

        _t_re_fname = "log_result_" + _t_type_ + ".txt"
        _t_er_fname = "log_nodata_" + _t_type_ + ".txt"

        # 2017-5-29 기준
        # 2016년 11월 1일 부터 2017년 2월 28일까지:완료
        # 2017-5-30 기준
        # 2017년 02월 1일 부터 2017년 5월 29일까지
        # 2016년 09월 1일 부터 2016년 11월 1일까지
        sttime = "2016110100"
        entime = "2017050500"

        resultfile=open(_t_re_fname,"a")
        nodata_id_file = open(_t_er_fname,"a")

        pout = ("check date " + sttime + " ~ " + entime +"\n" )
        pout = pout + "start time -> "+ str(datetime.datetime.now())
        print pout
        resultfile.write(pout)
        resultfile.flush()

        nodata_cnt = 0
        ix = 1
        tagdata = ['aa','aa','aa','aa','aa']

        # 입력 리스트 파일, LED, 인버터 ID 리스트
        # inverterinfotest.inverter LIST
        # ledinfotest.led LIST
        if (_t_type_ == 'inverter'):
            _input_ = inverterinfotest.inverter
        elif (_t_type_ == 'led'):
            _input_ = ledinfotest.led

        toendpoint = len(_input_)
        print "  Total = %d" %(toendpoint)
        assert (type(_input_) is list) # 입력데이터 형태가 LIST인지 확인

        for i in range (toendpoint):
            # 미터 아이디
            tagdata[0] = (ledinfotest.led[i][0])
            mds_id = tagdata[0]
            # LED,INVERTER, 형광등, 백열등, 메탈라이드
            tagdata[1] = (ledinfotest.led[i][1])
            # factory, mart, apt, office
            tagdata[2] = (ledinfotest.led[i][2])
            # fan, pump, compressor, blower
            tagdata[3] = (ledinfotest.led[i][3])
            # 등록번호(?)
            #tagdata[4] = (ledinfotest.led[i][4])

            donecheck = updateMINONE(sttime, entime, mds_id, tagdata)

            if donecheck == 0 :
                nodata_cnt = nodata_cnt + 1
                pout = str(nodata_cnt) + ', '+ str(mds_id)
                print pout + " "*80
                pout = pout + '\n'
                nodata_id_file.write(pout)
                nodata_id_file.flush()

            pout = str(mds_id)+", nodata_cnt = "+ str(nodata_cnt) + " / " + str(ix) + "      " "\r"
            sys.stdout.write(pout)
            sys.stdout.flush()
            resultfile.write(pout)
            resultfile.flush()

            # 화면에 메세지 출력할때,
            # 줄이 바뀌지 않고. 한줄에만 덮혀서 출력함

            # pout = "ix: %s, mdsid: %s, donecheck: %d \r" %(ix, mds_id, donecheck)
            # sys.stdout.write(pout)
            # sys.stdout.flush()

            ix = ix + 1
            time.sleep(0.3)

        cur.close()
        con.close()

        pout = "\n finish time -> "+ str(datetime.datetime.now())
        print pout
        resultfile.write(pout)
        resultfile.flush()

# main function
if __name__ == "__main__":
    print "GO ..."
    #print (datetime.date(2017,06,1).weekday())    # if  > 4 : 주말
    #week = ('Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')
    #print (week[datetime.date(2017,05,30).weekday()])

    go()

    exit('... exiting')
