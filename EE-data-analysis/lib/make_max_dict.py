# -*- coding: utf-8 -*-
# Author : hwijinkim , https://github.com/jeonghoonkang

# max_value를 찾고, 이에대한 max_value를 .py로 저장하기 위한 class
# last modified by 20171106

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import copy
import numpy as np
import datetime
import time
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
#
# def tsdb_put(put, metric, dps, tags, file=None):
#     packed_data = pack_dps(metric, dps, tags)
#     for i in xrange(0, len(packed_data), 8):
#         tmp = json.dumps(packed_data[i:i+8])
#         #print tmp
#         if 0:
#             response = requests.post(put, data=tmp)
#         if response.text: print response.text
#         else:
#             try:
#                 response = requests_retry_session().post(put, data=tmp, timeout=5)
#             except Exception as x:
#                 print 'requests timeout'
#             else:
#                 if response.text: print response.text
#     return

def Find_MaxValue(metric, dps, tags):
    packed_data = pack_dps(metric, dps, tags)
    #print 'packed_data : %s' % packed_data
    global max_value

    for dp in packed_data:
        #print 'dp : %s' % dp
        if max_value < dp['value']:
            max_value = dp['value']

# MaxValue 기록함수
def Write_MaxValue(max_dict):
        f = open('_d_max_dict_last.py', 'w')    # 경로설정 / 덮어쓰기
        f.write('max_value = { %s }' % max_dict)
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
    first = '2016/07/01-00:00:00'                                   # get 시작일
    last  = '2017/07/01-00:00:00'                                   # get 종료일
    metric_in  = 'none:rc05_excel_copy_tag_v5'               # get할 metric명
    #metric_in  = 'sum:rc04_simple_data_v3'
    chk_number = 0                                                  # outlier 횟수
    save_outlier = 0.0
    max_dic = ''
    max_value = 0.0

    # 2. get할 metric에서 가져올 특정 list 설정
    modem_list = in_list.total_vlist
    print '<총 {0!r}개의 Modem list 데이터로 max 값 dict 생성 시작>\n'.format(len(modem_list))

    modem_count = 0                             # lte 처리 갯수
    start_time = datetime.datetime.now()        # 프로그램 시작값

    # 3. 입력된 list를 for문으로 하나씩 get함
    # 4. get한 list에서 얻은 한달치 value값을 비교
    # 5. 설정한 outlier값과 같거나 이상일시 txt로 log기록 및 print 출력
    ### 시작일 ~ 끝일까지 하루 data씩 get (get data 많으면 opentsdb가 timeout될 수 있기 때문에)
    for modem in modem_list:
        print modem
        #iterate every days and must be started w/ start of the day
        tmp_time = datetime.datetime.now()
        end = first
        while is_past(end, last):
            start = end
            end = add_time(start, days=1)
            modem_holiday = is_weekend(start)
            query_result = tsdb_query(query, start, end, metric_in, modem, modem_holiday)
            for group in query_result:
                Find_MaxValue(metric_in, group['dps'], group['tags'])
        max_dic += "'%s': %f, " % (modem, max_value)
        #print 'max_dic : %s' % max_dic
        max_value = 0.0
        modem_count += 1
        print 'elapsed time: {0!s}, {1!s}'.format(datetime.datetime.now() - tmp_time, datetime.datetime.now() - start_time)
        print '<총 {0!r}/{1!r}개의 Modem 데이터 처리>\n'.format(modem_count, len(modem_list))
    if (max_dic != ''):       # max_value가 빈값이 아니면 py로 저장
        Write_MaxValue(max_dic) # outlier log 기록함수
        print 'max dic 작성완료!'
    print 'total elapsed time: {0!s}'.format(datetime.datetime.now() - start_time)
