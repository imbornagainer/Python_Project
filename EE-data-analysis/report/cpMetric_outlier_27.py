# -*- coding: utf-8 -*-

# Author : hwijinkim , https://github.com/jeonghoonkang

# outlier를 제거하기 위한 class
# last modified by 20171119

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
import in_list

USE_HTTP_API_PUT = False
debug_val = 1 # if 1, does not insert to TSDB, just print out

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


# 제일 앞쪽 outlier 를 txt 파일로 정보 저장하기 위해, lte 번호를 기억하는 if 조건
_outlier_lte = None

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
            print 'time sleep 5second'
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

    packed_data = pack_dps(metric, dps, tags)
    __lteid = tags['modem_num']

    for dp in packed_data:
        # outlier 조건 설정 , Execel 파일에서 목표수치 max, min 확인하여 설정
        if (dp['value'] != 0 and dp['value'] != None and dp['value'] > 0.001 and dp['value'] <= 200.0):
            if len(send) >= 1024:
                global debug_val
                if debug_val ==0 : sock.sendall(send)

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
            count += 1
        else: # it is outlier && check process if _outlier_lte is changed
            global _outlier_lte
            global chk_number
            if (_outlier_lte != __lteid) :
                _outlier_lte = __lteid
                chk_number = (chk_number + 1)
                Chk_Outlier(chk_number, outlier_txt_name, dp['tags']['modem_num'], dp['tags']['_mds_id'], dp['timestamp'], dp['value']) # outlier log 기록함수

    if len(send) > 0:
        global debug_val
        if debug_val ==0 : sock.sendall(send)
        #if file: file.write(send)
        send = ''

    sock.close()
    pout = 'put dps: {0} processed... \r '.format(count)
    sys.stdout.write(pout)
    sys.stdout.flush()
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
    # 1. 설정값 입력 - 시작
    host  = '125.140.110.217'                                       # get할 url
    port  = 4242                                                    # get할 port 번호
    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)       # opentsdb에서 get할 url 주소
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
    first = '2016/07/01-00:00:00'                                   # get 시작일
    last  = '2017/07/01-00:00:00'                                   # get 종료일
    metric_in  = 'none:rc05_excel_copy_tag_v5'                      # get할 metric명
    metric_out = 'rc05_operation_rate_v6'                           # put할 metric명
    outlier_txt_name = '_d_outlier_list_last.txt'               # outlier log를 저장할 txt명
    # 설정 - 끝

    chk_number = 0                                                  # outlier 갯수 num

    # 2. get할 metric에서 가져올 특정 list 설정
    modem_list = in_list.total_vlist

    
    print '<총 {0!r}개의 Modem list 데이터 추출>\n'.format(len(modem_list))

    modem_count = 0                             # lte 처리 갯수
    start_time = datetime.datetime.now()        # 프로그램 시작값

    #3. 입력된 lte_list를 for문으로 하나씩 get함
    #4. get한 값을 put함
    #5. 반복적으로 get & put 마지막 list까지
    ### 시작일 ~ 끝일까지 하루 data씩 get & put (get data 많으면 opentsdb가 timeout될 수 있기 때문에)
    for modem in modem_list:
        #modem = str(modem)[2:-2]
        #print modem
        #iterate every days and must be started w/ start of the day
        tmp_time = datetime.datetime.now()
        end = first

        while is_past(end, last):
            start = end
            end = add_time(start, days=1)
            modem_holiday = is_weekend(start)
            query_result = tsdb_query(query, start, end, metric_in, modem, modem_holiday)
            for group in query_result:
                if USE_HTTP_API_PUT:
                    tsdb_put(put, metric_out, group['dps'], modem, out_file)
                else:
                    tsdb_put_telnet(host, port, metric_out, group['dps'], group['tags'], '' ,outlier_txt_name)

        modem_count += 1
        print 'elapsed time: {0!s}, {1!s}'.format(datetime.datetime.now() - tmp_time, datetime.datetime.now() - start_time)
        print '<총 {0!r}/{1!r}개의 Modem 데이터 처리>\n'.format(modem_count, len(modem_list))
    print 'total elapsed time: {0!s}'.format(datetime.datetime.now() - start_time)
