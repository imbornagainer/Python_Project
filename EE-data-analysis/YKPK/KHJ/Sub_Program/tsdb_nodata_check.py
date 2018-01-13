# -*- coding: utf-8 -*-
# Author : jeonghoonkang , https://github.com/jeonghoonkang

### TO DO : LTE Number로 변경해서 처리해야함
### 오라클DB가 아닌 OpenTSDB에서 데이터를 읽어와야함
    
import time
import datetime
#import cx_Oracle
import os
import sys
import requests
import argparse
import json
import time, datetime
import numpy as np
import socket
import urllib2
import sys
import ast
sys.path.append("./")
#import useTSDB

#import _input_list_17_0904 as _ids

url = "http://125.140.110.217:4242/api/query?"
#url = "http://49.254.13.34:4242/api/put"
response ={}
zero_list = [['0',0]]
HOST = '125.140.110.217'
PORT = 4242
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

class u_ee_tsdb :

    __cin_stime = None #시작시간
    __cin_etime = None #종료시간
    __cin_url = None
    __cin_recent = None
    __cin_datelist = []
    __cin_metric_name = None

    # 시간은 string type 예) 20160701
    def __init__(self, __url, __st = None, __et = None, __r = None) :
       self._url(__url)
       if __st != None and __et != None and __r != None : exit (" < Input Error > no time info")
       elif __st != None and __et != None : self._set_time_period(__st, __et)
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
    # 최소한 시작 시간 필

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

        print self.__cin_url, self.__cin_stime, self.__cin_etime

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
    def get_tsdb_value(self, _tag = None):
        _st = self.__cin_stime
        _et = self.__cin_etime
        _m  = self.__cin_metric_name

        # 형식 YYYY/MM/DD-HH:00:00
        starttime = "%s/%s/%s-%s:00:00" % (_st[0:4], _st[4:6], _st[6:8], _st[8:10])
        endtime   = "%s/%s/%s-%s:00:00" % (_et[0:4], _et[4:6], _et[6:8], _et[8:10])

        # 참고 : "{"는 URL창에 %7B 로 표현됨
        url_tsdb = self.__cin_url + "start=" + starttime + "&end=" + endtime + "&m=none:" + _m + _tag
        #print 'url_tsdb : %s' % url_tsdb
        try :
            tsdbdata = urllib2.urlopen(url_tsdb)
            _read_buf = tsdbdata.read() # get string of TSDB value
            #print '_read_buf : %s' % _read_buf
#             response = requests.get(url_tsdb)
#             if response.ok:
#                 print 'response.text : %s' % response.text
#                 return response.json()
#             else:
#                 print 'request fails'
#                 return []

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
    def readTSD(self, _tag = None) :
        _m = self.__cin_metric_name
        _p = self.__cin_datelist
        s = ''
        if _tag != None: 
            for (k, v) in _tag.items():
                s += '%s=%s,' % (k, v)
            s = '{' + s[:-1] + '}'

        _existence, _val = self.get_tsdb_value(s)

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

    def readTSDrecent(self,  _tag = None, _agg = None, _start = '10m-ago', _end = "10m_later") :

        #if self.__cin_recent != 'True' : exit (" <Error> check call for *recent* ")
        _u = self.__cin_url
        _m = self.__cin_metric_name
        if _agg == None : _agg = 'sum'

        url = '%sstart=%s' % (_u, _start)
        url += '&end=%s' %(_end)
        url += '&m=%s:%s' %(_agg, _m)
                
        #_tag_dict = ast.literal_eval(_tag)
        #assert isinstance(_tag, dict)
        print "2번"
#         if len(_tag):
# 
#             url += '{'
#             for (k, v) in _tag.items():
#                 url += '%s=%s,' % (k, v)
#             url = url[:-1] + '}'
# 
#             try : ret = requests.get(url=url)
#             except:
#                 print " <Error>... get restful"

        #print "\n Receive OK from server.... " + str(ret) + "\n"
        print "3번"
        print url
        try : ret = requests.get(url=url)
        except:
            print " <Error>... get restful"
        if ret.ok:
            print "4번"
            print "url : %s" % (url)
            data = json.loads(ret.text)
            assert isinstance(data, (list, tuple))
            return data
            
            dps = data[0]['dps']
            assert isinstance(dps, dict)  # 't' --> value
            if len(dps):
                max_time = sorted(dps.keys())[-1]
                value = dps[max_time]
                epoch = float(max_time)
                ts = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
                return (value, ts, epoch)

########## end of class u_tsdb

def parse_args():
    parser=argparse.ArgumentParser(description="how to run, insert TSDB SW",\
            usage='use "%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-st", "--starttime", default=20160701, help="input start time")
    parser.add_argument("-et", "--endtime", default=20170501, help="input end time")
    parser.add_argument("-sp", "--startpoint", default=0, help="start point of\
            input list(group of meter IDs) ")
    args = parser.parse_args()
    return args

#openTSDB 리턴 예시
#{'metric': 'rc03_simple_data_led', 'aggregateTags': [], 'dps': {'1467301500': 0.9279999732971191, '1467298800': 0.07500000298023224, '1467299700': 0.8870000243186951, '1467302400': 0.9399999976158142, '1467300600': 0.9010000228881836}, 'tags': {'holiday': '0', 'mds_id': '00-250068136', 'led_inverter': 'led'}}
# metric, dps, tags

def DCP(in_sttime, in_mdsid, tsdbclass, _tag):
    #print type(in_sttime) #datetime.date object

    date_str = ''
    date_str = date_str.join(str(in_sttime))
    #print date_str
    date_str = date_str.replace('-','')
    starttime = date_str

    # calculate endtime, in this case, just 1 day after starttime
    date_str = in_sttime + datetime.timedelta(days=1)
    date_str = str(date_str)
    date_str = date_str.replace('-','')
    #print date_str
    endtime = date_str

    mdsid = in_mdsid
    #print starttime, endtime
    tsdbclass._set_time_period(starttime, endtime)

    #_tag = {'mds_id': str(mds_id)}
    ret_dict = tsdbclass.readTSD(_tag)
    #print ret_dict
    #ret_dict = openTSDB return 값
    __mds_id = str(_tag['modem_num']) # mds_id 를 string으로 만든게 __mds_id

    if ret_dict == None:
        i = 0
        for i in range(0,len(zero_list)):
            if zero_list[i][0] == __mds_id :
                zero_list[i][1] += 1
                return 0
            else :
                pass
        # 작성형식 [id, 데이터없는 날짜수]            
        zero_list.append([__mds_id,1])
        return 0

    return 42

def ch2date(_s, _e):

    ys = int(_s[:4])
    ms = int(_s[4:6])
    ds = int(_s[6:8])
    ye = int(_e[:4])
    me = int(_e[4:6])
    de = int(_e[6:8])
    sday = datetime.date(ys,ms,ds)
    eday = datetime.date(ye,me,de)

    return sday, eday


# main function
if __name__ == "__main__":

    arg = parse_args()

    sttime = '20160701'
    entime = '20170501'
    __st = sttime
    __et = entime

    if (arg.starttime != None) : sttime = arg.starttime
    if (arg.endtime != None) : entime = arg.endtime
    #spoint_index = arg.startpoint
    print ("   " + "processing ... ")
    print ("  ", sttime, entime)

    __m = "rc05_operation_tag_v3"

    filename = '_zero_no_data_result_20160701_toentime_20170501_real.txt'
    resultfile = open(filename,"a")

    dix = 1
    tagdata = ['aa','aa','aa','aa']

    #input dictionary
    #important : this is input file, make it clear which the input data
    #id_tag = _ids.modem_list

    ids = ['01222799986', '01220800574', '01224230529', '01222714543', '01224230467', '01223239869', '01224230576', '01222679989', '01222746396', '01222746350', '01224230549', '01223192391', '01221343888', '01224230577', '01222729929', '01221574361', '01224230493', '01224230501', '01224272949', '01224230526', '01221386983', '01223239875', '01223239870', '01221451993', '01221251996', '01224230542', '01224230434', '01224230480', '01224230484', '01224230485', '01224230470', '01222746456', '01222742834', '01223219133', '01223219131', '01223219130', '01223219129', '01223192247', '01222745462', '01221574357', '01222699986', '01222742200', '01222649984', '01222754504', '01222739929', '01224230571', '01222674503', '01224230527', '01224230569', '01222669986', '01223187397', '01223209886', '01222764501', '01222742912', '01224272962', '01222745935', '01222745933', '01222745947', '01222742969', '01222742878', '01222746463', '01223239874', '01223239873', '01222704503', '01223187431', '01223187430', '01224272938', '01222745939', '01222674501', '01220684147', '01222694501', '01222734501', '01223187419', '01223188270', '01223189537', '01222769929', '01221574356', '01224230509', '01224230472', '01224230478', '01222746390', '01222745510', '01222719929', '01221574359', '01222746366', '01222779929', '01223239865', '01223219128', '01224230518', '01223187436', '01223188269', '01222754503', '01222742885', '01222745938', '01222724503', '01222704504', '01222742752', '01222694503', '01224230546', '01221341991', '01224224149', '01220800623', '01220435025', '01224230511', '01224230515', '01224230461', '01224230533', '01224230451', '01223209883', '01223209884', '01223219126', '01223209881', '01223192283', '01222654504', '01222755541', '01222766541', '01222709541', '01222744754', '01222719541', '01222739541', '01222587543', '01222666541', '01221291991', '01223192386', '01222714503', '01224230446', '01224230532', '01222667543', '01222764503', '01222586543', '01222684504', '01222699987', '01222742956', '01222684501', '01222699984', '01224230479', '01221731209', '01224230558', '01224230495', '01222739987', '01222739986', '01221388812', '01221388441', '01221721213', '01221961213', '01223187386', '01223192395', '01224273086', '01222567452', '01222587452', '01221566970', '01221566958', '01222714504', '01222664504', '01222676543', '01222742757', '01222647452', '01222744504', '01222749989', '01222746383', '01222776543', '01222745635', '01222597452', '01222745363', '01222779984', '01224230436', '01222758870', '01221474412', '01221474414', '01222779987', '01224273013', '01222745527', '01222745458', '01222664501', '01222779986', '01224230496', '01221566963', '01221574336', '01224230433', '01222767541', '01222742927', '01222742916', '01222689984', '01222687452', '01222742760', '01224230525', '01222797541', '01224230439', '01224272937', '01224272982', '01224230449', '01224230506', '01222746381', '01224230477', '01224273037', '01223192327', '01223192308', '01223192263', '01223192287', '01223192392', '01224230491', '01221421994', '01221441994', '01222749929', '01222659986', '01224230473', '01223187393', '01224230530', '01223239872', '01224230488', '01223187389', '01223209885', '01224273039', '01224273091', '01224230570', '01224272955', '01224230483', '01224230513', '01224230482', '01223239867', '01224230507', '01224230517', '01224273038', '01224230490', '01222704501', '01222798870', '01223239866', '01222754501', '01222709929', '01222748870', '01224230528', '01222683542', '01222664503', '01222654503', '01222674504', '01222746482', '012227694504', '01222719989', '01221448178', '01222744503', '01223192284', '01223187417', '01223187414', '01222759929', '01221311993', '01221243882', '01221361991', '01223192328', '01221371991', '01221474413', '01221273883', '01222654501', '01222799985', '01221253884', '01220800593', '01222742949', '01222746459', '01222684503', '01224230460', '01224230565', '01224230465', '01221388068', '01221391442', '01221391244', '01221391199', '01221391155', '01224230476', '01221574346', '01221567020', '01222765541', '01222734504', '01221566961', '01221566960', '01223189591', '01221566971', '01223187435', '01221574354', '01223188887', '01221574324', '01221567011', '01222742946', '01222636543', '01222659984', '01222745943', '01222563542', '01224230564', '01224230568', '01224230541', '01220800748', '01222744780', '01224230541', '01224230539', '01224230534', '01222745479', '01222729989', '01222577452', '01222746397', '01222779985', '01222769989', '01222729987', '01222688541', '01222618542', '01224230435', '01224230487', '01223209889', '01223209891', '01223209888', '01224230504', '01224230486', '01224230469', '01224230510', '01222746461', '01224230443', '01222796541', '01224230512', '01222742798', '01222746421', '01222753541', '01222744501', '01222749984', '01222749985', '01222742888', '01222742934', '01222788870', '01222746472', '01222597541', '01222769542', '01222616541', '01222742704', '01224230437', '01222724501', '01221283886', '01222564542', '01222742908', '01222745934', '01222745495', '01222745859', '01224230516', '01224230500', '01221390965', '01221387937', '01221474387', '01221351991', '01221431994', '01221261996', '01222769984', '01223187402', '01223187398', '01223187384', '01223187403', '01223187406', '01224272944', '01221429366', '01221429367', '01221429369', '01221471994', '01221474403', '01221474402', '01221474406', '01221474407', '01221341993', '01221371993', '01223192410', '01223192453', '01221243885', '01221243887', '01224230464', '01223192393', '01223192394', '01223187395', '01224230458', '01224230459', '01222746380', '01222794503', '01222759989', '01220800701', '01222734543', '01222747452', '01223187394', '01223187387', '01221463494', '01221429368', '01221390254', '01221388836', '01221474404', '01221474405', '01222789986', '01224230502', '01224273014', '01224272948', '01223187306', '01223187305', '01221392626', '01221392897', '01224272943', '01224273042', '01223187310', '01223187316', '01223181056', '01223181052', '01223187319', '01223192261', '01223187358', '01224230567', '01224273017', '01223187286', '01223180993', '01220553054', '01224273061', '01224273022', '01221392027', '01221389654', '01221390900', '01221387086', '01221387826', '01223187380', '01221399481', '01221393131', '01221393546', '01224273046', '01224273052', '01223239879', '01223239880', '01223239878', '01223239876', '01223192275', '01223192271', '01223192368', '01223192376', '01223192373', '01223181052', '01223181049', '01224273085', '01224273018', '01224273092', '01224273096', '01223180966', '01223180976', '01224230447', '01224230455', '01224230466', '01224230441', '01224230521', '01224272948', '01224273045', '01224272958', '01224230559', '01224273026', '01224273079', '01224272971', '01223192371', '01223187370', '01223192249', '01220800675', '01224272988']
    #ids = _ids.modem_list
    toendpoint = len(ids)

    # DAY _ loop
    # sday 시작일 eday 종료일 mday 시작~종료까지 증가하는 date
    # lds : loop days
    sday, eday = ch2date(__st, __et)
    mday = sday
    lds = repr(eday - sday)
    lds = lds[ lds.index( '(' )+1 : lds.index( ')' ) ]

    # TSDB 시작일만 등록
    tsdbclass = u_ee_tsdb(url, __st)
    tsdbclass.set_metric(__m)

    while (eday != mday) :
        # just day count
        dix = dix + 1

        # mday 데이터 처리
        # print mday

        # 모든 MDSiD에 대해서 처리, MDSID는 위의 import _mds_id 에서 읽음
        for i in range (toendpoint):
            serial_id = ids[i]
            s_id = str(serial_id)
            #print s_id
            #중요: 빈칸이 제일 앞에 있으면 TSDB read 시에 에러남
            if (s_id[0] == ' ') : s_id = s_id[1:]
            #print "  >>", s_id            
            _tag = { 'modem_num': serial_id }
            #print _tag

            donecheck = DCP(mday, serial_id, tsdbclass, _tag)
        time.sleep(0.0001)

        # mday 1일 증가
        mday = mday + datetime.timedelta(days=1)

        pout = " ... main loop -> dix: %s, : lds %s 전체 진행률: %s 퍼센트 진행!  \r" \
                %(dix, lds,int(float((dix)/float(lds))*100))
        sys.stdout.write(pout)
        sys.stdout.flush()
        resultfile.write(pout)
        resultfile.flush()
    fname = '171109_out_list.py'
    f = open(fname,'w')
    f.write('zero_list = ')
    f.write(str(zero_list))
    f.write('\n\n')

    sock.close()
    print (" \n ... Finishing copying ... check file ", fname)
    
