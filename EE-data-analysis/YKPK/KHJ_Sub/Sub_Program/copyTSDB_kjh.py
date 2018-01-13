# -*- coding: utf-8 -*-
# Author : jeonghoonkang , https://github.com/jeonghoonkang


# openTSDB를 사용하기 위한 class 
# last modified by 20171031  

import time
import datetime
import os
import sys
import requests
import json
import argparse
import calendar
import urllib2
import socket
#import ledinfotest
from operator import itemgetter, attrgetter
#import xlsxwriter
#import re
import ast

#import _input_list_17_0906

#ltelist = _input_list_17_0906.valid_list
ltelist = [['01223187332'], ['01224230502'], ['01224272943'], ['01223187357'], ['01224273096'], ['01220800675'], ['01224230548'], ['01224273046'], ['01223239888'], ['01223299446'], ['01224273022'], ['01223239886'], ['01220800701'], ['01223299434'], ['01223187276'], ['01223187286'], ['01223180976'], ['01224230521'], ['01223180994'], ['01224230529'], ['01224230467'], ['01223192391'], ['01221343888'], ['01224230577'], ['01224230493'], ['01224230501'], ['01224230526'], ['01221386983'], ['01223239875'], ['01223239870'], ['01221251996'], ['01224230542'], ['01224230434'], ['01224230484'], ['01224230485'], ['01224230470'], ['01222699986'], ['01222742200'], ['01222739929'], ['01224230527'], ['01223187397'], ['01222764501'], ['01223239874'], ['01223187431'], ['01223187430'], ['01222674501'], ['01220684147'], ['01222694501'], ['01224230509'], ['01224230472'], ['01224230478'], ['01222746390'], ['01222779929'], ['01224230518'], ['01222754503'], ['01224230546'], ['01224224149'], ['01220800623'], ['01220435025'], ['01224230511'], ['01224230515'], ['01224230461'], ['01224230533'], ['01224230451'], ['01223192386'], ['01224230446'], ['01224230532'], ['01222764503'], ['01222586543'], ['01222684504'], ['01222684501'], ['01224230479'], ['01223187386'], ['01222647452'], ['01222746383'], ['01224230436'], ['01222758870'], ['01221474412'], ['01221474414'], ['01222779987'], ['01222664501'], ['01221566963'], ['01221574336'], ['01224230433'], ['01224230525'], ['01224230439'], ['01224230449'], ['01220800592'], ['01224230457'], ['01222746381'], ['01223192263'], ['01224230491'], ['01221421994'], ['01221441994'], ['01222749929'], ['01224230551'], ['01224230473'], ['01223239872'], ['01224230488'], ['01224230513'], ['01224230482'], ['01224230507'], ['01224230517'], ['01224230490'], ['01222704501'], ['01222754501'], ['01222709929'], ['01224230528'], ['01222683542'], ['01221448178'], ['01223192284'], ['01222759929'], ['01221243882'], ['01221361991'], ['01221474413'], ['01222654501'], ['01222799985'], ['01221253884'], ['01220800593'], ['01224230460'], ['01224230565'], ['01224230465'], ['01224230476'], ['01221574346'], ['01221567020'], ['01221566961'], ['01221566960'], ['01221566971'], ['01223187435'], ['01221574354'], ['01223188887'], ['01221574324'], ['01222636543'], ['01222745943'], ['01224230564'], ['01224230541'], ['01224230539'], ['01224230534'], ['01222746397'], ['01224230435'], ['01224230487'], ['01224230489'], ['01224230504'], ['01224230486'], ['01224230469'], ['01224230510'], ['01224230443'], ['01222796541'], ['01224230512'], ['01222744501'], ['01224230437'], ['01222724501'], ['01221283886'], ['01222745934'], ['01222745495'], ['01224230516'], ['01224230500'], ['01221474387'], ['01221431994'], ['01221261996'], ['01223187402'], ['01223187398'], ['01223187384'], ['01221471994'], ['01221474403'], ['01221474402'], ['01221474406'], ['01221474407'], ['01221243887'], ['01224230464'], ['01223192393'], ['01223192394'], ['01224230458'], ['01224230459'], ['01223187394'], ['01221474404'], ['01221474405'], ['01222789986'], ['01220674130'], ['01220674064'], ['01220674076'], ['01220674061'], ['01220800602'], ['01220800591'], ['01220674093'], ['01220674088'], ['01220800573'], ['01221474395'], ['01220800684'], ['01220674121'], ['01220674078'], ['01220674112'], ['01220674094'], ['01221474399'], ['01220674085'], ['01221474389'], ['01220674157'], ['01221429374'], ['01221446671'], ['01221401991'], ['01220800716'], ['01220674084'], ['01220800763'], ['01221431991'], ['01220674095'], ['01220800669'], ['01220435093'], ['01221241996'], ['01221391991'], ['01221381991'], ['01223192096'], ['01223299440'], ['01223219093'], ['01224273017'], ['01223180993'], ['01223219115'], ['01223219114'], ['01224273087'], ['01224273045'], ['01224230559'], ['01223219089'], ['01224273026'], ['01224273079'], ['01224272971'], ['01222746396'], ['01222746350'], ['01224230549'], ['01224224135'], ['01224272966'], ['01222729929'], ['01222746456'], ['01222742834'], ['01223219130'], ['01223192247'], ['01222745462'], ['01221574357'], ['01222754504'], ['01222674503'], ['01224230531'], ['01224230569'], ['01222742878'], ['01222746463'], ['01222704503'], ['01222745939'], ['01222734501'], ['01222769929'], ['01221574356'], ['01222745510'], ['01222719929'], ['01221574359'], ['01222746366'], ['01223239865'], ['01223219128'], ['01222742885'], ['01222745938'], ['01222724503'], ['01222704504'], ['01222742752'], ['01222694503'], ['01223209883'], ['01223209884'], ['01223192283'], ['01222654504'], ['01222714503'], ['01222699984'], ['01221731209'], ['01224230558'], ['01224230495'], ['01221388812'], ['01221388441'], ['01224273086'], ['01221566970'], ['01223209872'], ['01222714504'], ['01222664504'], ['01222742757'], ['01222744504'], ['01224230496'], ['01222689984'], ['01224230506'], ['01224230477'], ['01224273073'], ['01223219050'], ['01224230530'], ['01224273039'], ['01224273091'], ['01224230570'], ['01224272955'], ['01224230483'], ['01223239867'], ['01222798870'], ['01222748870'], ['01222664503'], ['01222654503'], ['01222674504'], ['01222746482'], ['01222744503'], ['01221273883'], ['01222746459'], ['01222684503'], ['01221388068'], ['01221567011'], ['01222742946'], ['01222659984'], ['01222744780'], ['01222745479'], ['01223209889'], ['01223209891'], ['01222742798'], ['01222746421'], ['01223209890'], ['01222745859'], ['01221351991'], ['01223239871'], ['01223187403'], ['01223187406'], ['01223192453'], ['01222746380'], ['01222794503'], ['01223187387'], ['01221390254'], ['01223299436'], ['01223219047'], ['01223299431'], ['01222714543'], ['01223239869'], ['01224230576'], ['01223188269'], ['01222742956'], ['01222745635'], ['01222745363'], ['01222742927'], ['01222742916'], ['01224272937'], ['01222742949'], ['01221391199'], ['01221391155'], ['01222618542'], ['01222742704'], ['01222742908'], ['01223209868'], ['01223299443'], ['01223299439'], ['01223209866'], ['01224273085'], ['01223180968'], ['01223209864'], ['01223209863'], ['01224272988'], ['01223299442'], ['01224272962'], ['01223187419'], ['01223188270'], ['01222744754'], ['01222587543'], ['01221291991'], ['01222567452'], ['01222577452'], ['01222688541'], ['01222769542'], ['01221463494'], ['01221474401']]
# OpenTSDB 클래스
# EE db 는 15분 단위의 데이터를 저장하고 있음
# OpenTSDB read, and write
class u_ee_tsdb :

    __cin_stime = None #시작시간
    __cin_etime = None #종료시간
    __cin_url = None
    __cin_recent = None
    __cin_datelist = []
    __cin_metric_name = None

    # 시간은 string type 예) 20160701
    def __init__(self, __url, __st = None, __et = None, __r = None, __outmetric = None) :
       self._url(__url)
       if __st != None and __et != None and __r != None : exit (" < Input Error > no time info")
       elif __st != None and __et != None : 
           self._set_time_period(__st, __et)
           self.__cin_datelist = self.makeDateList()
       elif __st != None : self._set_time_period(__st)
       elif __r != None : self.__cin_recent = True
       elif self.__cin_recent != True : self.__cin_datelist = self.makeDateList()

    def _url(self, __url):
        self.__cin_url = __url
        if __url == None :
            # default for test
            self.__cin_url = None

    def _set_time_period(self, __st, __et = None) : 
    # TSDB는 기본적으로 시작/종료 시간필요
    # 최소한 시작 시간 필요함
    # 시간 형식을 스트링으로 정리할 뿐... 다른 작업은 안함 

        if __et == None :
            _lst = len(__st)
            if _lst < 8 : exit ("... too short data length")
            if _lst < 10 : __st = __st[:8] + '00'
            # 여기까지 진행한 날짜는 2017072912 이런식이라고 가정함.
            self.__cin_stime = __st
            self.__cin_etime = __et
            return

        _lst = len(__st)
        _let = len(__et)

        if _lst < 8 or _let < 8 : exit ("... too short data length")
        if _lst < 10 : __st = __st[:8] + '00'
        if _let < 10 : __et = __et[:8] + '00'
        if __st[:8] > __et[:8] : exit ("... Check start, end date")

        self.__cin_stime = __st
        self.__cin_etime = __et


    def set_metric(self,__m) : #TSDB는 metric 이름을 기준으로 읽고/저장
        self.__cin_metric_name = __m

    def changeTimeForOnePointReading(self, _start):
        _st = self.__cin_stime
        assert(self.__cin_etime == None)
        #print ("change self.__cin_etime = self.__cin_stime+ 1 hour")
        # 날짜는 2017072912 이런식이라고 가정함.
        # datetime.date object
        _tmp_obj = datetime.datetime.strptime(_st[:-2],"%Y%m%d").date()
        _tt = _st[-2:] + '00' + '00'
        _time_obj = datetime.datetime.strptime(_tt, "%H%M%S").time()
        _tmp_obj = datetime.datetime.combine(_tmp_obj, _time_obj)
        _delta_obj = datetime.timedelta(hours = 1)
        # datetime.datetime object
        _tmp_obj = _tmp_obj + _delta_obj
        _tmp = _tmp_obj.strftime('%Y%m%d%H')
        self.__cin_etime = _tmp 
        print _tmp
        assert(self.__cin_stime < self.__cin_etime )
        return _tmp

    ''' 
    함수 : readTSDB
    특정 시간의 TSDB값 반환
    parameter1 (in_st) : 시작 시각
    parameter2 (in_et) : 종료 시각
    parameter3 (mid) : 미터기 아이디
    반환 (packetlist_filter) : database 값 리스트(list) 
    '''

    def read_otsdb(self, __in_st, __in_et, __mid):
        packetlist = []  # split :
        packetlist_filter = []  # integer

        # YYYY/MM/DD-HH:00:00
        start = "%s/%s/%s-%s:00:00" % (__in_st[0:4], __in_st[4:6], __in_st[6:8], __in_st[8:10])
        end = "%s/%s/%s-%s:00:00" % (__in_et[0:4], __in_et[4:6], __in_et[6:8], __in_et[8:10])
        tsdb_url = t_url + start + "&end=" + end + "&m=avg:test_daily_led" + "{MDS_ID=" + str(mid) + "}"

        tsdbdata = urllib2.urlopen(url_tsdb)
        read_query = tsdbdata.read()

        print read_query
        exit(-1)
        # 이부분은 사용하지 않음, ast 함수 사용

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
    ## 함수 : calDate
    특정 시간 사이에 날짜들을 연월일시간(YYMMDDhh)을 반환
    open TSDB는 이런형식으로 날짜입력이 된다
    parameter1 (sttime) : 시작 시각
    parameter2 (ettime) : 종료 시각
    반환 (re_datelist) : 날짜 리스트
    '''
    
    def makeDateList(self):
        w_sttime = self.__cin_stime #start unixtime
        w_ettime = self.__cin_etime #end unixtime
        #make it to 23 hour for the last day, 2016110223
        #if w_ettime[-2:] != '23' : w_ettime = w_ettime[:-2] + '23'

        tmp_w_sttime = w_sttime[0:8]
        first_loop = 0
        re_datelist = []

        #print self.__cin_url, self.__cin_stime, self.__cin_etime

        while 1:
            #time.sleep(0.01)
            #print ("   ... Processing Date List ... ")

            if first_loop > 0: # 첫 루프가 아니면, 마지막 루프 (종료 또는 다음날로 진행)
                if w_ettime > self.__cin_etime:
                    # 마지막 이면 : 최초 입력 날짜/시간 보다 종료 시간이 늦으면 종료
                    break
                else:
                    w_sttime = self.nextDate(w_sttime, 'd') # 다음날짜 받아옴
                    tmp_w_sttime = w_sttime[0:8]  # ymd 형식

            w_ettime = tmp_w_sttime + '23' #마지막 23시 표시

            if w_ettime == self.__cin_etime: # 마지막 시간 부분 :
                first_loop = 1 # 다음부터는 첫 루프로 진행
                re_datelist.append([w_sttime, w_ettime])
                break

            else:  # start time != end time, 아직 앞부분
                # 동일한 year 처리
                if dateInt(self.__cin_etime, 'y') == dateInt(w_sttime, 'y'):
                    if dateInt(self.__cin_etime, 'm') > dateInt(w_sttime, 'm'):  
                        # different month
                        # check the last day of start month
                        w_st_calr=calendar.monthrange(int(w_sttime[0:4]),dateInt(w_sttime,'m'))
                        if dateInt(w_sttime, 'd') == w_st_calr[1]:  
                            # current day == the last day of stday
                            # next month
                            re_datelist.append([w_sttime, tmp_w_sttime + '23'])
                            w_sttime = self.nextDate(w_sttime, 'm')
                            first_loop = 1
                            continue
                else: # 시작과 종료가 다른 year
                    tmp_w_sttime = w_sttime[0:4]  # year
                    w_st_calr = calendar.monthrange(int(w_sttime[0:4]), dateInt(w_sttime, 'm'))
                    if dateInt(w_sttime, 'd') == w_st_calr[1]:  
                        # current day == the last day of stday
                        re_datelist.append([w_sttime, w_ettime])
                        if dateInt(w_sttime, 'm') == 12:  # 12 month
                            # next year
                            w_sttime = self.nextDate(w_sttime, 'y')
                            tmp_w_sttime = w_sttime[0:8]
                            first_loop = 1
                            continue
                        else:
                            # next month
                            w_sttime = self.nextDate(w_sttime, 'm')
                            tmp_w_sttime = w_sttime[0:8]
                            first_loop = 1
                            continue
                first_loop = 1
            re_datelist.append([w_sttime, w_ettime])
            # [['2016110100', '2016110123'], ['2016110200', '2016110223'],
        return re_datelist

    '''
    ## 함수 : nextDate
    다음 "연, 월, 일"을 계산, 2016년 12월 30일 이후 31일인지, 아니면 1월1일 인지
    parameter1 (in_time) : 문자형 date 값
    parameter2 (in_mdh) : 연, 월, 일, 시간의 분류 (y, m, d, h)
    반환 (re_mdh) : 계산 된 다음 날
    '''
    def nextDate(self, in_time, in_mdh):
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
    ## 함수 : get_tsdb_value
    데이터베이스에 데이터가 있는지 여부를 확인하고
    데이터가 있으면 측정 수치 수집
    주의 : 메트릭만으로 판단 (tag 까지는 확인 안함, 추후 tag 검색 추가 필요)
    반환 (empty_flag) : 비어있을 경우 1 / 비어있지 않을 경우 0
    '''
    def get_tsdb_value(self, _tag = None, agg = 'sum'):
        _st = self.__cin_stime
        _et = self.__cin_etime
        _m  = self.__cin_metric_name

        # 형식 YYYY/MM/DD-HH:00:00
        starttime = "%s/%s/%s-%s:00:00" % (_st[0:4], _st[4:6], _st[6:8], _st[8:10])
        endtime   = "%s/%s/%s-%s:00:00" % (_et[0:4], _et[4:6], _et[6:8], _et[8:10])

        # 참고 : "{"는 URL창에 %7B 로 표현됨
        url_tsdb = self.__cin_url + "start=" + starttime + "&end=" + endtime + "&m=" + agg + ":" + _m + _tag
        #print url_tsdb

        try :
            tsdbdata = urllib2.urlopen(url_tsdb)
            _read_buf = tsdbdata.read() # get string of TSDB value

        except urllib2.HTTPError as e:
            error_msg = e.read()
            print "\n < There is no data in TSDB of requested Metric or Tag : %s> \n" %_tag
            #print "\n < BerePi grep error message from Server > \n\n", error_msg
            return False, '[]' 

        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'Error code: ', e.code
            print "\n < Timeout error : %s> \n" %_tag
            return False, '[]'
        
        if _read_buf !='[]' : 
            _ext_f = True
            _read_buf = _read_buf[1:-1]
            _buf_dict = ast.literal_eval(_read_buf)
        else : 
            _ext_f = False
            _buf_dict = _read_buf

        #print type(_buf_dict)
        #print _buf_dict

        return _ext_f, _buf_dict

    '''
    ## 함수 : readTSD
    parameter1 (in_datelist) : 시각 리스트
    parameter2 (in_mdsid_list) : 미터기 아이디 리스트
    반환 (retList) : 비어있지 않은 아이디 리스트
    (예) http://xxx.xxx.xxx.xxx:4242/#start=2016/11/01-00:00:00&end=2017/03/01-00:00:00
    &m=sum:origin_data_please{factory_mart=mart,led_inverter=led}
    '''
    def readTSD(self, _tag = None, agg=sum) :
        _m = self.__cin_metric_name
        _p = self.__cin_datelist

       # Tag 한개인 경우, 중간에 여러개인 경우 추후 수정 필요
        s = ''
        if _tag != None: 
            #태그 여러개인 경우 #for (k, v) in _tag.items():
            s += 'modem_num=%s,' % (_tag)
            s = '{' + s[:-1] + '}'

        _existence, _val = self.get_tsdb_value(s, agg)

        if _existence == False : return None
        
        return _val


    def readOnePoint(self, _t, _tag = None, _agg = None) :
        _u = self.__cin_url
        _m = self.__cin_metric_name
        if _agg == None : _agg = 'sum'
       
        # it rturns end time, just 1 hour + of stime
        _t = self.changeTimeForOnePointReading(_t)

        __in_st = self.__cin_stime
        __in_et = self.__cin_etime
        st = "%s/%s/%s-%s:00:00" % (__in_st[0:4], __in_st[4:6], __in_st[6:8], __in_st[8:10])
        et = "%s/%s/%s-%s:00:00" % (__in_et[0:4], __in_et[4:6], __in_et[6:8], __in_et[8:10])
        url = '%sstart=%s&end=%s' % (_u,st,et) 
        # 기준시간을 입력. 기준 시간  보다 1시간 이후 시간으로 설정
        url += '&m=%s:%s' %(_agg, _m)

        #_tag_dict = ast.literal_eval(_tag)
        assert isinstance(_tag, dict)

        if len(_tag):

            url += '{'
            for (k, v) in _tag.items(): url += '%s=%s,' % (k, v)
            url = url[:-1] + '}'

            try : ret = requests.get(url=url)
            except:
                print " <Error>... connect to restful SEVER"

        #print "\n Receive OK from server.... " + str(ret) + "\n"
        # print if have not proper return  
        #if ret.status_code > 200 : print "\n " + str(ret.text) + "\n"

        if ret.ok:
            data = ret.json() 
            if len(data) == 0 : return None
            # this line is not working on RSP2. use below loads() rather than .json()
            assert isinstance(data, (list, tuple))
            dps = data[0]['dps']
            assert isinstance(dps, dict)  # 't' --> value
            if len(dps):
                min_time = sorted(dps.keys())[0]
                value = dps[min_time]
                epoch = float(min_time)
                ts = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
                return (value, ts, epoch)

    def readTSDrecent(self,  _tag = None, _agg = None, _start='10m-ago') :

        #if self.__cin_recent != 'True' : exit (" <Error> check call for *recent* ")
        _u = self.__cin_url
        _m = self.__cin_metric_name
        if _agg == None : _agg = 'sum'

        url = '%sstart=%s' % (_u, _start)
        url += '&m=%s:%s' %(_agg, _m)
        #_tag_dict = ast.literal_eval(_tag)
        assert isinstance(_tag, dict)

        if len(_tag):

            url += '{'
            for (k, v) in _tag.items():
                url += '%s=%s,' % (k, v)
            url = url[:-1] + '}'

            try : ret = requests.get(url=url)
            except:
                print " <Error>... get restful"

        #print "\n Receive OK from server.... " + str(ret) + "\n"
        if ret.ok:
            data = json.loads(ret.text)
            assert isinstance(data, (list, tuple))
            dps = data[0]['dps']
            assert isinstance(dps, dict)  # 't' --> value
            if len(dps):
                max_time = sorted(dps.keys())[-1]
                value = dps[max_time]
                epoch = float(max_time)
                ts = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
                return (value, ts, epoch)

########## end of class u_tsdb

'''
## 함수 : dateInt
문자열 date를 정수형으로 변환
parameter1 (in_time) : 문자형 date 값
parameter2 (mdh) : 연, 월, 일, 시간의 분류 (y, m, d, h)
반환 (re_mdh) : 변환 된 정수
'''
def dateInt(in_time, mdh):
    # year
    if mdh == 'y': re_mdh = int(in_time[0:4])
    # month
    if mdh == 'm':
        if in_time[4] == '0': re_mdh = int(in_time[5])
        else: re_mdh = int(in_time[4:6])
    # day
    elif mdh == 'd':
        if in_time[6] == '0': re_mdh = int(in_time[7])
        else: re_mdh = int(in_time[6:8])
    # hour
    elif mdh == 'h':
        if in_time[8] == '0': re_mdh = int(in_time[9])
        else: re_mdh = int(in_time[8:10])
    return re_mdh

'''
## 함수 : twodigitZero
한자리 정수 에 0을 추가
'''
def twodigitZero(in_num):
    if in_num < 10: re_num = '0' + str(in_num)
    else:
        re_num = str(in_num)
    return re_num


def parse_args():
    story = 'OpenTSDB needs many arguments URL, start time, end time, port '
    usg = '\n python tsdb_read.py  -url x.x.x.x -port 4242 -start 2016110100 -end 2016110222 -m metric_name, -wm write_metric_name --help for more info'
    parser=argparse.ArgumentParser(description=story, usage=usg, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-url",    default="http://125.140.110.217", help="URL input, or run fails")
    parser.add_argument("-start",  default='20160701', help="start time input, like 2016110100")
    parser.add_argument("-end",    default='20170101', help="end time input, like 2016110223")
    parser.add_argument("-port",   default=4242, help="port input, like 4242")
    parser.add_argument("-recent", default=True, help="Time input for recent value")
    parser.add_argument("-m", default='rc04_simple_data_v3', help="metric ")
    parser.add_argument("-wm", default='EE_test_0001', help="write-metric ")
    args = parser.parse_args()
    
    #check args if valid
    url = args.url
    _ht = 'http://'
    if ( url[:7] != _ht ) : url = _ht + url
    port = args.port
    if  port == 80 : port = ''
    else : port = ":"+ str(port)
    url = url + port +'/api/query?'

    start = args.start
    if start != None : start = args.start
    end = args.end
    if end != None : end = args.end

    recent = args.port
    if recent != None : recent = args.recent

    m = args.m
    if m == None : exit("... please input metric name")

    wm = args.wm
    
    return url, port, start, end, recent, m, wm

# 시간사이 데이터 읽기
def ptest(__url, __st, __et, __m):
    tsdbclass = u_ee_tsdb(__url, __st, __et)
    tag = __m
    if (tag == None) : return
    tsdbclass.set_metric(tag)
    print tsdbclass.readTSD()

# 최근 데이터 읽기
def rtest(__url, __m, __tag):
    tsdbclass = u_ee_tsdb(__url, None, None, True)
    tsdbclass.set_metric(__m)
    tag = __tag
    if (tag == None) : return
    print tsdbclass.readTSDrecent(tag, 'sum')

# 특정 시간에 가까운 데이터 읽기
def point(__url, __m, __time, __tag):
    tsdbclass = u_ee_tsdb(__url, __time)
    tsdbclass.set_metric(__m)
    tag = __tag
    if (tag == None) : return
    print tsdbclass.readOnePoint(__time, tag, 'sum')

    cnt = 0
    loop = 0

def countall(__url, __m,  __st, __et):
    tsdbclass = u_ee_tsdb(__url, __st, __et)
    tsdbclass.set_metric(__m)
    cnt = 0
    loop = 0
    for tagid in ltelist : 
        print "Start processing ....", tagid[0], '>>'
        #tsdb에서 데이터 읽어오기
        #인자 (태그, agg)
        _buf_dict = tsdbclass.readTSD(tagid[0], 'count')
        if _buf_dict is None: continue
        for (k, v) in _buf_dict['dps'].items():
            #pair = '%s=%s' % (k, v)
            __ut = '%s' %(k)
            __v = '%s' %(v)
            cnt = cnt + v
            loop = loop + 1
        print "      Data piont exists in DB ID-%s, 유닉스 시간 : %s  데이터 갯수 : %s, 누적 데이터 갯수 : %s " %( tagid[0], __ut, __v, cnt)

    print 
    print  '        Total Count of TSDB %s' %__m, 'is', cnt 


def cpmetric(__url, __m,  __st, __et, __wm):
    tsdbclass = u_ee_tsdb(__url, __st, __et)
    tsdbclass.set_metric(__m)
    cnt = 0
    loop = 0
    num_cnt = 0
    
    print 'Started time is : %s\n' % datetime.datetime.now()
    print 'ltelist :%d 추출' % (len(ltelist))

    for tagid in ltelist :
        num_cnt += 1
        #print tagid[0]
        #tsdb에서 데이터 읽어오기
        _buf_dict = tsdbclass.readTSD(tagid[0], 'sum')
        if _buf_dict is None: continue
        for (k, v) in _buf_dict['dps'].items():
            #pair = '%s=%s' % (k, v)
            __ut = '%s' %(k)
            __v = '%s' %(v)
            __qv = '%s' %(3*v/4.0)
            cnt = cnt + v
            loop = loop + 1
            #print __ut
            sockWriteTSD( __wm, __ut, __qv, tagid[0] )
        print 'ltelist :[%d] / [%d] 처리' % (num_cnt, len(ltelist))
            #print "processing ....", tagid[0], '>'
        #print  'Total Count of TSDB %s' %__m, 'is', cnt
    print '끝시간 : %s\n' % datetime.datetime.now()

def sockWriteTSD(__wmetric, __utime, __value, __tags = None):

    if __tags == None: __tags = 'ops=copy'

    _buf = "put %s %s %s modem_num=%s\n" %( __wmetric, __utime, __value, __tags)

    HOST = '125.140.110.217'
    PORT = 4242
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    ret = sock.sendall(_buf)
    #print '  .... writing', ret, _buf
    return

if __name__ == "__main__":
    u, p, stime, etime, recent, metric, write_metric = parse_args()

    #tag = {'mds-id':'911'}

    if recent == 'True' :
        rt = rtest(u, metric, tag)
    #elif (etime == None) and (stime != None)  :
    #    rt = point(u, metric, stime, tag)
    cpmetric(u, metric, stime, etime, write_metric )
#    countall(u, metric, stime, etime)


    #def __init__(self, __url, __st = None, __et = None, __r = None) :
    #para1 = 'gyu_RC1_co2.ppm'
    #para2 = {'id':'924'}
    #print get_last_value('125.7.128.53:4242', str(para1), para2)
    #python useTSDB.py -url tinyos.iptime.org -port 4242 -recent True -m rc01.t_power.WH
    #/api/query?start=2017/06/23-00:00:00&end=2017/06/23-00:01:00&m=sum:rc01.t_power.WH{id=911} 
    # -url 125.140.110.217 -port 4242 -start 20161101 -end 2016110207 -m origin_data_please
    # -url tinyos.iptime.org -port 4242 -m rc01.temp.degree -recent True
    # python useTSDB.py -url 125.140.110.217 -port 4242 -start 2016070100 -end 2016080100  -m rc04_simple_data_v3 -recent None -wm ____test_write

    # 메트릭 복사할때 사용
    # python countTSDB.py -url 125.140.110.217 -port 4242 -start 2016070100 -end 2016080100  -m rc04_simple_data_v3 -recent None -wm ___zz_000write_000