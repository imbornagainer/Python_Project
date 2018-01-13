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

# 일일 평균 가동율 계산 함수
# 시작일, 종료일, 날수를 입력해주어야 한다.         
def yr_operation_rate(start, end, days):

    duration = 96*days # 한달 15분 단위.. 96 TS key 갯수

    metric_op = 'avg:___d_tag_test_load_rate_4'

    pout = ''
    f = open("load_factor_log_1123_loadfactor.txt", 'a')

    for tagk,v in in_list.category_inv_tag_dict.items():
        for s in v:
            tags = {'device_type':'inverter'}
            if s != 'total' : tags[tagk] = s
            tot_num = in_list.category_inv_len_dict[tagk][s]
            op = query(start, end, metric_op, tags)
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

def insert_op_rate(__url, __m, __wm, devlist, maxdict, __st, __et, data_json, of):
    cnt =0
    loop = 0
    d_type = 'device_type'
    totcount = ''
    _pre_m = 0
    print 'hi!'
    exit()

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
            
            print start, end
            exit()

            holiday = is_weekend(start)

            #print holiday

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
                    _pre_m = 0
#                     dev = 'led'
#                     key = 'detail'
#                     tag = 'medical'
                    if tag == 'total':
                        rate_result = query(start, end, 'zimsum:rc04_totoal_cnt__002', {d_type: dev})
                        value_result = query(start, end, 'zimsum:'+__m , {'device_type': dev})
                    else:
                        rate_result = query(start, end, 'zimsum:rc04_totoal_cnt__002', {d_type: dev, key : tag})
                        value_result = query(start, end, 'zimsum:'+__m , {'device_type': dev, key : tag})
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
                                
                                #print _m                                
                                
                                # 주중 최대값 구하기
                                if _m > _pre_m:
                                    if holiday != 1:
                                        _pre_m = _m

                                # 주중값은 평상시 값으로 나누기
                                if holiday == 0:
                                    _rate = round((1.0 * _v / _m * 100.0), 2)
                                    #print _rate
                                # 주말값은 주중 최대값으로 나누기
                                else:
                                    _rate = round((1.0 * _v / _pre_m * 100.0), 2)
                                    #print _rate

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
        
    ### Data 전송을 위한 Funtions - socket
    def sockWriteTSD(__wmetric, __utime, __value, __tags = None):
        if __tags == None: __tags = 'ops=copy'
    
        _buf = "put %s %s %s %s\n" %( __wmetric, __utime, __value, __tags)
        
        ret = sock.sendall(_buf)
        pout = "  .... writing to TSDB, return(%s), cmd(%s) \r \r" %(ret, _buf)
        sys.stdout.write(pout)
        sys.stdout.flush()
        return

