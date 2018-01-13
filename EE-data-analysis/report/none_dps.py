# -*- coding: utf-8 -*-

# Author : hwijinkim , https://github.com/jeonghoonkang

# outlier를 제거하기 위한 class
# last modified by 20171031

# ver 0.2
# 1. 함수에서 직접 outlier log txt 파일명 설정 -> main의 변수에서 수정하도록 변경 (편의를 위하여)

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
sys.path.insert(0, '../lib')
import in_list

#tag = {'mds-id':'911'}
HOST = '125.140.110.217'
PORT = 4242


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
    session=None,
):
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

def tsdb_query(query, start, end, metric, modem_num, holiday):
    param = {}
    if start: param['start'] = start
    if end: param['end'] = end
    param['m'] = metric + '{' + 'holiday={1!s},modem_num={0!s}'.format(modem_num, holiday) + '}'
    #print param
    if 1:
        response = requests.get(query, params=param)
        if response.ok:
            #print response.text
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
                #print response.text
                return response.json()
        return []

def tsdb_put(put, metric, dps, tags, file=None):
    packed_data = pack_dps(metric, dps, tags)
    for i in xrange(0, len(packed_data), 8):
        tmp = json.dumps(packed_data[i:i+8])
        #print tmp
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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    retry = 9999
    #print 'socket error: ' + host
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
            send += ' 1'                                 # 값이 있으면 이진법 1처리(작동했다.)
            #send += ' {0!r}'.format(dp['value'])
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


def find_none_dp(__url, __wm, __v, __st, __et, __period=900):

    host  = '125.140.110.217'                                       # get할 url
    port  = 4242                                                    # get할 port 번호
    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)       # opentsdb에서 get할 url 주소
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
    t_first = __st                                                  # get 시작일
    t_end  = __et                                                   # get 종료일
    metric_in  = 'none:rc06_operation_rate_v5'                       # get할 metric명
    #metric_out = 'rc05_none_dp_v1'                                 # put할 metric명
    metric_ref  = 'none:rc04_simple_data_v3'                        # get할 metric명

    chk_number = 0                                                  # outlier 갯수 num
    #modem_list = in_list.total_vlist
    modem_list2 = in_list.modem_list

    modem_count = 0                             # lte 처리 갯수

    chk_day = '2017/01/01-00:00:00'

    cnt = 0
    loop = 0
    dt = datetime.datetime.strptime(__st, '%Y/%m/%d-%H:%M:%S')
    __st_unix = time.mktime(dt.timetuple())
    last = __st_unix
    dt = datetime.datetime.strptime(__et, '%Y/%m/%d-%H:%M:%S')
    __et_unix = time.mktime(dt.timetuple())
    end = __et_unix

    mcount = 0
    xlist = modem_list2
    for modem in modem_list2:
        last = __st_unix
        mcount += 1
        pout = "  \n"
        sys.stdout.write(pout)
        #if modem_list.index(modem) < 121: continue

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        while (last < end):

            start = datetime.datetime.fromtimestamp(int(last)-5).strftime('%Y/%m/%d-%H:%M:%S')
            mid = datetime.datetime.fromtimestamp(int(last)+10).strftime('%Y/%m/%d-%H:%M:%S')

            pout = "  >>  %d / 350, modem: %s last: %d, end: %d, %s %s \r" %(mcount, modem, last, end, start,mid)
#             sys.stdout.write(pout)
#             sys.stdout.flush()

            modem_holiday = is_weekend(start)
            _query_result = tsdb_query(query, start, mid, metric_in, modem, modem_holiday) # operation rate 읽기

            if (last == __st_unix ) : # 처음 한번만 tag를 읽어 들임
                _ret = tsdb_query(query, start, chk_day, metric_in, modem, modem_holiday)
                __tag = _ret[0]['tags']
                #{u'load': u'none', u'building': u'factory', u'modem_num': u'01224230496',
                #u'company': u'middlecompany', u'detail': u'food', u'device_type': u'led', u'holiday': u'0', u'_mds_id': u'00-250130380'}
                _tag_buf = ''
                for k,v in __tag.items():
                    _tag_buf += ' %s=%s' %(k, v)
                _tag_buf += '\n'

            #print _query_result
            _ut = last
            last += __period #keep while looping until end of time

            if len(_query_result) < 1 or (len(_query_result[0]['dps'].keys())) < 1 : #operation rate 체크
                #here to process None metric
                #원본 메트릭 읽기, 값이 없으면, 1로 입력, 0인것도 값이 있으므로 해당 안됨
                #원본 메트릭에 0 또는 다른 값(정상값, outlier 값) 이 있으면 무시
                #outlier 값과 0 측정값은 비슷한 성격으로 분류, 정의한 것임
                _q_original = tsdb_query(query, start, mid, metric_ref, modem, modem_holiday)
                if len(_q_original) < 1 or len(_q_original[0]['dps'].keys()) < 1 : # 데이터 없음
                    sockWriteTSD( sock, __wm, int(_ut), 1, _tag_buf)
                else:
                    print " \n data exits"
            else:
                print "\n operation mark"

        sock.close()


def cp_metric(__url, __wm, __v, __st, __et, __period=900): # not yet ... in init devel status

    host  = '125.140.110.217'                                        # get할 url
    port  = 4242                                                     # get할 port 번호
    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)        # opentsdb에서 get할 url 주소
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port)  # opentsdb에서 put할 url 주소
    t_first = __st                                                   # get 시작일
    t_end  = __et                                                    # get 종료일
    metric_in   = 'none:rc06_operation_rate_v5'                      # get할 metric명
    #metric_out = 'rc05_none_dp_v1'                                  # put할 metric명
    metric_ref  = 'none:rc04_simple_data_v3'                         # get할 metric명

    chk_number = 0                                                   # outlier 갯수 num
    #modem_list = in_list.total_vlist
    modem_list = in_list.modem_list
    modem_count = 0                             # lte 처리 갯수

    chk_day = '2017/01/01-00:00:00'

    cnt = 0
    loop = 0
    dt = datetime.datetime.strptime(__st, '%Y/%m/%d-%H:%M:%S')
    __st_unix = time.mktime(dt.timetuple())
    dt = datetime.datetime.strptime(__et, '%Y/%m/%d-%H:%M:%S')
    __et_unix = time.mktime(dt.timetuple())
    end = __et_unix
    #last = 1464739200 #2016/07/01, second scale
    #end = 1464739800
    #end = 1509494400 #2017/11/01, second scale, 1498834800 17/7/1
    #last = 1468060199

    mcount = 0
    xlist = modem_list
    
    for modem in modem_list:
        last = __st_unix
        mcount += 1
        pout = "  \n"
        sys.stdout.write(pout)
        # 가끔 서버 다운으로 정지되었을때, 정지 지점부터 다시 시작
        #if modem_list.index(modem) < 0: continue

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        while (last < end):

            start = datetime.datetime.fromtimestamp(int(last)).strftime('%Y/%m/%d-%H:%M:%S')
            mid = datetime.datetime.fromtimestamp(int(last)).strftime('%Y/%m/%d-%H:%M:%S')

            mid = datetime2str(str2datetime(dt_str) + datetime.timedelta(1))

            pout = "  >>  %d / 445, modem: %s last: %d, end: %d, %s %s \r" %(mcount, modem, last, end, start,mid)
            sys.stdout.write(pout)
            sys.stdout.flush()

            modem_holiday = is_weekend(start)
            _query_result = tsdb_query(query, start, mid, metric_in, modem, modem_holiday)

            if (last == __st_unix ) : # 처음 한번만 tag를 읽어 들임, 메트릭 write 에 사용함
                _ret = tsdb_query(query, start, chk_day, metric_in, modem, modem_holiday)
                __tag = _ret[0]['tags']
                #{u'load': u'none', u'building': u'factory', u'modem_num': u'01224230496',
                #u'company': u'middlecompany', u'detail': u'food', u'device_type': u'led', u'holiday': u'0', u'_mds_id': u'00-250130380'}
                _tag_buf = ''
                for k,v in __tag.items():
                    _tag_buf += ' %s=%s' %(k, v)
                _tag_buf += '\n'

            #print _query_result
            _ut = last
            last += __period #keep while looping until end of time

            if len(_query_result) < 1 or (len(_query_result[0]['dps'].keys())) < 1 :
                #here to process None metric
                #원본 메트릭 읽기, 값이 없으면, 1로 입력, 0인것도 값이 있으므로 해당 안됨
                #원본 메트릭에 0 또는 다른 값(정상값, outlier 값) 이 있으면 무시
                #outlier 값과 0 측정값은 비슷한 성격으로 분류, 정의한 것임
                _q_original = tsdb_query(query, start, mid, metric_ref, modem, modem_holiday)
                if len(_q_original) < 1 or len(_q_original[0]['dps'].keys()) < 1 : # 데이터 없음
                    sockWriteTSD( sock, __wm, int(_ut), 1, _tag_buf)
                else:
                    print " \n data exists "

        sock.close()

def sockWriteTSD(sock, __wmetric, __utime, __value, __tags = None):

    if __tags == None: __tags = 'ops=copy'

    _buf = "put %s %s %s %s\n" %( __wmetric, __utime, __value, __tags)
    print _buf
    
    try:
        ret = sock.sendall(_buf)
    except:
        print " something wroing in socket send function"
        pass
    time.sleep(0.0001)
    #pout = "  .... writing to TSDB, return(%s), cmd(%s) \r \r" %(ret, _buf)
    #sys.stdout.write(pout)
    #sys.stdout.flush()

    return


# outlier log 기록함수
def Chk_Outlier(chk_num, outlier_txt_name, adj_modem_num, mds_id,unix_time, value):
    if chk_num == 1:
        f = open(outlier_txt_name, 'w')    # 경로설정 / 덮어쓰기
        f.write('%d:\n' % chk_num)
        f.write('modem_num : %s\n' % adj_modem_num)
        f.write('_mds_id   : %s\n' % mds_id)
        f.write('unix_time : %s\n' % ts2datetime(unix_time))
        f.write('value     : %s\n' % value)
        f.write('\n')
        f.close()
    else:
        f = open(outlier_txt_name, 'a')    # 경로설정 / 이어쓰기
        f.write('%d:\n' % chk_num)
        f.write('modem_num : %s\n' % adj_modem_num)
        f.write('_mds_id   : %s\n' % mds_id)
        f.write('unix_time : %s\n' % ts2datetime(unix_time))
        f.write('value     : %s\n' % value)
        f.write('\n')
        f.close()

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

if __name__ == '__main__':

    __url  = '125.140.110.217'                                       # get할 url
    port  = 4242                                                    # get할 port 번호
#    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)       # opentsdb에서 get할 url 주소
#    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
#    __st = '2016/07/09-00:00:00'                                   # get 시작일
#    __et  = '2016/07/12-00:00:00'                                   # get 종료일
#    2016/07/09-19:59:55, 2016/07/09-20:00:10

    __st = '2016/07/01-00:00:00'                                   # get 시작일
    __et = '2017/07/01-00:00:00'                                   # get 종료일

    #metric_in  = 'none:rc05_excel_copy_tag_v5'                    # get할 metric명
    __wm = 'rc05_none_dp_v10'                                      # put할 metric명
    __v = None

    find_none_dp(__url, __wm, __v, __st, __et, 900)
    exit("....ending main")
