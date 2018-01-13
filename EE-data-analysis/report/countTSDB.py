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
sys.path.insert(0, '../lib')
import in_list
import useTSDB
sys.path.insert(0, '../lib/tools')
#import ledinfotest
#import xlsxwriter
#import re
import max_dict
from tsdb_tool import tsdb, esc


def parse_args():

    story = 'OpenTSDB needs many arguments URL, start time, end time, port '
    usg = '\n python tsdb_read.py  -url x.x.x.x -port 4242 -start 2016110100 -end 2016110222 -m metric_name, -wm write_metric_name --help for more info'
    parser=argparse.ArgumentParser(description=story, usage=usg, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-url",    default="125.140.110.217", help="URL input, or run fails")
    parser.add_argument("-start",  default=None, help="start time input, like 2016110100")
    parser.add_argument("-end",    default=None, help="end time input, like 2016110223")
    parser.add_argument("-port",   default=4242, help="port input, like 4242")
    parser.add_argument("-recent", default=None, help="Time input for recent value")
    parser.add_argument("-rdm", default=None, help="metric ")
    parser.add_argument("-val", default=None, help="value ")
    parser.add_argument("-wtm", default=None, help="write-metric ")
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

def sockWriteTSD(__wmetric, __utime, __value, __tags = None):

    if __tags == None: __tags = 'ops=copy'

    _buf = "put %s %s %s %s\n" %( __wmetric, __utime, __value, __tags)

    ret = sock.sendall(_buf)
    pout = "  .... writing to TSDB, return(%s), cmd(%s) \r \r" %(ret, _buf)
    sys.stdout.write(pout)
    sys.stdout.flush()

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
        param['m'] += tag + '={0!s}'.format(tags[tag])
        if i < len(tags) - 1:
            param['m'] += ','
    param['m'] += '}'

    if 1:
        print api_query, param
        response = requests.get(api_query, params=param)
        if response.ok:
            return response.json()
        else:
            return []

if __name__ == "__main__":
    u, p, stime, etime, recent, metric, write_metric, val = parse_args()

    inlist = in_list.total_vlist

    maxdict = dict()
    maxdict = in_list.max_dict
    print len(inlist)

    ret = countall(u, metric, stime, etime, inlist)

    outfile = metric
    of = open (outfile+'_count.txt', 'w+')
    of.write(metric+'=')
    of.write(str(ret))
    of.close()
