# -*- coding: utf-8 -*-
# Author : jeonghoonkang , https://github.com/jeonghoonkang

# openTSDB를 사용하기 위한 class
# last modified by 20171031

import time
import datetime
import os
import requests
import json
import argparse
import calendar
import urllib2
import socket
from operator import itemgetter, attrgetter
import ast
import sys
from numpy.distutils.ccompiler import _m
#sys.path.insert(0, '/home/bornagain/kdatahub/EE-data-analysis/lib')
#sys.path.insert(0, 'C:\Users\Be Pious\git\kdatahub\EE-data-analysis\lib')
sys.path.insert(0, '../../../../lib')

import in_list
#import useTSDB
sys.path.insert(0, '/home/bornagain/kdatahub/EE-data-analysis/lib/tools')
sys.path.insert(0, 'C:\Users\Be Pious\git\kdatahub\EE-data-analysis\lib\tools')
#import ledinfotest
#import xlsxwriter
#import re
#import max_dict
#from tsdb_tool import tsdb, esc
from pprint import pprint

#with open('C:/Users/Be Pious/git/kdatahub/EE-data-analysis/lib/tools/count_list.json') as data_file:
with open('../../../../lib/tools/count_list.json') as data_file:
    data_json = json.load(data_file)

#tag = {'mds-id':'911'}
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
    parser.add_argument("-rdm", default='rc06_operation_rate_v3', help="metric ")
    parser.add_argument("-val", default=None, help="value ")
    parser.add_argument("-wtm", default='rc06_op_rate_v2', help="write-metric ")
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

# 시간사이 데이터 읽기
def ptest(__url, __st, __et, __m):
    tsdbclass = useTSDB.u_ee_tsdb(__url, __st, __et)
    tag = __m
    if (tag == None) : return
    tsdbclass.set_metric(tag)
    print tsdbclass.readTSD()

# 최근 데이터 읽기
def rtest(__url, __m, __tag):
    tsdbclass = useTSDB.u_ee_tsdb(__url, None, None, True)
    tsdbclass.set_metric(__m)
    tag = __tag
    if (tag == None) : return
    print tsdbclass.readTSDrecent(tag, 'sum')

# 특정 시간에 가까운 데이터 읽기
def point(__url, __m, __time, __tag):
    tsdbclass = useTSDB.u_ee_tsdb(__url, __time)
    tsdbclass.set_metric(__m)
    tag = __tag
    if (tag == None) : return
    print tsdbclass.readOnePoint(__time, tag, 'sum')

    cnt = 0
    loop = 0

# 기간동안의 데이터포인트 갯수 리턴
def countall(__url, __m,  __st, __et, __listname):
    tsdbclass = useTSDB.u_ee_tsdb(__url, __st, __et)
    tsdbclass.set_metric(__m)
    cnt = 0
    loop = 0
    dt = datetime.datetime.strptime(__st, "%Y%m%d%H%M")
    __st_unix = time.mktime(dt.timetuple())
    dt = datetime.datetime.strptime(__et, "%Y%m%d%H%M")
    __et_unix = time.mktime(dt.timetuple())
    diff = __et_unix - __st_unix
    unit_num = 1 + int(diff) / (15*60)

    countlist = dict()
    retdict = dict()
    ratedict = dict()
    retdict["description"] = 'count dps number and time unit number, then return as dict'
    retdict['count'] = countlist #dict member
    retdict['rate'] = ratedict #dict member
    retdict['denom'] = unit_num
    retdict['period'] = __st + ' ' + __et

    ids = __listname
    _pos = 0

    for i in ids :
        _pos += 1
        #tsdb에서 데이터 읽어오기
        #인자 (태그, aggregation of openTSDB)
        _buf_dict = tsdbclass.readTSD(i,'zimsum')
        if _buf_dict is None: continue
        for (k, v) in _buf_dict['dps'].items():
            if v > 0.001 : v = 1
            cnt = cnt + v
        countlist[str(i)] = cnt
        r = format(100 * float(cnt) / unit_num, '06.2f')
        ratedict[str(i)] = r

        cnt = 0
        pout = ' progress : ' + '%s/%s \r' %(_pos, len(ids))
        sys.stdout.write(pout)
        sys.stdout.flush()

    return retdict


def insertValue_periodically(__url, __wm, __v, __st, __et, __period=3600):
    cnt = 0
    loop = 0
    dt = datetime.datetime.strptime(__st, "%Y%m%d%H%M")
    __st_unix = time.mktime(dt.timetuple())
    dt = datetime.datetime.strptime(__et, "%Y%m%d%H%M")
    __et_unix = time.mktime(dt.timetuple())
    last = __st_unix
    end = __et_unix
    #last = 1464739200 #2016/07/01, second scale
    #end = 1464739800
    #end = 1509494400 #2017/11/01, second scale

    while (last < end):
        __ut = '%s' %(int(last))
        __v = '%s' %(__v)
        # tag supports 8 tagk and tagv pairs
        __tag = 'type=data'
        sockWriteTSD( __wm, __ut, __v, __tag )
        last += __period
    print " ... insert done "

def cpmetric(__url, __m,  __st, __et, __wm):
    tsdbclass = useTSDB.u_ee_tsdb(__url, __st, __et)
    tsdbclass.set_metric(__m)
    cnt = 0
    loop = 0

    for tagid in ltelist :
        print tagid[0]
        #tsdb에서 데이터 읽어오기
        _buf_dict = tsdbclass.readTSD(tagid[0], 'sum')
        if _buf_dict is None: continue
        for (k, v) in _buf_dict['dps'].items():
            #pair = '%s=%s' % (k, v)
            __ut = '%s' %(k)
            __v = '%s' %(v)
            __qv = '%s' %(3*v/4.0)
            cnt = cnt + v
            loop = loop + 1
            print __ut
            sockWriteTSD( __wm, __ut, __qv, tagid[0] )
            print "processing ....", tagid[0], '>'
        #print  'Total Count of TSDB %s' %__m, 'is', cnt

def GetTheKey(data_json):
    for dev in data_json:  # lte modem number
        print dev

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

def insert_op_rate(__url, __m, __wm, devlist, maxdict, __st, __et, data_json, of):
    cnt =0
    loop = 0
    d_type = 'device_type'
    totcount = ''

    st = datetime.datetime.strptime(__st, "%Y%m%d%H%M")
    et = datetime.datetime.strptime(__et, "%Y%m%d%H%M")
    first = st.strftime('%Y/%m/%d-%H:%M:%S')
    last = et.strftime('%Y/%m/%d-%H:%M:%S')

    dev_count = 0

    for dev in data_json:  # lte modem number
        #rate_result = query(start, end, 'none:rc05_operation_rate_v6', {'modem_num': dev})
        # none aggregation 은 holiday 를 구분해서 읽어옴. 이런경우. holiday 태그 두개에 대해서 다 앍어야 함
        # 그래서 읽는 방법을 변경함. count 로.
        ## led, tags,building

        of.write(dev+'\n')
        #print dev

        end = first
        while is_past(end, last):
            start = end
            end = add_time(start, days=1)

            holiday = is_weekend(start)

            if dev == 'led':
                totcount = 'total'
            else:
                totcount = 'each'

            tag_list = data_json[dev]['tags']

            for key in tag_list: # key is total, buildlng, device_type.... or
                of.write(key+'\n')
                #print key

                for tag in tag_list[key]: # tag --> building.office etc
                    of.write(tag+'\n')
                    #print tag

                    _tag = ''
                    
                    if tag == 'total':
                        rate_result = query(start, end, 'zimsum:rc04_totoal_cnt__002', {d_type: dev})
                        value_result = query(start, end, 'zimsum:'+__m , {d_type: dev})
                    else:
                        rate_result = query(start, end, 'zimsum:rc04_totoal_cnt__002', {d_type: dev, key : tag})
                        value_result = query(start, end, 'zimsum:'+__m , {d_type: dev, key : tag})
                    #print start, end
                    #print rate_result
                    #print value_result
                    #exit()

                    if rate_result == '[]' or len(rate_result) < 1 : continue
                    if value_result == '[]' or len(value_result) < 1 : continue

                    #print rate_result
                    r_dict = rate_result[0]     # none을 뺀 dp값
                    v_dict = value_result[0]    # rate count 값

                    stt = start +'\r'
                    sys.stdout.write(stt)
                    sys.stdout.flush()

                    #tag copy
                    for k, v in v_dict['tags'].items():
                        if k == key:
                            _tag = _tag + "%s=%s %s=%s %s=%s %s=%s" %(k, v, d_type, dev, 'holiday', holiday,'totcount',totcount)
                        try:
                            ut_list = r_dict['dps'].keys()

                            for utt in ut_list:
                                #print utt
                                _m = r_dict['dps'][str(utt)]

                                if v_dict['dps'].has_key(utt):
                                    _v = v_dict['dps'][str(utt)]
                                else:
                                    #print '  __ no key in operatioin_rate dict !!!'
                                    continue

                                #print _v, _m, 'total count'

                                if (_m < 1) :
                                    #print '  ________no total count, which is < 1'
                                    continue

                                _rate = round((1.0 * _v / _m * 100.0), 2)

                                if _rate > 100:
                                    #print '__________________over rate : %s total: %s' % (_rate, _m)
                                    continue

                                #time.sleep(0.001)

                                #pout = ' value=%f, totoal_cnt=%f, rate=%s \n' %(_v, _m, _rate)
                                #sys.stdout.write(pout)
                                #sys.stdout.flush()
                                #print '! ut !: ' + utt + '\r'

                                sockWriteTSD(__wm, utt, _rate, _tag)
                        except KeyError , e:
                            print 'exception num: ' , e
                            pass
                    dev_count = dev_count + 1
        print ( dev_count / len(tag_list[key]) )

def sockWriteTSD(__wmetric, __utime, __value, __tags = None):

    if __tags == None: __tags = 'ops=copy'
    _buf = "put " + __wmetric[:-2] 
    _buf += " %s %s %s\n" %(__utime, __value, __tags)
    #print _buf

    ret = sock.sendall(_buf)
    #pout = "  %s \r " %(_buf[:-2])
    #sys.stdout.write(pout)
    #sys.stdout.flush()

    return

def query(start, end, metric, tags):

    host = '125.140.110.217'
    port = 4242
    api_query = 'http://{0!s}:{1!r}/api/query'.format(host,port)
    param = {}

    if start: param['start'] = start
    if end: param['end'] = end

    param['m'] = metric + '{'
    for i, tag in enumerate(tags):
        #print i, tag
        param['m'] += tag + '={0!s}'.format(tags[tag])
        if i < len(tags) - 1:
            param['m'] += ','
    param['m'] += '}'

    if 1:
        #print api_query, param
        response = requests.get(api_query, params=param)
        #print response
        if response.ok:
            return response.json()
        else:
            return []

if __name__ == "__main__":
    u, p, stime, etime, recent, metric, write_metric, val = parse_args()

    inlist = in_list.total_vlist
    print " will prcessing %d lte numbers" %(len(inlist))
    maxdict = dict()
    maxdict = in_list.max_dict

    #print pprint(data['led']['tags']['building']) #data는 json 전체를 dictionary 형태로 저장하고 있음
    #keys = [key for key in data['led']['tags']['building']] #data는 json 전체를 dictionary 형태로 저장하고 있음

    outfile = metric
    of = open (outfile+'_opertaion_rate_1210.txt', 'w+')
    of.write(metric+'=')
    
    print "start time = %s" %stime
    print "end time = %s" %etime

    ret = insert_op_rate(u, metric, write_metric, inlist, maxdict, stime, etime, data_json, of)
    #insert_load_rate(u, metric, write_metric, inlist, maxdict, stime, etime)

    of.write(str(ret))
    of.close()