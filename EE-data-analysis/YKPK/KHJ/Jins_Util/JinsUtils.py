# -*- coding: utf-8 -*-
# Author : hwijinkim https://github.com/imbornagainer/MyProject

#===============================================================================
# 모든 def를 모아놓은 Lib source 입니다.
# 필요하신 def를 사용하시어 간단한 source를 구현하실 수 있습니다.
#===============================================================================

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

#===============================================================================
# 데이터를 가공하여 리턴하는 def 시작
#===============================================================================

def parse_args():
    story = 'OpenTSDB needs many arguments URL, start time, end time, port '
    usg = '\n python tsdb_read.py  -url x.x.x.x -port 4242 -start 2016110100 -end 2016110222 -m metric_name, -wm write_metric_name --help for more info'
    parser=argparse.ArgumentParser(description=story, usage=usg, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-url",    default="125.140.110.217", help="URL input, or run fails")
    parser.add_argument("-start",  default='2016070100', help="start time input, like 2016110100")
    parser.add_argument("-end",    default='2017070100', help="end time input, like 2016110223")
    parser.add_argument("-port",   default='4242', help="port input, like 4242")
    parser.add_argument("-recent", default='True', help="Time input for recent value")
    parser.add_argument("-rdm", default='rc06_op_rate_', help="metric ")
    parser.add_argument("-val", default=None, help="value ")
    parser.add_argument("-wtm", default='rc05_daily_opr_v2_testtesttest', help="write-metric ")
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

#===============================================================================
# 데이터를 가공하여 리턴하는 def 끝
#===============================================================================

#===============================================================================
# 엑셀 수정 def 시작
#===============================================================================

def thin_device(row):
    thin = {get_tag_ref('device'): 'none'}
    print "col2num(get_col_ref('led_modem_serial')) : %s" % (col2num(get_col_ref('led_modem_serial')))
    print "row[col2num(get_col_ref('led_modem_serial'))].value : %s" % row[col2num(get_col_ref('led_modem_serial'))].value
    if row[col2num(get_col_ref('led_modem_serial'))].value != None:
        if row[col2num(get_col_ref('led_size'))].value != None:
            thin[get_tag_ref('device')] = conv2tag(row[col2num(get_col_ref('device'))].value)
            thin[get_tag_ref('led_serial')] = row[col2num(get_col_ref('led_serial'))].value.encode('utf8')
            thin[get_tag_ref('led_modem_serial')] = row[col2num(get_col_ref('led_modem_serial'))].value.encode('utf8')
            thin[get_tag_ref('company')] = conv2tag(row[col2num(get_col_ref('company'))].value)
            thin[get_tag_ref('building')] = conv2tag(row[col2num(get_col_ref('building'))].value)
            thin[get_tag_ref('detail')] = conv2tag(row[col2num(get_col_ref('detail'))].value)
            thin[get_tag_ref('load')] = conv2tag(row[col2num(get_col_ref('load'))].value)
    elif row[col2num(get_col_ref('inv_modem_serial'))].value != None:
        if row[col2num(get_col_ref('inv_size'))].value != None:
            thin[get_tag_ref('device')] = conv2tag(row[col2num(get_col_ref('device'))].value)
            thin[get_tag_ref('inv_serial')] = row[col2num(get_col_ref('inv_serial'))].value.encode('utf8')
            thin[get_tag_ref('inv_modem_serial')] = row[col2num(get_col_ref('inv_modem_serial'))].value.encode('utf8')
            thin[get_tag_ref('company')] = conv2tag(row[col2num(get_col_ref('company'))].value)
            thin[get_tag_ref('building')] = conv2tag(row[col2num(get_col_ref('building'))].value)
            thin[get_tag_ref('detail')] = conv2tag(row[col2num(get_col_ref('detail'))].value)
            thin[get_tag_ref('load')] = conv2tag(row[col2num(get_col_ref('load'))].value)
    return thin

def col2num(col_str):
    expn = 0
    col_num = 0
    for char in reversed(col_str):
        col_num += (ord(char) - ord('A') + 1) * (26 ** expn)
        expn += 1
    return col_num - 1

def conv2tag(val_str):
    if val_str in tag_ref:
        return tag_ref[val_str]
    else:
        return 'none'

def get_col_ref(key):
    if key in column_ref:
        return column_ref[key][0]
    else:
        return 'ZZZ'

def get_tag_ref(key):
    if key in column_ref:
        return column_ref[key][1]
    else:
        return 'unknown'
    
#===============================================================================
# 엑셀 수정 def 끝
#===============================================================================

#===============================================================================
# 시간 수정 def 시작
#===============================================================================
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

#===============================================================================
# 시간 수정 def 끝
#===============================================================================

#===============================================================================
# 데이터를 txt로 저장하는 def 시작
#===============================================================================

# outlier log 기록함수
# open의 경로명을 설정해주어야 한다.
def Chk_Outlier(chk_num, adj_modem_num,mds_id,unix_time, value):
    if chk_num == 1:
        f = open('outlier_lists_171109_v1.txt', 'w')    # 경로설정 / 덮어쓰기
        f.write('%d:\n' % chk_num)
        f.write('modem_num : %s\n' % adj_modem_num)
        f.write('_mds_id   : %s\n' % mds_id)
        f.write('unix_time : %s\n' % ts2datetime(unix_time))
        f.write('value     : %s\n' % value)
        f.write('\n')
        f.close()
    else:
        f = open('outlier_lists_171109_v1.txt', 'a')    # 경로설정 / 이어쓰기
        f.write('%d:\n' % chk_num)
        f.write('modem_num : %s\n' % adj_modem_num)
        f.write('_mds_id   : %s\n' % mds_id)
        f.write('unix_time : %s\n' % ts2datetime(unix_time))
        f.write('value     : %s\n' % value)
        f.write('\n')
        f.close()

#===============================================================================
# 데이터를 txt로 저장하는 def 끝
#===============================================================================

#===============================================================================
# 일일 평균를 계산하는 def 시작
#===============================================================================

# 년 평균 가동율 계산 함수
# 시작일, 종료일, 날수를 입력해주어야 한다.
# 계산만하여 출력만 한다. put은 없다.
def yr_operation_rate(start, end, days, metric_op_name, device_type, host, post, in_list):

    duration = 96*days # 한달 15분 단위.. 96 TS key 갯수

    pout = ''
    f = open("load_factor_log_1123_loadfactor.txt", 'a')

    for tagk,v in in_list.category_inv_tag_dict.items():
        for s in v:
            tags = {'device_type : ':device_type}
            if s != 'total' : tags[tagk] = s
            tot_num = in_list.category_inv_len_dict[tagk][s]
            op = query(start, end, metric_op_name, tags, host, post)
            len_num = 0
            cnt = 0
            val = 0

            if len(op) < 1:
                print "length is < 1, none packet"
                continue
            else:
                len_num = len(op[0]['dps'].keys())
                print len_num
                for k,__v in op[0]['dps'].items():
                    val +=  __v

            percent = (val * 1.0 / len_num)
            
            if percent > 100 : percent = 100

            pout =  "   %6.2f " %percent
            pout +=  "  %s ~ %s %s \n" %(start[:-9], end[:-9], tagk + ' '+ s )
            f.write(pout)
            sys.stdout.write(pout)
            sys.stdout.flush()
        f.write('\n')
    f.write('\n\n\n')
    f.close()

## 하루평균 가동율 구하는 Functions
## 
def insert_op_rate(__url, __m, __wm, devlist, __st, __et, data_json, host, port):
    cnt =0
    loop = 0
    d_type = 'device_type'
    totcount = ''
 
    st = datetime.datetime.strptime(__st, "%Y%m%d%H%M")
    et = datetime.datetime.strptime(__et, "%Y%m%d%H%M")
    start = st.strftime('%Y/%m/%d-%H:%M:%S')
    end = et.strftime('%Y/%m/%d-%H:%M:%S')
 
    dev_count = 0
     
    for dev in data_json:  # lte modem number
        #rate_result = query(start, end, 'none:rc05_operation_rate_v6', {'modem_num': dev})
        # none aggregation 은 holiday 를 구분해서 읽어옴. 이런경우. holiday 태그 두개에 대해서 다 앍어야 함
        # 그래서 읽는 방법을 변경함. count 로.
        ## led, tags,building
         
        if dev == 'led':
            totcount = 'total'
        else:
            totcount = 'each'
 
        tag_list = data_json[dev]['tags']
        for key in tag_list: # key is total, buildlng, device_type.... or
            for tag in tag_list[key]: # tag --> building.office etc
 
                if tag == 'total':
                    value_result = query(start, end, 'avg:'+__m , {'device_type': dev}, host, port)
                else:
                    value_result = query(start, end, 'avg:'+__m , {'device_type': dev, key : tag}, host, port)
 
                if value_result == '[]' or len(value_result) < 1 : continue
                 
                v_dict = value_result[0]    # rate 값
                 
                _m =  1
                _v = 0.0
                 
                _tag = ''
                for k, v in v_dict['tags'].items():
                    if k == key:
                        _tag = _tag + "%s=%s %s=%s %s=%s" %(k, v, d_type, dev, 'totcount',totcount)
                    try:
                        for ut in v_dict['dps'].keys():
                            _v += v_dict['dps'][str(ut)]
 
                            _rate = round((1.0 * _v / _m), 2)
 
                            if _rate > 100:
                                print 'rate : %s' % _rate
                                continue
 
                            pout = ' rate=%f, rate=%s \n' % (_v, _rate)
                            sys.stdout.write(pout)
 
                            sockWriteTSD(__wm, ut, _rate, _tag, host, port)
                    except KeyError , e:
                        print e
                        pass
 
                dev_count = dev_count + 1
                print ( dev_count / len(tag_list[key]) )

#===============================================================================
# Data 전송을 위한 def 시작
#===============================================================================

def query(start, end, metric, tags, host=None, port=None):
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

### Data 전송을 위한 Funtions - socket
def sockWriteTSD(__wmetric, __utime, __value, __tags=None, HOST=None, PORT=None):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    if __tags == None: __tags = 'ops=copy'

    _buf = "put %s %s %s %s\n" %( __wmetric, __utime, __value, __tags)

    ret = sock.sendall(_buf)
    pout = "  .... writing to TSDB, return(%s), cmd(%s) \r \r" %(ret, _buf)
    sys.stdout.write(pout)
    sys.stdout.flush()
    return

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
            __ut = '%s' %(k)
            __v = '%s' %(v)
            __qv = '%s' %(3*v/4.0)
            cnt = cnt + v
            loop = loop + 1
            print __ut
            sockWriteTSD( __wm, __ut, __qv, tagid[0] )
            print "processing ....", tagid[0], '>'
            
#===============================================================================
# Data 전송을 위한 def 끝
#===============================================================================

#===============================================================================
# Etc Utils def 시작
#===============================================================================

def check_list():

    valid_led = in_list.valid_led
    buff=[]

    elec = ['01222748870', '01222664503', '01222654503', '01222746482', '01222744503', '01222636543', '01222659984', '01222744780', '01222745479', '01222729989', '01222577452', '01222746397', '01222779985', '01222769989', '01222729987', '01222688541', '01222618542', '01222796541', '01222742798', '01222724501']


    inp = in_list.led_factory_list
    print len(inp),
    print len(set(inp))
    for idx in inp:
        try:
            print elec.index(idx)
        except:
            pass

    inp = in_list.led_office_list
    print len(inp),
    print len(set(inp))
    for idx in inp:
        try:
            print elec.index(idx)
        except:
            pass

    inp = in_list.led_mart_list
    print len(inp),
    print len(set(inp))
    for idx in inp:
        try:
            print elec.index(idx)
        except:
            pass

    inp = in_list.led_apt_list
    print len(inp),
    print len(set(inp))
    for idx in inp:
        try:
            print elec.index(idx)
        except:
            pass

#===============================================================================
# etc Utils def 끝
#===============================================================================