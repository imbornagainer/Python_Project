# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import socket
import copy
import numpy as np
import datetime
import time

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

def tsdb_query(query, start, end, metric, modem_num):
    param = {}
    if start: param['start'] = start
    if end: param['end'] = end
    param['m'] = metric + '{' + 'modem_num={0!s}'.format(modem_num) + '}'
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

def tsdb_put_telnet(host, port, metric, dps, tag, load, holiday, file='False'):
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
    #print 'put dps: {0} requested...'.format(len(dps))
    
    tags = {    # 받은 tag를 원하는 모양으로 가공
        "holiday": holiday,
        "_mds_id": tag['_mds_id'],
        "modem_num": tag['modem_num'],
        "load": load
    }
    
    packed_data = pack_dps(metric, dps, tags)
    for dp in packed_data:
        if (dp['value'] < 101.0):   # 100이하인 값만 put, 아닌 값은 outlier로 간주 txt로 log저장
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
            send += ' {0!r}'.format(dp['value'])
            #print 'dp : %s' % dp
            if 'tags' in dp:
                for key in dp['tags']:
                    #print 'key : %s' % key
                    send += ' {0!s}'.format(key) + '={0!s}'.format(dp['tags'] [key])
            send += '\n'
            count += 1
        else:
            global chk_number
            chk_number = (chk_number + 1)
            Chk_Outlier(chk_number, dp['tags']['modem_num'], dp['tags']['_mds_id'], dp['timestamp'], dp['value']) # outlier log 기록함수
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
    # 1. 설정값 입력 - 시작
    host  = '125.140.110.217'                                       # get할 url
    port  = 4242                                                    # get할 port 번호
    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)       # opentsdb에서 get할 url 주소
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
    first = '2016/07/01-00:00:00'                                   # get 시작일
    last  = '2016/07/02-00:00:00'                                   # get 종료일
    metric_in  = 'none:oracledb에서 추가한 metric명'                # get할 metric명
    #metric_in  = 'sum:rc04_simple_data_v3'                
    metric_out = 'metric명 정하기'                                  # put할 metric명
    #metric_out = 'RazaTheChained_v4'
    # 설정값 입력 - 끝
    chk_number = 0                                                  # outlier 횟수
    
    # 2. get할 metric에서 가져올 특정 list 설정    
    load_list = ['01220800653', '01220824131', '01220800754', '01220435097', '01220674104', '01224224145', '01220674127', '01220824133', '01220435017', '01224230474', '01220435137', '01220435096', '01220800670', '01220800666', '01220434991', '01220474138', '01224230503', '01220674054', '01224224148', '01224230475', '01224224146', '01224224137', '01220674137', '01220674059', '01220800665', '01220674126', '01220435087', '01220674124', '01220674132', '01220800616', '01220674131', '01220800605', '01220800760', '01220674072', '01220674143', '01220435120', '01220800759', '01220674158', '01220800639', '01220674148', '01220674057', '01220435112', '01220674074', '01220435048', '01220674092', '01220800673', '01220674097', '01220800667', '01220674063', '01220800725', '01224230497', '01220674129', '01220674103', '01220800629', '01224224126', '01224224143', '01224224147', '01224230492', '01220674066', '01224230462', '01224230498', '01220674091', '01220674158', '01220800715', '01220674062', '01220674068', '01220435110', '01220435075', '01220824145', '01222718541', '01222699985', '01222649986 ', '01222789985 ', '01222669984', '01222598541 ', '01222677452', '01222699541', '01222799989', '01222749987 ', '01222789987', '01222577541 ', '01222708541', '01222726543', '01222731541', '01222744759', '01222719985', '01222671541 ', '01222628541', '01222757452', '01222627543', '01222588541 ', '01222709987 ', '01222649989', '01222729984']
    load_list_json = [{'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01220800653'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01220824131'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220800754'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220435097'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01220674104'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01224224145'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220674127'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220824133'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220435017'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01224230474'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01220435137'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01220435096'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220800670'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220800666'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01220434991'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01220474138'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01224230503'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220674054'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01224224148'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01224230475'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01224224146'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01224224137'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01220674137'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01220674059'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220800665'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220674126'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01220435087'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01220674124'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220674132'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220800616'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01220674131'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01220800605'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220800760'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220674072'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01220674143'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01220435120'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220800759'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220674158'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01220800639'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01220674148'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220674057'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220435112'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220674074'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220435048'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01220674092'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01220800673'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220674097'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220800667'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220674063'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220800725'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01224230497'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01220674129'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220674103'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220800629'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01224224126'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01224224143'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01224224147'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': 'none'}, {'load': 'turbo_cold', 'holiday': '0', 'modem_num': '01224230492'}, {'load': 'pump_cold', 'holiday': '0', 'modem_num': '01220674066'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01224230462'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01224230498'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220674091'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220674158'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220800715'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220674062'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220674068'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220435110'}, {'load': 'cold_hot_dispensers', 'holiday': '0', 'modem_num': '01220435075'}, {'load': 'cold_hot_pump', 'holiday': '0', 'modem_num': '01220824145'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222718541'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222699985'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222649986 '}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222789985 '}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222669984'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222598541 '}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222677452'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222699541'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222799989'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222749987 '}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222789987'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222577541 '}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222708541'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222726543'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222731541'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222744759'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222719985'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222671541 '}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222628541'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222757452'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222627543'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222588541 '}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222709987 '}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222649989'}, {'load': 'ehp', 'holiday': '0', 'modem_num': '01222729984'}]
    print '<총 {0!r}개의 Load list 데이터 추출>\n'.format(len(load_list))
    
    modem_count = 0                             # lte 처리 갯수
    start_time = datetime.datetime.now()        # 프로그램 시작값

    #3. 입력된 lte_list를 for문으로 하나씩 get함
    #4. get한 값을 put함
    #5. 반복적으로 get & put 마지막 list까지
    ### 시작일 ~ 끝일까지 하루 data씩 get & put (get data 많으면 opentsdb가 timeout될 수 있기 때문에)
    for modem in load_list_json:
        #iterate every days and must be started w/ start of the day
        tmp_time = datetime.datetime.now()
        end = first
        while is_past(end, last):
            start = end
            end = add_time(start, days=1)
            modem_holiday = is_weekend(start)
            query_result = tsdb_query(query, start, end, metric_in, modem['modem_num'])
            
            for group in query_result:
                if USE_HTTP_API_PUT:
                    tsdb_put(put, metric_out, group['dps'], group['tags'], out_file)
                else:
                    tsdb_put_telnet(host, port, metric_out, group['dps'], group['tags'], modem['load'], modem_holiday)
        modem_count += 1
        print 'elapsed time: {0!s}, {1!s}'.format(datetime.datetime.now() - tmp_time, datetime.datetime.now() - start_time)
        print '<총 {0!r}/{1!r}개의 Modem 데이터 처리>\n'.format(modem_count, len(modem_list))
    print 'total elapsed time: {0!s}'.format(datetime.datetime.now() - start_time)
    