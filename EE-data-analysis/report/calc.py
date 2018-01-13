# -*- coding: utf-8 -*-
# Author : jeonghoonkang , https://github.com/jeonghoonkang

import sys
sys.path.insert(0, '../lib')

import in_list
import useTSDB
import time_keys

import requests
# from collections import defaultdict

def query(start, end, metric, tags):
    host = '125.140.110.217'
    port = 4242
    api_query = 'http://{0!s}:{1!r}/api/query'.format(host,port)
    param = {}

    if start: param['start'] = start
    if end: param['end'] = end

    if tags == '{}':
        param['m'] = metric
    else :
        param['m'] = metric + '{'
        for i, tag in enumerate(tags):
            param['m'] += tag + '={0!s}'.format(tags[tag])
            if i < len(tags) - 1:
                param['m'] += ','
        param['m'] += '}'

    if 1:
        #print api_query, param
        response = requests.get(api_query, params=param)
        if response.ok:
            return response.json()
        else:
            return []

def get_data():
    start = '2016/07/01-00:00:00'
    end = '2016/08/01-00:00:00'
    metric = 'none:rc05_none_dp_v4'
    #metric = 'none:rc05_operation_rate_v6'
    tags = '{}'
    q = query(start, end, metric, tags )

    n = q[0]['dps'].keys()
    print len(n)

def make_keys():
    ts_keys=[]
    last = 1464739200 #2016/07/01, second scale
    end = 1498834801 #2017/07/01, second scale

    while last < end :
       try:
           ts_keys.append(str(last).encode('utf8'))
       except :
           print "   exception   "
           pass

       last += 900

    f = open('time_keys.py', 'w')    # 경로설정 / 덮어쓰기
    f.write('\n')
    f.write('time_keys = ')
    f.write('%s\n' %ts_keys)
    f.write('\n')
    f.close()

    print ts_keys

def make_led_base_num():
    duration = 96*365  # 한달 15분 단위.. 96 TS key 갯수

    led_num = 393

    start = '2016/07/01-00:00:00'
    end = '2017/07/01-00:00:00'
    metric = 'zimsum:rc05_none_dp_v4'
    #metric = 'none:rc05_operation_rate_v6'
    metric_op = 'zimsum:rc05_operation_rate_v6'
    tags = {'device_type':'led', 'detail':'sangyong'}

    q = query(start, end, metric, tags )
    op = query(start, end, metric_op, tags )

    none_num = 0
    cnt = 0
    val = 0

    if len(q) < 1:
        print "length is < 1, none packet"
    else:
        print len(q[0]['dps'].keys())
        for k,v in q[0]['dps'].items():
            none_num +=  v

    for tsk in time_keys.time_keys :
        if tsk in op[0]['dps'] :
            val += op[0]['dps'][tsk]

    base_num = (led_num * 1.0 * duration - none_num) / duration

    print base_num
    print val / (base_num * duration)


def yr_operation_rate(start, end, days):
    #
    duration = 96*days # 한달 * (하루의 15분 단위.. 96 TS key 갯수)
    #print in_list.category_dict['led_num']

    metric = 'zimsum:rc05_none_dp_v4'
    #metric = 'none:rc05_operation_rate_v6'
    metric_op = 'zimsum:rc05_operation_rate_v6'

    pout = ''
    f = open("operation_rate_log_171123_inverter_last.txt", 'a')

    for tagk,v in in_list.category_inv_tag_dict.items():
        for s in v:
            tags = {'device_type':'inverter'}
            if s != 'total' : tags[tagk] = s
            tot_num = in_list.category_inv_len_dict[tagk][s]
            #print " ... processing %s" %tags
            q = query(start, end, metric, tags )

            op = query(start, end, metric_op, tags )
            none_num = 0
            cnt = 0
            val = 0

            if len(q) < 1:
                print "q length is < 1, none packet"
                continue
            else:
                for k,__v in q[0]['dps'].items():
                    none_num +=  __v

            for tsk in time_keys.time_keys :
                if len(op) < 1:
                    print 'op length is < 1, none packet'
                    continue
                if tsk in op[0]['dps'] :
                    val += op[0]['dps'][tsk]
            base_num = (tot_num * 1.0 * duration - none_num) / duration

            percent = (100*(val / (base_num * duration)))
            if percent > 100 : percent = 100

            pout =  "   %6.2f " %percent
            pout +=  "  base-num: %6.1f / %3d ," %(base_num, tot_num)
            pout +=  "  %s ~ %s %s \n" %(start[:-9], end[:-9], tagk+' '+s )
            f.write(pout)
            sys.stdout.write(pout)
            sys.stdout.flush()
        f.write('\n')
    f.write('\n\n\n')
    f.close()



def check_list():

    valid_led = in_list.valid_led
    buff=[]

    elec = ['01222748870', '01222664503', '01222654503', '01222746482', '01222744503', '01222636543', '01222659984', '01222744780', '01222745479', '01222729989', '01222577452', '01222746397', '01222779985', '01222769989', '01222729987', '01222688541', '01222618542', '01222796541', '01222742798', '01222724501']


    inp = in_list.led_factory_list
    #print "led_factory_list",
    print len(inp),
    print len(set(inp))
    for idx in inp:
        try:
            print elec.index(idx)
        except:
            pass
        #buff.append(valid_led.index(idx))

    inp = in_list.led_office_list
    #print "led_office_list",
    print len(inp),
    print len(set(inp))
    for idx in inp:
        try:
            print elec.index(idx)
        except:
            pass

    inp = in_list.led_mart_list
    #print "led_mart_list",
    print len(inp),
    print len(set(inp))
    for idx in inp:
        try:
            print elec.index(idx)
        except:
            pass

    inp = in_list.led_apt_list
    #print "led_apt_list",
    print len(inp),
    print len(set(inp))
    for idx in inp:
        try:
            print elec.index(idx)
        except:
            pass


def run():

     start = '2016/07/01-00:00:00'
     end = '2017/07/01-00:00:00'
     yr_operation_rate(start, end, 365)
     

     start = '2016/07/01-00:00:00'
     end = '2016/08/01-00:00:00'
     yr_operation_rate(start, end, 31)

     start = '2016/08/01-00:00:00'
     end = '2016/09/01-00:00:00'
     yr_operation_rate(start, end, 31)

     start = '2016/09/01-00:00:00'
     end = '2016/10/01-00:00:00'
     yr_operation_rate(start, end, 30)

     start = '2016/10/01-00:00:00'
     end = '2016/11/01-00:00:00'
     yr_operation_rate(start, end, 31)

     start = '2016/11/01-00:00:00'
     end = '2016/12/01-00:00:00'
     yr_operation_rate(start, end, 30)

     start = '2016/12/01-00:00:00'
     end = '2017/01/01-00:00:00'
     yr_operation_rate(start, end, 31)

     start = '2017/01/01-00:00:00'
     end = '2017/02/01-00:00:00'
     yr_operation_rate(start, end, 30)

     start = '2017/02/01-00:00:00'
     end = '2017/03/01-00:00:00'
     yr_operation_rate(start, end, 28)

     start = '2017/03/01-00:00:00'
     end = '2017/04/01-00:00:00'
     yr_operation_rate(start, end, 31)

     start = '2017/04/01-00:00:00'
     end = '2017/05/01-00:00:00'
     yr_operation_rate(start, end, 30)

     start = '2017/05/01-00:00:00'
     end = '2017/06/01-00:00:00'
     yr_operation_rate(start, end, 31)

     start = '2017/06/01-00:00:00'
     end = '2017/07/01-00:00:00'
     yr_operation_rate(start, end, 30)

if __name__ == "__main__":

    run()
