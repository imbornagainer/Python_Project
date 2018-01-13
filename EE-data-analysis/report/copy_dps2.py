# -*- coding: utf-8 -*-

# Author : hwijinkim , https://github.com/jeonghoonkang

# outlier를 제거하기 위한 class
# last modified by 20171031

# ver 0.2
# 1. 함수에서 직접 outlier log txt 파일명 설정 -> main의 변수에서 수정하도록 변경 (편의를 위하여)

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
sys.path.insert(0, '../lib')
import in_list

with open('C:/Users/Be Pious/git/kdatahub/EE-data-analysis/lib/tools/count_list.json') as data_file:
#with open('/home/bornagain/kdatahub/EE-data-analysis/lib/tools/count_list.json') as data_file:
    data_json = json.load(data_file)

#tag = {'mds-id':'911'}
HOST = '125.140.110.217'
PORT = 4242

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
        #print api_query, param
        response = requests.get(api_query, params=param)
        if response.ok:
            return response.json()
        else:
            return []

def tsdb_query(query, start, end, metric, modem, holiday):
    param = {}
    if start: param['start'] = start
    if end: param['end'] = end
    param['m'] = metric + '{' + 'holiday={1!s},modem_num={0!s}'.format(modem, holiday) + '}'
#     print query
#     print param
#     exit()
    if 1:
        response = requests.get(query, params=param)
#         print response
#         exit()
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

def tsdb_put_telnet(host, port, metric, dps, tags, file='False', outlier_txt_name='outlier.txt'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    retry = 9999
    #print 'socket error: ' + host
    while 1:
        try:
            sock.connect((host, port))
        except:
            print 'socket error: ' + host
            time.sleep(5)
            print 'time sleep 5 second'
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

    # time loop 2016/07/01 ~ 2017/07/01 by 15min, unix_time
    # check the data is None

    for dp in packed_data:
        if 1:
        #if (dp['value'] != 0 and dp['value'] != None and dp['value'] > 0.01 and dp['value'] <= 200.0):   # outlier 조건 설정
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
            send += ' 1'                                 # 값이 있으면 이진법 1처리(작동했다.)
            #send += ' {0!r}'.format(dp['value'])
            #print 'dp : %s' % dp
            if 'tags' in dp:
                for key in dp['tags']:
                    #print 'key : %s' % key
                    send += ' {0!s}'.format(key) + '={0!s}'.format(dp['tags'] [key])
            send += '\n'
            #print 'send : %s' % send
            count += 1

        else:
            global chk_number
            chk_number = (chk_number + 1)
            Chk_Outlier(chk_number, outlier_txt_name, dp['tags']['modem_num'], dp['tags']['_mds_id'], dp['timestamp'], dp['value']) # outlier log 기록함수
    #print 'send : ' + send

    if len(send) > 0:
        #print send + '\n\n'
        sock.sendall(send)
        #if file: file.write(send)
        send = ''
    sock.close()
    #print 'put dps: {0} processed...'.format(count)
    return


def find_none_dp(__url, __wm, __v, __st, __et, __period=900):

    host  = '125.140.110.217'                                       # get할 url
    port  = 4242                                                    # get할 port 번호
    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)       # opentsdb에서 get할 url 주소
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
    t_first = __st                                   # get 시작일
    t_end  = __et                                   # get 종료일
    metric_in  = 'none:rc05_operation_rate_v6'                      # get할 metric명
    #metric_out = 'rc05_none_dp_v1'                           # put할 metric명
    metric_ref  = 'none:rc04_simple_data_v3'                      # get할 metric명


    chk_number = 0                                                  # outlier 갯수 num
    modem_list = in_list.total_vlist
    modem_count = 0                             # lte 처리 갯수

    chk_day = '2017/01/01-00:00:00'

    cnt = 0
    loop = 0
    dt = datetime.datetime.strptime(__st, '%Y/%m/%d-%H:%M:%S')
    __st_unix = time.mktime(dt.timetuple())
    dt = datetime.datetime.strptime(__et, '%Y/%m/%d-%H:%M:%S')
    __et_unix = time.mktime(dt.timetuple())
    end = __et_unix
    #last = 1464739200 #2016/07/01, second scale
    #end = 1464739800
    #end = 1509494400 #2017/11/01, second scale, 1498834800 17/7/1
    #last = 1468060199

    mcount = 0
    xlist = modem_list
    for modem in modem_list:
        last = __st_unix
        mcount += 1
        pout = "  \n"
        sys.stdout.write(pout)
        if modem_list.index(modem) < 121: continue

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        while (last < end):

            start = datetime.datetime.fromtimestamp(int(last)-5).strftime('%Y/%m/%d-%H:%M:%S')
            mid = datetime.datetime.fromtimestamp(int(last)+10).strftime('%Y/%m/%d-%H:%M:%S')

            pout = "  >>  %d / 445, modem: %s last: %d, end: %d, %s %s \r" %(mcount, modem, last, end, start,mid)
            sys.stdout.write(pout)
            sys.stdout.flush()

            modem_holiday = is_weekend(start)
            _query_result = tsdb_query(query, start, mid, metric_in, modem, modem_holiday)

            if (last == __st_unix ) : # 처음 한번만 tag를 읽어 들임
                _ret = tsdb_query(query, start, chk_day, metric_in, modem, modem_holiday)
                __tag = _ret[0]['tags']
                #{u'load': u'none', u'building': u'factory', u'modem_num': u'01224230496',
                #u'company': u'middlecompany', u'detail': u'food', u'device_type': u'led', u'holiday': u'0', u'_mds_id': u'00-250130380'}
                _tag_buf = ''
                for k,v in __tag.items():
                    _tag_buf += ' %s=%s' %(k, v)
                _tag_buf += '\n'

            #print _query_result
            _ut = last
            last += __period #keep while looping until end of time

            if len(_query_result) < 1 or (len(_query_result[0]['dps'].keys())) < 1 :
                #here to process None metric
                #원본 메트릭 읽기, 값이 없으면, 1로 입력, 0인것도 값이 있으므로 해당 안됨
                #원본 메트릭에 0 또는 다른 값(정상값, outlier 값) 이 있으면 무시
                #outlier 값과 0 측정값은 비슷한 성격으로 분류, 정의한 것임
                _q_original = tsdb_query(query, start, mid, metric_ref, modem, modem_holiday)
                if len(_q_original) < 1 or len(_q_original[0]['dps'].keys()) < 1 : # 데이터 없음
                    #write
                    sockWriteTSD( sock, __wm, int(_ut), 1, _tag_buf)

        sock.close()


def cp_metric(__url, __wm, __v, __st, __et): # not yet ... in init devel status

    host  = '125.140.110.217'                                       # get할 url
    port  = 4242                                                    # get할 port 번호
    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)       # opentsdb에서 get할 url 주소
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
    t_first = __st                                   # get 시작일
    t_end  = __et                                   # get 종료일
    metric_in  = 'none:rc05_operation_rate_v6'                      # get할 metric명
    #metric_out 은 인자로 받음
    #metric_ref  = 'none:rc04_simple_data_v3'                      # get할 metric명


    chk_number = 0                                                  # outlier 갯수 num
    modem_list = in_list.total_vlist
    modem_count = 0                             # lte 처리 갯수

    chk_day = '2017/01/01-00:00:00'

    cnt = 0
    loop = 0
    dt = datetime.datetime.strptime(__st, '%Y/%m/%d-%H:%M:%S')
    __st_unix = time.mktime(dt.timetuple())
    dt = datetime.datetime.strptime(__et, '%Y/%m/%d-%H:%M:%S')
    __et_unix = time.mktime(dt.timetuple())
    end = __et_unix
    
    # 16/06/01 00:00:00
    #last = 1464739200 #2016/07/01, second scale
    #end = 1464739800
    #end = 1509494400 #2017/11/01, second scale, 1498834800 17/7/1
    #last = 1468060199

    mcount = 0
    xlist = modem_list
    for modem in modem_list:
        last = __st_unix
        mcount += 1
        pout = "  \n"
        sys.stdout.write(pout)
        # 가끔 서버 다운으로 정지되었을때, 정지 지점부터 다시 시작
        #if modem_list.index(modem) < 0: continue

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        while (last < end):
            start = datetime.datetime.fromtimestamp(int(last)).strftime('%Y/%m/%d-%H:%M:%S')
            mid = datetime.datetime.fromtimestamp(int(last)).strftime('%Y/%m/%d-%H:%M:%S')

            mid = datetime2str((str2datetime(start)) + datetime.timedelta(1))
            ux_nday = datetime2ts(mid)

            pout = "  >>  %d / 445, modem: %s last: %d, end: %d, %s %s %s \r" %(mcount, modem, last, end, __wm, start,mid)
            sys.stdout.write(pout)
            sys.stdout.flush()

            modem_holiday = is_weekend(start)
            _query_result = tsdb_query(query, start, mid, metric_in, modem, modem_holiday)

            if (last == __st_unix ) : # 처음 한번만 tag를 읽어 들임, 메트릭 write 에 사용함
                _ret = tsdb_query(query, '2016/08/01-00:00:00', chk_day, metric_in, modem, modem_holiday)
                if len(_ret) < 1 or (len(_ret[0]['dps'].keys())) < 1 :
                    print " @@@ can't find any tags during 16/08/01~17/07/01"
                    continue
                __tag = _ret[0]['tags']
                #{u'load': u'none', u'building': u'factory', u'modem_num': u'01224230496',
                #u'company': u'middlecompany', u'detail': u'food', u'device_type': u'led', u'holiday': u'0', u'_mds_id': u'00-250130380'}
                _tag_buf = ''
                for k,v in __tag.items():
                    _tag_buf += ' %s=%s' %(k, v)
                _tag_buf += '\n'

            #last += __period #keep while looping until end of time

            if len(_query_result) < 1 or (len(_query_result[0]['dps'].keys())) < 1 :
                None
            else:
                for k,v in _query_result[0]['dps'].items() :
                    #write
                    #print k, v
                    #print _tag_buf
                    sockWriteTSD( sock, __wm, int(k), v , _tag_buf)
            last = ux_nday

        sock.close()

def one_day_pattern (__url, __wm, __v, __st, __et, host, port):
    
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
    holiday = '0'
    stam_list = []
    
    dt = datetime.datetime.strptime(__st, '%Y/%m/%d-%H:%M:%S')
    __st_unix = time.mktime(dt.timetuple())
    
    dt = datetime.datetime.strptime(__et, '%Y/%m/%d-%H:%M:%S')
    __et_unix = time.mktime(dt.timetuple())
    end = __et_unix
    metric_in  = 'avg:rc05_op_rate_v10'                            # get할 metric명
    __m = metric_in
    #metric_out 은 인자로 받음
    #metric_ref  = 'none:rc04_simple_data_v3'                      # get할 metric명
    
    #last = 1464739200 #2016/07/01, second scale
    #end = 1464739800
    #end = 1509494400 #2017/11/01, second scale, 1498834800 17/7/1
    
    last = __st_unix
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    days_long = 0
    put_unix_time = 1464705900 # unix_time = 16/06/01 00:00:00
    
    for dev in data_json:
        #rate_result = query(start, end, 'none:rc05_operation_rate_v6', {'modem_num': dev})
        # none aggregation 은 holiday 를 구분해서 읽어옴. 이런경우. holiday 태그 두개에 대해서 다 앍어야 함
        # 그래서 읽는 방법을 변경함. count 로.
        ## led, tags,building
        
        if dev == 'led':
            totcount = 'total'
        else:
            totcount = 'each'

        tag_list = data_json[dev]['tags']
        
        for key in tag_list:                    # key is total, buildlng.... or
            for k,v in tag_list[key].items():   # tag --> building.office etc
                qtag = {}
                qtag['device_type'] = dev
                qtag[key] = k
                a_day_avg = {}
                for x in range(0,96):
                   a_day_avg[x] = 0

                while (last < end):
                    days_long += 1
                    start = datetime.datetime.fromtimestamp(int(last)).strftime('%Y/%m/%d-%H:%M:%S')
                    mid = datetime.datetime.fromtimestamp(int(last)).strftime('%Y/%m/%d-%H:%M:%S')

                    mid = datetime2str((str2datetime(start)) + datetime.timedelta(1))
                    ux_nday = datetime2ts(mid)

                    holiday = is_weekend(start)
#                     print start,mid
                    last = ux_nday # 하루 추가 진행을 위해 시간 변경

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

                _query_result = query(ts2datetime(__st_unix), ts2datetime(__et_unix), 'avg:'+__m , qtag)
#     
                if _query_result == '[]' or len(_query_result) < 1 : continue
                    # >>> to do : 쿼리 방식 변경 ... json 구조에 있는 것처럼 데이터를 호출해야 함
                    # >>> 예, device_type:led, building:office, detail:food
            
                    # >>> 태그는 위에서 호출한 태그 사용, 위 태그를 아래 Write 태그에 입력
                    ## 결과를 TSDB에 저장할때 달아놓을 태그들
            
                    ## 결과 저장할 (변수)
                    ## 키는 시간 96개 단위
                    ## '00:00' : 평균값, '00:15' : 평균값
                    ## 시간은 편한방식으로 지정
                denom1 = 1467298800
                denom2 = 86400

                for k,v in _query_result[0]['dps'].items() :
                   daykey = (int(k) % denom1 % denom2) / 900
                   a_day_avg[daykey] += v
                last = ux_nday # 하루 추가 진행을 위해 시간 변경
#             print '몇일째 : %s' % days_long
# 
                for k,v in a_day_avg.items():
                    a_day_avg[k] = v / days_long
                    put_unix_time += 900
                    sockWriteTSD( sock, __wm, put_unix_time, a_day_avg[k] , wtag)
            print ' [%s/%s]: ' % (days_long, days_long)

    ## 키 (시간) 루프 호출
    ## >> 해당 키 time 에 대해 전송된 모든 값을 더하고 / len(전체갯수) 함

    #query 결과를 a_day_avg 에 연산하여 입력
    # key 호출 (시간)
    #호출해서 아래 방법으로 시간 분류 (인덱싱) 0~95로 분류
    #- 1단계 : d = Unix Time % 1467298800 (2016/07/01 기준으로 처리)
    #- 2단계 : d = d % 86400 (하루 시간 내로만 범위 설정)
    #- 3단계 :  scale = d / 96, 하루는 96개 시간 단위로 분리됨

    # 해당 분류의 dp 값들을 모두 더해하고 평균하여,            
    
    sock.close()

def sockWriteTSD(sock, __wmetric, __utime, __value, __tags = None):

    if __tags == None: __tags = 'ops=copy'

    _buf = "put %s %s %s %s\n" %( __wmetric, __utime, __value, __tags)
    print _buf

    try:
        ret = sock.sendall(_buf)
    except:
        print " something wroing in socket send function"
        pass
    time.sleep(0.0001)

    return

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
    
def run():
    __url  = '125.140.110.217'           # get할 url
    port  = 4242                         # get할 port 번호

    __wm = 'rc05_tot_daily_opr_test_v1'      # put할 metric명
    __v = None
    
    __st = '2016/07/01-00:00:00'
    __et = '2016/07/10-00:00:00'
    one_day_pattern(__url, __wm, __v, __st, __et, __url, port)

#     __st = '2016/07/01-00:00:00'
#     __et = '2016/08/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)

#     __st = '2016/08/01-00:00:00'
#     __et = '2016/09/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
# 
#     __st = '2016/09/01-00:00:00'
#     __et = '2016/10/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
# 
#     __st = '2016/10/01-00:00:00'
#     __et = '2016/11/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
# 
#     __st = '2016/11/01-00:00:00'
#     __et = '2016/12/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
# 
#     __st = '2016/12/01-00:00:00'
#     __et = '2017/01/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
# 
#     __st = '2017/01/01-00:00:00'
#     __et = '2017/02/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
# 
#     __st = '2017/02/01-00:00:00'
#     __et = '2017/03/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
# 
#     __st = '2017/03/01-00:00:00'
#     __et = '2017/04/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
# 
#     __st = '2017/04/01-00:00:00'
#     __et = '2017/05/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
# 
#     __st = '2017/05/01-00:00:00'
#     __et = '2017/06/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)
# 
#     __st = '2017/06/01-00:00:00'
#     __et = '2017/07/01-00:00:00'
#     one_day_pattern(__url, __wm, __v, __st, __et, __url, port)

if __name__ == '__main__':

    run()
