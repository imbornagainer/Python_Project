# -*- coding: utf-8 -*-
# Author : hwijinkim , https://github.com/imbornagainer

# openTSDB의 저장된 metrics를 get한 data와 개인의 data의 교집한 data값만 복사하기 위한 class 
# last modified by 20171026

import time
import datetime
import os
import sys
import requests
import json
import argparse
import calendar
import urllib2
from _input_list_17_0906 import modem_list, led_modem_list, inverter_modem_list

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

    def readTSDrecent(self,  _tag = None, _agg = None, _start = '10m-ago', _end = "10m-later") :
        #if self.__cin_recent != 'True' : exit (" <Error> check call for *recent* ")
        _u = self.__cin_url
        _m = self.__cin_metric_name
        if _agg == None : _agg = 'none'

        url = '%sstart=%s' % (_u, _start)
        url += '&end=%s' % (_end)
        url += '&m=%s:%s' % (_agg, _m)
                
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
        print "url : %s" % url
        if ret.ok:
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
    usg = '\n python tsdb_read.py  -url x.x.x.x -port 4242 -start 20161101 -end 20161102, --help for more info'
    parser = argparse.ArgumentParser(description=story, usage=usg, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-url", default="125.140.110.217", help="URL input, or run fails")
    parser.add_argument("-start", default='2016/07/01-00:00:00', help="start time input, like 2016/07/01-00:00:00")
    parser.add_argument("-end", default='2017/05/01-00:00:00', help="end time input, like 2016/07/02-00:00:00")
    parser.add_argument("-port", default=4242, help="port input, like 4242")
    parser.add_argument("-recent", default="True", help="Time input for recent value")
    parser.add_argument("-m", default="rc04_simple_data_v3", help="metric name")
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
    
    return url, port, start, end, recent, m

def rtest(__url, __m, __tag, __stime, __etime):
    tsdbclass = u_ee_tsdb(__url, None, None, True)
    tsdbclass.set_metric(__m)    
    tag = __tag
    #tag = ""    # tag가 없는 관계로 빈값을 입력
    stime = __stime
    etime = __etime
    if (tag == None) : return
    
    # print tsdbclass.readTSDrecent(tag, 'sum', __stime)
    list_data = tsdbclass.readTSDrecent(tag, 'none', stime, etime)
    return list_data

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == "__main__":
    u, p, stime, etime, recent, metric = parse_args()
    
    put_url = "http://125.140.110.217:4242/api/put" # api/put에 값을 주지 않는다면 db는 받질 않는다.
    new_metric = 'rc05_adj_copy_tag_v2'             # 새로 put할 metric 설정하는 변수 (원하는 metric명을 입력하면 된다.)
    progress_num = 0
    
    print '<총 {0!r}개의 데이터 추출>'.format(len(modem_list))
    print 'Start!'
    print 'Started time is : %s\n' % datetime.datetime.now()
    
    for modem_num in modem_list:
        adj_modem_num = str(modem_num)[2:-2]
        print "%d : %s" % (progress_num+1, adj_modem_num)
        tag = {'modem_num':adj_modem_num}
        
        if recent == 'True':
            if tag == "":tag = ""        # 특정 tag가 없음(시간을 기준으로 get한 모든 값을 얻기 위함)    
            get_list_data = rtest(u, metric, tag, stime, etime)
        else:
            print "Sorry... Not ready to Get"
            exit()

        if get_list_data == None:continue   #if no data, go to the next iteration
        
        #From start날짜 To last data하루값 씩 last
        while is_past(end, last):
            start = end
            end = add_time(start, days=1)
            led['holiday'] = is_weekend(start)
            query_result = tsdb_query(query, start, end, metric_in, led[get_tag_ref('led_modem_serial')], led['holiday'])
            for group in query_result:
                if USE_HTTP_API_PUT:
                    tsdb_put(put, metric_out, group['dps'], led, out_file)
                else:
                    tsdb_put_telnet(host, port, metric_out, group['dps'], led, out_file)
        
        for i in range(len(get_list_data)):
            mds_id = get_list_data[i]['tags']['_mds_id']
            holiday = get_list_data[i]['tags']['holiday']
            led_inverter = get_list_data[i]['tags']['led_inverter']

            progress_num += 1
            for (unix_time, value) in get_list_data[i]['dps'].items():
                input_data = {
                    "metric": new_metric,
                    "timestamp": unix_time,
                    "value": value,
                    "tags": {
                        "holiday": holiday,
                        "_mds_id": mds_id,
                        "modem_num": adj_modem_num,
                        "led_inverter": led_inverter,
                    }
                }
                try:
                    input_data=json.dumps(input_data)
                    ret = requests.post(put_url, input_data)
                except urllib2.HTTPError as e:
                    error_msg = e.read()
                    print ( "exception during requests HTTP", error_msg)
            print '<총 {0!r}/{1!r}개의 Data를 처리>'.format(progress_num, len(modem_list))
            printProgress(progress_num, len(modem_list), 'Progress:', 'Complete', 1, 50) # show progress
            print '\n'
    print 'end!'
    print 'Ending time is : %s\n' % datetime.datetime.now()