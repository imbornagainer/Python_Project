# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import socket
import copy
from openpyxl import load_workbook
import numpy as np
import datetime
import time
import gzip
import shutil

import sys
sys.path.insert(0, 'C:\Users\Be Pious\git\kdatahub\EE-data-analysis\lib')

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

def tsdb_query(query, start, end, metric, tag_kind, tag_value, building):
    param = {}
    if start: param['start'] = start
    if end: param['end'] = end
    param['m'] = metric + '{' + tag_kind + '=' + tag_value + ',' + 'detail' + '=' + building +'}'

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
    host  = '125.140.110.217'
    port  = 4242
    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port)
    first = '2016/07/01-00:00:00'
    last  = '2017/07/01-00:00:00'
    metric_in  = 'avg:___d_tag_test_load_rate_4'
    
    #tag_kind = raw_input("get하고 싶은 tag를 입력해주세요.\n\n예시\n--------------------\n1.tag_value\n2.modem_num\n3.mds_id\n4.company\n5.detail\n6.building\n-----------------------\n\n주의사항 숫자가 아닌 tag명을 입력해주세요.\ntag_name: ")
    #tag_value = raw_input("\nget하고 싶은 tag의 value값을 입력해주세요.\ntag_value: ")
    tag_kind = 'device_type'
    tag_value = 'led'
    building = 'building_etc'
    
    if tag_value == '1' or tag_value == 'led':
        tag_value = 'led'
    else:
        tag_value = 'fceramic'
    
    dps_sum = 0.0
    load_rate = 0.0
    
    query_result = tsdb_query(query, first, last, metric_in, tag_kind, tag_value, building)    
    for group in query_result:
        for i in group['dps'].values():
            dps_sum += i

    #base_num = (393.0 * 35040) / 35040
    #load_rate = (dps_sum / (base_num * 35040)) * 100
    load_rate = (dps_sum / 35040)
    
    print '\n'
    print round(load_rate, 2)
