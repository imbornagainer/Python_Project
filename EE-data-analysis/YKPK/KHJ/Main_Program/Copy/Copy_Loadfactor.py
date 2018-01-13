# -*- coding: utf-8 -*-
# Author : hwijinkim , https://github.com/jeonghoonkang

# openTSDB를 사용하기 위한 class
# last modified by 20171228

import time
import datetime
import requests
import json
import argparse
import urllib2
import socket
from operator import itemgetter, attrgetter

import sys
sys.path.insert(0, '/home/bornagain/kdatahub/EE-data-analysis/lib')
sys.path.insert(0, 'C:\Users\Be Pious\git\kdatahub\EE-data-analysis\lib')

import in_list
sys.path.insert(0, '/home/bornagain/kdatahub/EE-data-analysis/lib/tools')
sys.path.insert(0, 'C:\Users\Be Pious\git\kdatahub\EE-data-analysis\lib\tools')

HOST = '125.140.110.217'
PORT = 4242
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def parse_args():

    story = 'OpenTSDB needs many arguments URL, start time, end time, port '
    usg = '\n python tsdb_read.py  -url x.x.x.x -port 4242 -start 2016110100 -end 2016110222 -m metric_name, -wm write_metric_name --help for more info'
    parser=argparse.ArgumentParser(description=story, usage=usg, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-url",    default="125.140.110.217", help="URL input, or run fails")
    parser.add_argument("-start",  default='2016070100', help="start time input, like 2016110100")
    parser.add_argument("-end",    default='2017070100', help="end time input, like 2016110223")
    parser.add_argument("-port",   default='4242', help="port input, like 4242")
    parser.add_argument("-recent", default='True', help="Time input for recent value")
    parser.add_argument("-rdm", default='rc06_ld_rate_v2', help="metric ")
    parser.add_argument("-val", default=None, help="value ")
    parser.add_argument("-wtm", default='rc06_ld_rate_v3_test', help="write-metric ")
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

    m = args.rdm
    if m == None : print("... this time will not use READ function")

    wm = args.wtm
    if m == None and wm == None :
        print usg
        exit("... I can not do anything without metric")

    return url, port, start, end, recent, m, wm, args.val
        
def is_past(dt_str1, dt_str2):
    return datetime2ts(dt_str1) < datetime2ts(dt_str2)

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

def is_weekend(dt_str):
    if str2datetime(dt_str).weekday() >= 5: return '1'
    else: return '0'
    
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

def insert_ld_rate(__url, __m, __wm, devlist, __st, __et, data_json, season=''):
    cnt =0
    loop = 0

    st = datetime.datetime.strptime(__st, "%Y/%m/%d-%H:%M:%S")
    et = datetime.datetime.strptime(__et, "%Y/%m/%d-%H:%M:%S")
    first = st.strftime('%Y/%m/%d-%H:%M:%S')
    last = et.strftime('%Y/%m/%d-%H:%M:%S')
    
    for dev in data_json:
        #rate_result = query(start, end, 'none:rc05_operation_rate_v6', {'modem_num': dev})
        # none aggregation 은 holiday 를 구분해서 읽어옴. 이런경우. holiday 태그 두개에 대해서 다 앍어야 함
        # 그래서 읽는 방법을 변경함. count 로.
        ## led, tags,building

        tag_list = data_json[dev]['tags']

        for key in tag_list:                    # key is total, buildlng.... or
            for k,v in tag_list[key].items():   # tag --> building.office etc
                qtag = {}
                qtag['device_type'] = dev
                qtag[key] = k

                end = first
                while is_past(end, last):
                    cnt += 1
                    start = end
                    end = add_time(start, days=1)
                    holiday = '0'

                    holiday = is_weekend(start)

                    #리딩할 태그를 구성한다
                    if k == 'total':
                        qtag = {'device_type':dev}
                    if k == 'each': continue

                    wtag = ''
                    for wtag_k, wtag_v in qtag.items():
                        wtag += ' %s=%s' % (wtag_k,wtag_v)
    
                    if len(qtag.keys()) == 1 :
                        wtag += ' %s=%s' % ('totcount','total')
                    wtag += ' \n'
                
                    value_result = query(start, end, 'avg:'+__m ,qtag)
                    if value_result == '[]' or len(value_result) < 1 : continue
                    
                    v_dict = value_result[0]    # rate 값

                    _tag = ''
                    for k,v in v_dict['tags'].items():
                        if k == '_mds_id':continue                            
                        _tag += ' %s=%s' % (k,v)
                    _tag += ' %s=%s' % ('holiday',holiday)
                    if season != '':
                        _tag += ' %s=%s' % ('season',season)

                    try:
                        for k, v in v_dict['dps'].items():
                            sockWriteTSD(__wm, k, v, _tag)
                    except KeyError , e:
                        print e
                        pass
                    
    print '몇번째 : %s' % cnt

def sockWriteTSD(__wmetric, __utime, __value, __tags = None):

    if __tags == None: __tags = 'ops=copy'

    _buf = "put %s %s %s %s\n" %( __wmetric, __utime, __value, __tags)
    print _buf
    
    ret = sock.sendall(_buf)
    pout = "  .... writing to TSDB, return(%s), cmd(%s) \r \r" %(ret, _buf)
    sys.stdout.write(pout)
    sys.stdout.flush()

    return

def run(u, metric, write_metric, inlist, stime, etime, data_json):
 
    start = '2016/07/01-00:00:00'
    end = '2017/07/01-00:00:00'
    ret = insert_ld_rate(u, metric, write_metric, inlist, start, end, data_json)

    start = '2016/07/01-00:00:00'
    end = '2016/08/01-00:00:00'
    ret = insert_ld_rate(u, metric, write_metric, inlist, start, end, data_json,'summer')

    start = '2016/08/01-00:00:00'
    end = '2016/09/01-00:00:00'
    ret = insert_ld_rate(u, metric, write_metric, inlist, start, end, data_json,'summer')

    start = '2016/09/01-00:00:00'
    end = '2016/10/01-00:00:00'
    ret = insert_ld_rate(u, metric, write_metric, inlist, start, end, data_json,'summer')

    start = '2016/10/01-00:00:00'
    end = '2016/11/01-00:00:00'
    ret = insert_ld_rate(u, metric, write_metric, inlist, start, end, data_json)

    start = '2016/11/01-00:00:00'
    end = '2016/12/01-00:00:00'
    ret = insert_ld_rate(u, metric, write_metric, inlist, start, end, data_json,'winter')

    start = '2016/12/01-00:00:00'
    end = '2017/01/01-00:00:00'
    ret = insert_ld_rate(u, metric, write_metric, inlist, start, end, data_json,'winter')

    start = '2017/01/01-00:00:00'
    end = '2017/02/01-00:00:00'
    ret = insert_ld_rate(u, metric, write_metric, inlist, start, end, data_json,'winter')

    start = '2017/02/01-00:00:00'
    end = '2017/03/01-00:00:00'
    ret = insert_ld_rate(u, metric, write_metric, inlist, start, end, data_json,'winter')
    
    outfile = metric
    of = open (outfile+'_ld_rate_season_1213.txt', 'w+')
    of.write(metric+'=')
    of.write(str(ret))
    of.close()

if __name__ == "__main__":
    u, p, stime, etime, recent, metric, write_metric, val = parse_args()

    choice = input('1 = windows\n2 = linux\n')
    if choice == 1:
        with open('C:/Users/Be Pious/git/kdatahub/EE-data-analysis/lib/tools/count_list.json') as data_file:
            data_json = json.load(data_file)
    else:
        with open('/home/bornagain/kdatahub/EE-data-analysis/lib/tools/count_list.json') as data_file:
            data_json = json.load(data_file)

    inlist = in_list.total_vlist
    print " will prcessing %d lte numbers" %(len(inlist))
    
    run(u, metric, write_metric, inlist, stime, etime, data_json)
    
