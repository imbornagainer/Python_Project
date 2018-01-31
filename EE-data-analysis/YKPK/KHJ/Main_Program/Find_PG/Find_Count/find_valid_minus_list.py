# -*- coding: utf-8 -*-

# Author : hwijinkim , https://github.com/jeonghoonkang
# Author : jeonghoonkang , https://github.com/jeonghoonkang

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
    
    packed_data = pack_dps(metric, dps, tags)
    for dp in packed_data:        
        if (dp['value'] != 0 and dp['value'] != None and dp['value'] > 0.19 and dp['value'] <= 100.0):   # outlier 조건 설정        
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
            #send += ' 1'                                 # 값이 있으면 이진법 1처리(작동했다.)
            send += ' {0!r}'.format(dp['value'])
            #print ' saving to DB, dp : %s' % dp
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

# outlier log 기록함수
def Chk_Outlier(chk_num, outlier_txt_name, adj_modem_num, mds_id,unix_time, value):
    if chk_num == 1:
        f = open(outlier_txt_name, 'w')    # 경로설정 / 덮어쓰기
        f.write('%d:\n' % chk_num)
        f.write('modem_num : %s\n' % adj_modem_num)
        f.write('_mds_id   : %s\n' % mds_id)
        f.write('unix_time : %s\n' % ts2datetime(unix_time))
        f.write('value     : %s\n' % value)
        f.write('\n')
        f.close()
    else:
        f = open(outlier_txt_name, 'a')    # 경로설정 / 이어쓰기
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

def add_time(dt_str, days=0, hours=0, minutes=0, seconds=0):
    return datetime2str(str2datetime(dt_str) + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds))

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
    last  = '2016/08/01-00:00:00'                                   # get 종료일
    metric_in  = 'none:rc05_operation_rate_v3'                      # get할 metric명
    metric_out = 'rc05_BRR_15min_tag_v2'                            # put할 metric명
    outlier_txt_name = '__test_171114_brc_002.txt'                  # outlier log를 저장할 txt명
    
    chk_number = 0                                                  # outlier 갯수 num
    
    # 2. get할 metric에서 가져올 특정 list 설정
    modem_list= [u'01224230496', u'01224230495', u'01224230493', u'01224230490', u'01224230558', u'01222649984', u'01222564542', u'01222704504', u'01222704503', u'01222704501', u'01222714543', u'01222679989', u'01222709929', u'01224230491', u'01221429369', u'01222769542', u'01221429367', u'01221429366', u'01221441994', u'01222647452', u'01224230551', u'01221388836', u'01222747452', u'01221431994', u'01222754503', u'01222687452', u'01222754501', u'01222754504', u'01222664501', u'01224230478', u'01224230479', u'01224230470', u'01224230472', u'01222745458', u'01224230476', u'01224230477', u'01224272938', u'01224272937', u'01222746397', u'01222746396', u'01222746390', u'01222744503', u'01222744501',u'01222742798', u'01222744504', u'01223239871', u'01223192247', u'01221243882', u'01222714504', u'01222714503', u'01221243887', u'01222745363', u'01221243885', u'01220800592', u'01222742949', u'01223239872', u'01223239873', u'01223239874', u'01223239875', u'01222742946', u'01221391199', u'01221390254', u'01222764501', u'01221429368', u'01221251996', u'01224230500', u'01224230501', u'01224230504', u'01224230506', u'01224230507', u'01224230509', u'01222764503', u'01222587543', u'01221567011', u'01221474402', u'01221474403', u'01221474406', u'01221474407', u'01221474404', u'01221474405', u'01222742760', u'01223187395', u'01223187394', u'01223187397', u'01222577452', u'01221388068', u'01224230434', u'01224230435', u'01224230436', u'01224230437', u'01221421994', u'01224230433', u'01221283886', u'01222699987', u'01222683542', u'01224230439', u'01223187398', u'01222758870', u'01222779986', u'01222779987', u'01222779984', u'01222616541', u'01224273086', u'01222709541', u'01222749989', u'01222744780', u'01222798870', u'01222749985', u'01222749984', u'01222755541', u'01222746366', u'01224273013', u'01223192284', u'01223192287', u'01222748870', u'01223192283', u'01223192327', u'01224224135', u'01224272962', u'01224272966', u'01222742908', u'01222745933', u'01222745934', u'01222745935', u'01222745938', u'01222745939', u'01221721213', u'01224230549', u'01224230546', u'01224230541', u'01224230542', u'01221574354', u'01221574357', u'01221574356', u'01221574359', u'01222742834', u'01223192410', u'01224230480', u'01222744754', u'01224230483', u'01224230529', u'01221261996', u'01223192453', u'01222587452', u'01221567020', u'01222659986', u'01222659984', u'01222766541', u'01222739929', u'01223187430', u'01223187431', u'01222779985', u'01223187435', u'01223187436', u'01224230449', u'01224230446', u'01224230443', u'01222796541', u'01222664504', u'01222746383', u'01222746380', u'01222746381', u'01222688541', u'01221387937', u'01222745479', u'01223209891', u'01223209890', u'01222779929', u'01224224149', u'01220800701', u'01221253884', u'01222694503', u'01222742878', u'01222676543', u'01224230534', u'01224230531', u'01224230530', u'01224230533', u'01224230532', u'01224230539', u'01221391244', u'01221566960', u'01221566963', u'01221574346', u'01222742752', u'01222742757', u'01223187386', u'01223187387', u'01223187384', u'01223189591', u'01221388812', u'01222745495', u'01222746459', u'01221386983', u'01222563542', u'01224230473', u'01222749929', u'01223219133', u'01223219131', u'01223219130', u'01221391155', u'01223192328', u'01222746350', u'01222746421', u'01220684147', u'01222799985', u'01222799986', u'01222742934', u'01224272955', u'01222769989', u'01222788870', u'01222769984', u'01224230571', u'01224230570', u'01224230573', u'01224230575', u'01224230577', u'01224230576', u'01223192263', u'01221341993', u'01221391442', u'01222666541', u'01222719541', u'01222667543', u'01222745510', u'01222636543', u'01222797541', u'01222729987', u'01222729989', u'01221574336', u'01221291991', u'01223188270', u'01223189537', u'01224273071', u'01224273073', u'01222742704', u'01223187406', u'01223187403', u'01223187402', u'01224230451', u'01224230457', u'01224230458', u'01224230459', u'01222746463', u'01222746461', u'01222597452', u'01222586543', u'01221388441', u'01220800748', u'01221343888', u'01222742200', u'01221351991', u'01222745943', u'01222745947', u'01222739986', u'01222739987', u'01222745462', u'01223209883', u'01222765541', u'01223209881', u'01223209886', u'01223209884', u'01223209888', u'01223209889', u'01223192308', u'01222699986', u'01222699984', u'01222742969', u'01224272982', u'01223192395', u'01223192394', u'01223192393', u'01223192392', u'01223192391', u'01221566961', u'01224230528', u'01224230482', u'01224230485', u'01224230484', u'01224230487', u'01224230486', u'01224230489', u'01224230488', u'01221311993', u'01224230526', u'01224230527', u'01224230525', u'01222669986', u'01222694501', u'01221566970', u'01221566971', u'01221471994', u'01221463494', u'01222597541', u'01222759929', u'01222753541', u'01222567452', u'01221731209', u'01222745527', u'01222689984', u'01222719929', u'01223219128', u'01223219129', u'01223219126', u'01222746482', u'01221371993', u'01221371991', u'01222618542', u'01224230469', u'01224230461', u'01224230460', u'01224230467', u'01222745635', u'01224230464', u'01222734504', u'01222734501', u'01224273037', u'01224273039', u'01224273038', u'01222769929', u'01221448178', u'01220435025', u'01222742885', u'01224230465', u'01222742927', u'01222742888', u'01224272944', u'01222745859', u'01222664503', u'01223239870', u'01224230564', u'01224230565', u'01220800593', u'01224230568', u'01224230569', u'01223239867', u'01223239866', u'01223239865', u'01220800623', u'01223239869', u'01223239868', u'01222742956', u'01222767541', u'01221961213', u'01224230513', u'01224230512', u'01224230511', u'01224230510', u'01224230517', u'01224230516', u'01224230515', u'01224230518', u'01222794503', u'01221273883', u'01222674503', u'01221474387', u'01222674501', u'01222776543', u'01222674504', u'01221574324', u'01223188269', u'01222746456', u'01221474414', u'01221474413', u'01221474412', u'01222719989', u'01223187417', u'01223187414', u'01223187419', u'01222734543', u'01221341991', u'01222746472', u'01222729929', u'01221451993', u'01222684504', u'01222684501', u'01222684503', u'01222739541', u'01220800574', u'01221361991', u'01224273091', u'01222654501', u'01222654503', u'01222654504', u'01222759989', u'01223188887', u'01222789986', u'01221390965', u'01222724501', u'01222724503', u'01222742916', u'01222742912', u'01223192386']
    #valid_led=[u'01224230496', u'01224230495', u'01224230493', u'01224230490', u'01224230558', u'01222649984', u'01222564542', u'01222704504', u'01222704503', u'01222704501', u'01222714543', u'01222679989', u'01222709929', u'01224230491', u'01221429369', u'01222769542', u'01221429367', u'01221429366', u'01221441994', u'01222647452', u'01224230551', u'01221388836', u'01222747452', u'01221431994', u'01222754503', u'01222687452', u'01222754501', u'01222754504', u'01222664501', u'01224230478', u'01224230479', u'01224230470', u'01224230472', u'01222745458', u'01224230476', u'01224230477', u'01224272938', u'01224272937', u'01222746397', u'01222746396', u'01222746390', u'01222744503', u'01222744501',u'01222742798', u'01222744504', u'01223239871', u'01223192247', u'01221243882', u'01222714504', u'01222714503', u'01221243887', u'01222745363', u'01221243885', u'01220800592', u'01222742949', u'01223239872', u'01223239873', u'01223239874', u'01223239875', u'01222742946', u'01221391199', u'01221390254', u'01222764501', u'01221429368', u'01221251996', u'01224230500', u'01224230501', u'01224230504', u'01224230506', u'01224230507', u'01224230509', u'01222764503', u'01222587543', u'01221567011', u'01221474402', u'01221474403', u'01221474406', u'01221474407', u'01221474404', u'01221474405', u'01222742760', u'01223187395', u'01223187394', u'01223187397', u'01222577452', u'01221388068', u'01224230434', u'01224230435', u'01224230436', u'01224230437', u'01221421994', u'01224230433', u'01221283886', u'01222699987', u'01222683542', u'01224230439', u'01223187398', u'01222758870', u'01222779986', u'01222779987', u'01222779984', u'01222616541', u'01224273086', u'01222709541', u'01222749989', u'01222744780', u'01222798870', u'01222749985', u'01222749984', u'01222755541', u'01222746366', u'01224273013', u'01223192284', u'01223192287', u'01222748870', u'01223192283', u'01223192327', u'01224224135', u'01224272962', u'01224272966', u'01222742908', u'01222745933', u'01222745934', u'01222745935', u'01222745938', u'01222745939', u'01221721213', u'01224230549', u'01224230546', u'01224230541', u'01224230542', u'01221574354', u'01221574357', u'01221574356', u'01221574359', u'01222742834', u'01223192410', u'01224230480', u'01222744754', u'01224230483', u'01224230529', u'01221261996', u'01223192453', u'01222587452', u'01221567020', u'01222659986', u'01222659984', u'01222766541', u'01222739929', u'01223187430', u'01223187431', u'01222779985', u'01223187435', u'01223187436', u'01224230449', u'01224230446', u'01224230443', u'01222796541', u'01222664504', u'01222746383', u'01222746380', u'01222746381', u'01222688541', u'01221387937', u'01222745479', u'01223209891', u'01223209890', u'01222779929', u'01224224149', u'01220800701', u'01221253884', u'01222694503', u'01222742878', u'01222676543', u'01224230534', u'01224230531', u'01224230530', u'01224230533', u'01224230532', u'01224230539', u'01221391244', u'01221566960', u'01221566963', u'01221574346', u'01222742752', u'01222742757', u'01223187386', u'01223187387', u'01223187384', u'01223189591', u'01221388812', u'01222745495', u'01222746459', u'01221386983', u'01222563542', u'01224230473', u'01222749929', u'01223219133', u'01223219131', u'01223219130', u'01221391155', u'01223192328', u'01222746350', u'01222746421', u'01220684147', u'01222799985', u'01222799986', u'01222742934', u'01224272955', u'01222769989', u'01222788870', u'01222769984', u'01224230571', u'01224230570', u'01224230573', u'01224230575', u'01224230577', u'01224230576', u'01223192263', u'01221341993', u'01221391442', u'01222666541', u'01222719541', u'01222667543', u'01222745510', u'01222636543', u'01222797541', u'01222729987', u'01222729989', u'01221574336', u'01221291991', u'01223188270', u'01223189537', u'01224273071', u'01224273073', u'01222742704', u'01223187406', u'01223187403', u'01223187402', u'01224230451', u'01224230457', u'01224230458', u'01224230459', u'01222746463', u'01222746461', u'01222597452', u'01222586543', u'01221388441', u'01220800748', u'01221343888', u'01222742200', u'01221351991', u'01222745943', u'01222745947', u'01222739986', u'01222739987', u'01222745462', u'01223209883', u'01222765541', u'01223209881', u'01223209886', u'01223209884', u'01223209888', u'01223209889', u'01223192308', u'01222699986', u'01222699984', u'01222742969', u'01224272982', u'01223192395', u'01223192394', u'01223192393', u'01223192392', u'01223192391', u'01221566961', u'01224230528', u'01224230482', u'01224230485', u'01224230484', u'01224230487', u'01224230486', u'01224230489', u'01224230488', u'01221311993', u'01224230526', u'01224230527', u'01224230525', u'01222669986', u'01222694501', u'01221566970', u'01221566971', u'01221471994', u'01221463494', u'01222597541', u'01222759929', u'01222753541', u'01222567452', u'01221731209', u'01222745527', u'01222689984', u'01222719929', u'01223219128', u'01223219129', u'01223219126', u'01222746482', u'01221371993', u'01221371991', u'01222618542', u'01224230469', u'01224230461', u'01224230460', u'01224230467', u'01222745635', u'01224230464', u'01222734504', u'01222734501', u'01224273037', u'01224273039', u'01224273038', u'01222769929', u'01221448178', u'01220435025', u'01222742885', u'01224230465', u'01222742927', u'01222742888', u'01224272944', u'01222745859', u'01222664503', u'01223239870', u'01224230564', u'01224230565', u'01220800593', u'01224230568', u'01224230569', u'01223239867', u'01223239866', u'01223239865', u'01220800623', u'01223239869', u'01223239868', u'01222742956', u'01222767541', u'01221961213', u'01224230513', u'01224230512', u'01224230511', u'01224230510', u'01224230517', u'01224230516', u'01224230515', u'01224230518', u'01222794503', u'01221273883', u'01222674503', u'01221474387', u'01222674501', u'01222776543', u'01222674504', u'01221574324', u'01223188269', u'01222746456', u'01221474414', u'01221474413', u'01221474412', u'01222719989', u'01223187417', u'01223187414', u'01223187419', u'01222734543', u'01221341991', u'01222746472', u'01222729929', u'01221451993', u'01222684504', u'01222684501', u'01222684503', u'01222739541', u'01220800574', u'01221361991', u'01224273091', u'01222654501', u'01222654503', u'01222654504', u'01222759989', u'01223188887', u'01222789986', u'01221390965', u'01222724501', u'01222724503', u'01222742916', u'01222742912', u'01223192386']
    print '<총 {0!r}개의 Modem list 데이터 추출>\n'.format(len(modem_list))
    
    data_count = 0                              # lte 처리 갯수
    start_time = datetime.datetime.now()        # 프로그램 시작값
    nodata_count = 0
    _all_len = len(modem_list)
    #__done = 0

    #3. 입력된 lte_list를 for문으로 하나씩 get함
    #4. get한 값을 put함
    #5. 반복적으로 get & put 마지막 list까지
    ### 시작일 ~ 끝일까지 하루 data씩 get & put (get data 많으면 opentsdb가 timeout될 수 있기 때문에)

    tmp_time = datetime.datetime.now()
    end = first

    # adding 15-min, 15분 단위 시간으로 증가 하면서 지정 날짜까지 Loop 실행 
    while is_past(end, last): 
        #테스트로 loop 실행횟수를 제한하려면, 아래 구문 실행
#         __done += 1
#         if __done > 5 : exit()
        start = end
        end = add_time(start, minutes=15)
        __t = None
        group = None

        for modem in modem_list:
            modem_holiday = is_weekend(start)
            query_result = tsdb_query(query, start, add_time(end, seconds=1), metric_in, modem, modem_holiday)
            __qlen = len(query_result)            
            
            if __qlen > 0 : 
                data_count += 1
                if group == None : group = query_result[0]
            else :
                nodata_count += 1
            time.sleep(0.001)

        __rate = round(data_count * 100.0 / _all_len, 2) 
        __rate_str = "%f" %__rate
        print __rate_str,"%",  

        if group == None : continue

        if USE_HTTP_API_PUT:
            None
            #tsdb_put(put, metric_out, group['dps'], modem, out_file)
        else:
            None
            for k, v in group['dps'].items():
                group['dps'][k] = __rate
            #print group
            tsdb_put_telnet(host, port, metric_out, group['dps'], group['tags'], 'True', outlier_txt_name)

        print 'elapsed time: {0!s}, {1!s}'.format(datetime.datetime.now() - tmp_time, datetime.datetime.now() - start_time)
        print '<총 {0!r}~{1!r}날 Modem 데이터 처리>\n'.format(end, last)
        nodata_count = 0 
        data_count = 0
    print 'total elapsed time: {0!s}'.format(datetime.datetime.now() - start_time)