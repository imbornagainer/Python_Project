# -*- coding: utf-8 -*-
# Author : hwijinkim , https://github.com/jeonghoonkang

# max_value로 가동률 계산, 그리고 계산한 값을 다른 metric에 put 
# last modified by 20171106

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
sys.path.insert(0, '/home/bornagain/kdatahub/EE-data-analysis/lib')
sys.path.insert(0, 'C:\Users\Be Pious\git\kdatahub\EE-data-analysis\lib')
import in_list

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

def tsdb_put_telnet(host, port, metric, dps, tag, g_tag, file='False'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    retry = 9999
    
    tags = {    # 받은 tag를 원하는 모양으로 가공
        "holiday": g_tag['holiday'],
        "_mds_id": g_tag['_mds_id'],
        "modem_num": g_tag['modem_num'],
        "load": tag['load'],
    }
    
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
    #print 'put dps: {0} requested...'.format(len(dps))
    
    packed_data = pack_dps(metric, dps, tags)

    for dp in packed_data:
        if len(send) >= 1024:
            #print send + '\n\n'
            sock.sendall(send)
            #if file: file.write(send)
            send = ''
        try:
            send += 'put'
            send += ' {0!s}'.format(dp['metric'])
            send += ' {0!r}'.format(dp['timestamp'])
            send += ' {0!r}'.format(dp['value'])   # 최대값으로 가동율 구하는 공식 (dps/최대값) * 100
        except:
            continue
        else:
            if 'tags' in dp:
                for key in dp['tags']:
                    #print 'key : %s' % key
                    send += ' {0!s}'.format(key) + '={0!s}'.format(dp['tags'] [key])
            send += '\n'
            count += 1
    #print 'send : ' + send
    if len(send) > 0:
        #print send + '\n\n'
        sock.sendall(send)
        #if file: file.write(send)
        send = ''
    sock.close()
    #print 'put dps: {0} processed...'.format(count)
    return

# outlier log 기록함수
# open의 경로명을 설정해주어야 한다.
def Chk_Outlier(chk_num, adj_modem_num,mds_id,unix_time, value):
    if chk_num == 1:
        f = open('outlier_lists_171102_modem_v1.txt', 'w')    # 경로설정 / 덮어쓰기
        f.write('%d:\n' % chk_num)
        f.write('modem_num : %s\n' % adj_modem_num)
        f.write('_mds_id   : %s\n' % mds_id)
        f.write('unix_time : %s\n' % ts2datetime(unix_time))
        f.write('value     : %s\n' % value)
        f.write('\n')
        f.close()
    else:
        f = open('outlier_lists_171102_modem_v1.txt', 'a')    # 경로설정 / 이어쓰기
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
    # 1. 설정값 입력
    host  = '125.140.110.217'                                       # get할 url
    port  = 4242                                                    # get할 port 번호
    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)       # opentsdb에서 get할 url 주소
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
    first = '2016/07/01-00:00:00'                                   # get 시작일
    last  = '2017/07/01-00:00:00'                                   # get 종료일
    metric_in  = 'none:rc04_simple_cool_v1'               # get할 metric명
    #metric_in  = 'sum:rc04_simple_data_v3'
    metric_out = 'rc04_cool_tag_v2'                            # put할 metric명
    #metric_out = 'RazaTheChained_v4'
    chk_number = 0                                                  # outlier 횟수    

    # 2. get할 metric에서 가져올 특정 list 설정    
    print '<총 {0!r}개의 Modem list 데이터 추출>\n'.format(len(in_list.coolboil_list_json))
    
    modem_count = 0                             # lte 처리 갯수
    start_time = datetime.datetime.now()        # 프로그램 시작값

    #3. 입력된 lte_list를 for문으로 하나씩 get함
    #4. get한 값을 put함
    #5. 반복적으로 get & put 마지막 list까지
    ### 시작일 ~ 끝일까지 하루 data씩 get & put (get data 많으면 opentsdb가 timeout될 수 있기 때문에)
    for modem in in_list.coolboil_list_json:
        #iterate every days and must be started w/ start of the day
        tmp_time = datetime.datetime.now()
        end = first
        while is_past(end, last):
            start = end
            end = add_time(start, days=1)
            modem_holiday = is_weekend(start)
            query_result = tsdb_query(query, start, end, metric_in, modem['modem_num'], modem_holiday)
            for group in query_result:
                if USE_HTTP_API_PUT:
                    tsdb_put(put, metric_out, group['dps'], modem, out_file)
                else:
                    tsdb_put_telnet(host, port, metric_out, group['dps'], modem, group['tags'])
        modem_count += 1
        print 'elapsed time: {0!s}, {1!s}'.format(datetime.datetime.now() - tmp_time, datetime.datetime.now() - start_time)
        print '<총 {0!r}/{1!r}개의 Modem 데이터 처리>\n'.format(modem_count, len(in_list.coolboil_list))
    print 'total elapsed time: {0!s}'.format(datetime.datetime.now() - start_time)
    