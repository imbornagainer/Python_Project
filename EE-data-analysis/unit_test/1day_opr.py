# -*- coding: utf-8 -*-

# Author : JeonghoonKang , https://github.com/jeonghoonkang

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import socket
import copy
import numpy as np
import datetime
import time
import sys

if (0) :
    PATH = 'C:\Users\Be Pious\git\kdatahub\EE-data-analysis\lib\tools'
else:
    PATH = '../lib'

sys.path.insert(0, PATH)
import in_list
#import useTSDB
sys.path.insert(0, PATH)

with open(PATH+'/tools/count_list.json') as data_file:
    data_json = json.load(data_file)

HOST = 'tinyos.asuscomm.com'
PORT = 44242
USE_HTTP_API_PUT = False

def pack_dps(metric, dps, tags):
    pack = []
    #print 'tags : %s' % tags
    tag = {'metric': metric, 'tags': tags}

    for dp in dps:
        #print 'dp : %s' % dp
        sdp = copy.copy(tag)
        sdp['timestamp'] = int(dp.encode('utf8'))
        sdp['value'] = dps[dp]
        #print sdp
        pack.append(sdp)
    return pack

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,):

    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def query(start, end, metric, tags):
    host = '125.140.110.217'
    port = 4242
    api_query = 'http://{0!s}:{1!r}/api/query'.format(host,port)
    param = {}

    if start: param['start'] = start
    if end: param['end'] = end

    param['m'] = metric + '{'
    for i, tag in enumerate(tags):
        param['m'] += tag + '={0!s}'.format(tags[tag])
        if i < len(tags) - 1:
            param['m'] += ','
    param['m'] += '}'

    if 1:
        response = requests.get(api_query, params=param)
        if response.ok:
            return response.json()
        else:
            return []

def tsdb_query(query, start, end, metric, modem, holiday):
    param = {}
    if start: param['start'] = start
    if end: param['end'] = end
    param['m'] = metric + '{' + 'holiday={1!s},modem_num={0!s}'.format(modem, holiday) + '}'

    if 1:
        response = requests.get(query, params=param)
        if response.ok:
            return response.json()
        else:
            print 'request fails'
            return []
    else:
        try:
            response = requests_retry_session().get(query, params=param, timeout=5)
        except Exception as x:
            print 'requests timeout'
        else:
            if response.ok:
                return response.json()
        return []

def tsdb_put(put, metric, dps, tags, file=None):
    '''
    네트워크 커넥션 상태에 따라 Http 가 느리고,
    접속이 자주 끊겨서 처리 데이터량이 많을 경우는 사용하지 않음
    '''
    packed_data = pack_dps(metric, dps, tags)
    for i in xrange(0, len(packed_data), 8):
        tmp = json.dumps(packed_data[i:i+8])
        if 0:
            response = requests.post(put, data=tmp)
        if response.text: print response.text
        else:
            try:
                response = requests_retry_session().post(put, data=tmp, timeout=5)
            except Exception as x:
                print 'requests timeout'
            else:
                if response.text: print response.text
    return

def tsdb_put_telnet(host, port, metric, dps, tags, file='False', outlier_txt_name='outlier.txt'):
    '''
    소켓으로 서버에 연결하고, Text 를 입력하여 데이터를 openTSDB에 입력
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    retry = 9999
    while 1:
        try:
            sock.connect((host, port))
        except:
            print 'socket error: ' + host
            time.sleep(5)
            print 'time sleep 5 second'
            if retry > 0:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                continue
            else:
                print 'skip this dps'
                return
        else:
            break
    send = ''
    count = 0
    #print 'put dps: {0} requested...'.format(len(dps))

    packed_data = pack_dps(metric, dps, tags)

    # time loop 2016/07/01 ~ 2017/07/01 by 15min, unix_time
    # check the data is None

    for dp in packed_data:
        if 1:
        #if (dp['value'] != 0 and dp['value'] != None and dp['value'] > 0.01 and dp['value'] <= 200.0):   # outlier 조건 설정
            if len(send) >= 1024:
                #print send + '\n\n'
                sock.sendall(send)
                #if file: file.write(send)
                send = ''
            #print 'type : %s' % type(dp['metric'])
            #print "dp['metric'] : %s" % dp['metric']
            send += 'put'
            send += ' {0!s}'.format(dp['metric'])
            send += ' {0!r}'.format(dp['timestamp'])
            #send += ' 1'                                 # 값이 있으면 이진법 1처리(작동했다.)
            send += ' {0!r}'.format(dp['value'])
            #print 'dp : %s' % dp
            if 'tags' in dp:
                for key in dp['tags']:
                    #print 'key : %s' % key
                    send += ' {0!s}'.format(key) + '={0!s}'.format(dp['tags'] [key])
            send += '\n'
            #print 'send : %s' % send
            count += 1

        else:
            global chk_number
            chk_number = (chk_number + 1)
            Chk_Outlier(chk_number, outlier_txt_name, dp['tags']['modem_num'], dp['tags']['_mds_id'], dp['timestamp'], dp['value']) # outlier log 기록함수
    #print 'send : ' + send

    if len(send) > 0:
        #print send + '\n\n'
        sock.sendall(send)
        #if file: file.write(send)
        send = ''
    sock.close()
    #print 'put dps: {0} processed...'.format(count)
    return

def one_day_pattern (__url, __wm, __v, __st, __et, host, port):

    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
    holiday = '0'
    stam_list = []

    dt = datetime.datetime.strptime(__st, '%Y/%m/%d-%H:%M:%S')
    __st_unix = time.mktime(dt.timetuple())

    dt = datetime.datetime.strptime(__et, '%Y/%m/%d-%H:%M:%S')
    __et_unix = time.mktime(dt.timetuple())
    end = __et_unix
    #가동율 / 부하율 입력 선택
    metric_in  = 'avg:rc06_ld_rate_v3'                        # get할 metric명
    #metric_in  = 'avg:rc06_op_rate_v3'                       # get할 metric명
    __m = metric_in
    #metric_out 은 인자로 받음

    #last = 1464739200 #2016/07/01, second scale
    #end = 1464739800
    #end = 1509494400 #2017/11/01, second scale, 1498834800 17/7/1

    last = __st_unix
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    put_unix_time = 1464705900 # unix_time = 16/06/01 00:00:00
    #put_unix_time = 1462028400  # unix_time = 16/06/01 00:00:00

    for dev in data_json:
        ''' rate_result = query(start, end, 'none:rc05_operation_rate_v6', {'modem_num': dev})
            none aggregation 은 holiday 를 구분해서 읽어옴. 이런경우.
            holiday 태그 두개에 대해서 다 읽어야 함
            그래서 읽는 방법을 변경함. avg 로.
            led, tags,building '''

        if dev == 'led': totcount = 'total'
        else: totcount = 'each'
        ''' 디바이스타입 LED 의 경우 빌딩종류/업종 으로 두개로 나누어져, '''
        ''' 한 세트 만 처리하기 위해서는 total 과 each 로 나누어야 함'''

        tag_list = data_json[dev]['tags']

        for key in tag_list:                    # key is total, buildlng.... or
            for k,v in tag_list[key].items():   # tag --> building.office etc
                qtag = {}
                qtag['device_type'] = dev
                qtag[key] = k
                a_day_avg = {}
                a_day_cnt = {}
                a_day_avg_cmp = {}
                for x in range(0,96):
                   a_day_avg[x] = 0
                   a_day_cnt[x] = 0

                last = __st_unix
                print '\n', qtag

                days_long = 0
                ndays_long = 0

                while (last < end):
                    days_long += 1
                    start = datetime.datetime.fromtimestamp(int(last)).strftime('%Y/%m/%d-%H:%M:%S')

                    ''' Be careful, don't include 00:00 two times '''
                    mid = datetime.datetime.fromtimestamp(int(last)-1).strftime('%Y/%m/%d-%H:%M:%S')

                    mid = datetime2str((str2datetime(mid)) + datetime.timedelta(1))
                    ux_nday = datetime2ts(mid) + 1

                    holiday = is_weekend(start)
                    last = ux_nday # 하루 추가 진행을 위해 시간 변경

                    #리딩할 태그를 구성한다
                    if k == 'total':
                        qtag = {'device_type':dev}
                    if k == 'each': continue

                    wtag = ''
                    for wtag_k, wtag_v in qtag.items():
                        wtag += ' %s=%s' % (wtag_k,wtag_v)

                    if len(qtag.keys()) == 1 :
                        wtag += ' %s=%s' % ('totcount','total')
                    #wtag += ' %s=%s' % ('season',season)
                    wtag += ' \n'

                    ''' read TSDB and give it to processing  '''
                    ''' this is multiple LTE modems data, using group TAG '''
                    #print start, mid
                    _query_result = query(start, mid, __m , qtag)

                    if _query_result == '[]' or len(_query_result) < 1 :
                        ndays_long += 1
                        continue
                        # >>> to do : 쿼리 방식 변경 ... json 구조에 있는 것처럼 데이터를 호출해야 함
                        # >>> 예, device_type:led, building:office, detail:food
                        # >>> 태그는 위에서 호출한 태그 사용, 위 태그를 아래 Write 태그에 입력
                        ## 결과를 TSDB에 저장할때 달아놓을 태그들

                        ## 결과 저장할 (변수)
                        ## KEY는 시간 96개 단위
                        ## '00:00' : 평균값, '00:15' : 평균값
                        ## 시간은 편한방식으로 지정

                    denom1 = 1467298800
                    denom2 = 86400 # 60 * 60 * 24 = 하루를 second로 표시

                    ''' adding all the data of 15-min time slot of a year'''
                    #print len(_query_result[0]['dps'])
                    for k,v in _query_result[0]['dps'].items() :
                       daykey = (int(k) % denom1 % denom2) 
                       #if daykey == 0 :  print k, 
                       #if (daykey > 900*96) : print "something wrong"
                       daykey = (daykey) / 900
                       if (v == 0) : 
                           print "v is 0, Zero is not suitable for operation rate, we have to skip"
                           continue
                       a_day_avg[daykey] += v
                       a_day_cnt[daykey] += 1

                ''' put_unix_time = 1464705900  # unix_time = 16/06/01 00:00:00 '''
                #print a_day_cnt
                #print a_day_avg
                put_unix_time = 1464705900  # unix_time = 16/06/01 00:00:00
                for k,v in a_day_avg.items():
                    if ndays_long == days_long : 
                        #print ' no any 356 data, no input to DB '                        
                        continue
                    if a_day_cnt[k] == 0 : 
                        continue
                    if a_day_avg[k] == 0 : 
                        continue
                    #print "avg=", a_day_cnt[k], 'value=', v,
                    a_day_avg[k] = v / (a_day_cnt[k])
                    # not using below
                    #a_day_avg[k] = v / (1.0 * days_long - ndays_long)
                    #put_unix_time += 900

                    ''' after code verification, we should run write code below'''
                    sockWriteTSD( sock, __wm, put_unix_time, a_day_avg[k] , wtag)

                ' for debugging, print some parameters'
                print " total day=", days_long, "no data rcved day=", ndays_long
                #print a_day_avg
                #exit("exit print avg of query")
                
                tmp = 0
                for k,v in a_day_avg.items():
                    tmp += v
                tmp = tmp / len(a_day_avg)
                print "avg one-day operation rate", tmp
                

    ## 키 (시간) 루프 호출
    ## >> 해당 키 time 에 대해 전송된 모든 값을 더하고 / len(전체갯수) 함
    # key 호출 (시간)
    # 호출해서 아래 방법으로 시간 분류 (인덱싱) 0~95로 분류
    #- 1단계 : d = Unix Time % 1467298800 (2016/07/01 기준으로 처리)
    #- 2단계 : d = d % 86400 (하루 시간 내로만 범위 설정)
    #- 3단계 :  scale = d / 96, 하루는 96개 시간 단위로 분리됨

    sock.close()

def sockWriteTSD(sock, __wmetric, __utime, __value, __tags = None):

    if __tags == None: __tags = 'ops=copy'

    _buf = "put %s %s %s %s\n" %( __wmetric, __utime, __value, __tags)
    #print _buf

    try:
        ret = sock.sendall(_buf)
    except:
        print " something wroing in socket send function"
        pass
    time.sleep(0.0001)

    return

def ts2datetime(ts_str):
    return datetime.datetime.fromtimestamp(int(ts_str)).strftime('%Y/%m/%d-%H:%M:%S')

def datetime2ts(dt_str):
    dt = datetime.datetime.strptime(dt_str, "%Y/%m/%d-%H:%M:%S")
    return time.mktime(dt.timetuple())

def str2datetime(dt_str):
    return datetime.datetime.strptime(dt_str, "%Y/%m/%d-%H:%M:%S")

def datetime2str(dt):
    return dt.strftime('%Y/%m/%d-%H:%M:%S')

def add_time(dt_str, days=0, hours=0):
    return datetime2str(str2datetime(dt_str) + datetime.timedelta(days=days, hours=hours))

def is_past(dt_str1, dt_str2):
    return datetime2ts(dt_str1) < datetime2ts(dt_str2)

def is_weekend(dt_str):
    if str2datetime(dt_str).weekday() >= 5: return '1'
    else: return '0'

def run():
    __url = HOST           # get할 url
    port = PORT                         # get할 port 번호

    #__wm = '___oprate___test___001___'       # put할 metric명
    __wm = '___ldrate___test___001___'       # put할 metric명
    __v = None

#     __st = '2016/07/01-00:00:00'
#     __et = '2017/02/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port,'summer')

    __st = '2016/07/01-00:00:00'
    __et = '2017/07/01-00:00:00'
    one_day_pattern(__url, __wm, __v, __st, __et, __url, port)

#     __st = '2016/08/01-00:00:00'
#     __et = '2016/09/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port,'summer')
#
#     __st = '2016/09/01-00:00:00'
#     __et = '2016/10/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port,'summer')
#
#     __st = '2016/10/01-00:00:00'
#     __et = '2016/11/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port,'winter')
#
#     __st = '2016/11/01-00:00:00'
#     __et = '2016/12/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port,'winter')
#
#     __st = '2016/12/01-00:00:00'
#     __et = '2017/01/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port,'winter')
#
#     __st = '2017/01/01-00:00:00'
#     __et = '2017/02/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port,'winter')
#
#     __st = '2017/02/01-00:00:00'
#     __et = '2017/03/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port,'winter')

#     __st = '2016/07/01-00:00:00'
#     __et = '2016/08/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)

#     __st = '2016/08/01-00:00:00'
#     __et = '2016/09/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
#
#     __st = '2016/09/01-00:00:00'
#     __et = '2016/10/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
#
#     __st = '2016/10/01-00:00:00'
#     __et = '2016/11/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
#
#     __st = '2016/11/01-00:00:00'
#     __et = '2016/12/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
#
#     __st = '2016/12/01-00:00:00'
#     __et = '2017/01/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
#
#     __st = '2017/01/01-00:00:00'
#     __et = '2017/02/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
#
#     __st = '2017/02/01-00:00:00'
#     __et = '2017/03/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
#
#     __st = '2017/03/01-00:00:00'
#     __et = '2017/04/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
#
#     __st = '2017/04/01-00:00:00'
#     __et = '2017/05/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
#
#     __st = '2017/05/01-00:00:00'
#     __et = '2017/06/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
#
#     __st = '2017/06/01-00:00:00'
#     __et = '2017/07/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)

if __name__ == '__main__':
    #choice = input('1 = windows\n2 = linux\n')
    choice = 1
    if choice == 0:
        with open('C:/Users/Be Pious/git/kdatahub/EE-data-analysis/lib/tools/count_list.json') as data_file:
            data_json = json.load(data_file)
    else:
        with open('../lib/tools/count_list.json') as data_file:
            data_json = json.load(data_file)
    print data_json

    run()
