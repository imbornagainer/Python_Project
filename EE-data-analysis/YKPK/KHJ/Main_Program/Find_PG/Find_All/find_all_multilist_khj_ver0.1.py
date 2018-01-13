# -*- coding: utf-8 -*-
# Author : hwijinkim , https://github.com/jeonghoonkang

# 1. 해당 metric의 LED, INV의 갯수찾기
# 2. 해당 metric의 항목별 갯수 찾기 
# last modified by 20171115

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
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

def Find_Tags(metric, dps, tags):
    packed_data = pack_dps(metric, dps, tags)

    #print 'packed_data : %s' % packed_data
    global apt_cnt
    
    for dp in packed_data:
        #print 'dp : %s' % dp
        if dp['tags']['modem_num'] == 'led':
            apt_cnt = 1
            print 'led cnt : %s' % apt_cnt
            break

# MaxValue 기록함수
def Write_TagsLists(total_led_apt_cnt, total_inv_apt_cnt):
    f = open('apt_cnt_171108.txt', 'w')    # 경로설정 / 덮어쓰기
    f.write('led_apt_cnt : %s\n' % total_led_apt_cnt)
    f.write('inv_apt_cnt : %s\n' % total_inv_apt_cnt)
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
    last  = '2016/07/02-00:00:00'                                   # get 종료일
    metric_in  = 'none:rc05_operation_tag_v3'                       # get할 metric명
    #metric_in  = 'sum:rc04_simple_data_v3'
    chk_number = 0                                                  # outlier 횟수
    save_outlier = 0.0
    max_dic = ''
    apt_cnt = 0
    total_led_apt_cnt = 0
    total_inv_apt_cnt = 0
    
    # 2. get할 metric에서 가져올 특정 list 설정
    #modem_list = ['01222799986', '01220800574', '01224230529', '01222714543', '01224230467', '01223239869', '01224230576', '01222679989', '01222746396', '01222746350', '01224230549', '01223192391', '01221343888', '01224230577', '01222729929', '01221574361', '01224230493', '01224230501', '01224272949', '01224230526', '01221386983', '01223239875', '01223239870', '01221451993', '01221251996', '01224230542', '01224230434', '01224230480', '01224230484', '01224230485', '01224230470', '01222746456', '01222742834', '01223219133', '01223219131', '01223219130', '01223219129', '01223192247', '01222745462', '01221574357', '01222699986', '01222742200', '01222649984', '01222754504', '01222739929', '01224230571', '01222674503', '01224230527', '01224230569', '01222669986', '01223187397', '01223209886', '01222764501', '01222742912', '01224272962', '01222745935', '01222745933', '01222745947', '01222742969', '01222742878', '01222746463', '01223239874', '01223239873', '01222704503', '01223187431', '01223187430', '01224272938', '01222745939', '01222674501', '01220684147', '01222694501', '01222734501', '01223187419', '01223188270', '01223189537', '01222769929', '01221574356', '01224230509', '01224230472', '01224230478', '01222746390', '01222745510', '01222719929', '01221574359', '01222746366', '01222779929', '01223239865', '01223219128', '01224230518', '01223187436', '01223188269', '01222754503', '01222742885', '01222745938', '01222724503', '01222704504', '01222742752', '01222694503', '01224230546', '01221341991', '01224224149', '01220800623', '01220435025', '01224230511', '01224230515', '01224230461', '01224230533', '01224230451', '01223209883', '01223209884', '01223219126', '01223209881', '01223192283', '01222654504', '01222755541', '01222766541', '01222709541', '01222744754', '01222719541', '01222739541', '01222587543', '01222666541', '01221291991', '01223192386', '01222714503', '01224230446', '01224230532', '01222667543', '01222764503', '01222586543', '01222684504', '01222699987', '01222742956', '01222684501', '01222699984', '01224230479', '01221731209', '01224230558', '01224230495', '01222739987', '01222739986', '01221388812', '01221388441', '01221721213', '01221961213', '01223187386', '01223192395', '01224273086', '01222567452', '01222587452', '01221566970', '01221566958', '01222714504', '01222664504', '01222676543', '01222742757', '01222647452', '01222744504', '01222749989', '01222746383', '01222776543', '01222745635', '01222597452', '01222745363', '01222779984', '01224230436', '01222758870', '01221474412', '01221474414', '01222779987', '01224273013', '01222745527', '01222745458', '01222664501', '01222779986', '01224230496', '01221566963', '01221574336', '01224230433', '01222767541', '01222742927', '01222742916', '01222689984', '01222687452', '01222742760', '01224230525', '01222797541', '01224230439', '01224272937', '01224272982', '01224230449', '01224230506', '01222746381', '01224230477', '01224273037', '01223192327', '01223192308', '01223192263', '01223192287', '01223192392', '01224230491', '01221421994', '01221441994', '01222749929', '01222659986', '01224230473', '01223187393', '01224230530', '01223239872', '01224230488', '01223187389', '01223209885', '01224273039', '01224273091', '01224230570', '01224272955', '01224230483', '01224230513', '01224230482', '01223239867', '01224230507', '01224230517', '01224273038', '01224230490', '01222704501', '01222798870', '01223239866', '01222754501', '01222709929', '01222748870', '01224230528', '01222683542', '01222664503', '01222654503', '01222674504', '01222746482', '012227694504', '01222719989', '01221448178', '01222744503', '01223192284', '01223187417', '01223187414', '01222759929', '01221311993', '01221243882', '01221361991', '01223192328', '01221371991', '01221474413', '01221273883', '01222654501', '01222799985', '01221253884', '01220800593', '01222742949', '01222746459', '01222684503', '01224230460', '01224230565', '01224230465', '01221388068', '01221391442', '01221391244', '01221391199', '01221391155', '01224230476', '01221574346', '01221567020', '01222765541', '01222734504', '01221566961', '01221566960', '01223189591', '01221566971', '01223187435', '01221574354', '01223188887', '01221574324', '01221567011', '01222742946', '01222636543', '01222659984', '01222745943', '01222563542', '01224230564', '01224230568', '01224230541', '01220800748', '01222744780', '01224230541', '01224230539', '01224230534', '01222745479', '01222729989', '01222577452', '01222746397', '01222779985', '01222769989', '01222729987', '01222688541', '01222618542', '01224230435', '01224230487', '01223209889', '01223209891', '01223209888', '01224230504', '01224230486', '01224230469', '01224230510', '01222746461', '01224230443', '01222796541', '01224230512', '01222742798', '01222746421', '01222753541', '01222744501', '01222749984', '01222749985', '01222742888', '01222742934', '01222788870', '01222746472', '01222597541', '01222769542', '01222616541', '01222742704', '01224230437', '01222724501', '01221283886', '01222564542', '01222742908', '01222745934', '01222745495', '01222745859', '01224230516', '01224230500', '01221390965', '01221387937', '01221474387', '01221351991', '01221431994', '01221261996', '01222769984', '01223187402', '01223187398', '01223187384', '01223187403', '01223187406', '01224272944', '01221429366', '01221429367', '01221429369', '01221471994', '01221474403', '01221474402', '01221474406', '01221474407', '01221341993', '01221371993', '01223192410', '01223192453', '01221243885', '01221243887', '01224230464', '01223192393', '01223192394', '01223187395', '01224230458', '01224230459', '01222746380', '01222794503', '01222759989', '01220800701', '01222734543', '01222747452', '01223187394', '01223187387', '01221463494', '01221429368', '01221390254', '01221388836', '01221474404', '01221474405', '01222789986', '01224230502', '01224273014', '01224272948', '01223187306', '01223187305', '01221392626', '01221392897', '01224272943', '01224273042', '01223187310', '01223187316', '01223181056', '01223181052', '01223187319', '01223192261', '01223187358', '01224230567', '01224273017', '01223187286', '01223180993', '01220553054', '01224273061', '01224273022', '01221392027', '01221389654', '01221390900', '01221387086', '01221387826', '01223187380', '01221399481', '01221393131', '01221393546', '01224273046', '01224273052', '01223239879', '01223239880', '01223239878', '01223239876', '01223192275', '01223192271', '01223192368', '01223192376', '01223192373', '01223181052', '01223181049', '01224273085', '01224273018', '01224273092', '01224273096', '01223180966', '01223180976', '01224230447', '01224230455', '01224230466', '01224230441', '01224230521', '01224272948', '01224273045', '01224272958', '01224230559', '01224273026', '01224273079', '01224272971', '01223192371', '01223187370', '01223192249', '01220800675', '01224272988']    
    #led_list = ['01222799986', '01220800574', '01224230529', '01222714543', '01224230467', '01223239869', '01224230576', '01222679989', '01222746396', '01222746350', '01224230549', '01223192391', '01221343888', '01224230577', '01222729929', '01221574361', '01224230493', '01224230501', '01224272949', '01224230526', '01221386983', '01223239875', '01223239870', '01221451993', '01221251996', '01224230542', '01224230434', '01224230480', '01224230484', '01224230485', '01224230470', '01222746456', '01222742834', '01223219133', '01223219131', '01223219130', '01223219129', '01223192247', '01222745462', '01221574357', '01222699986', '01222742200', '01222649984', '01222754504', '01222739929', '01224230571', '01222674503', '01224230527', '01224230569', '01222669986', '01223187397', '01223209886', '01222764501', '01222742912', '01224272962', '01222745935', '01222745933', '01222745947', '01222742969', '01222742878', '01222746463', '01223239874', '01223239873', '01222704503', '01223187431', '01223187430', '01224272938', '01222745939', '01222674501', '01220684147', '01222694501', '01222734501', '01223187419', '01223188270', '01223189537', '01222769929', '01221574356', '01224230509', '01224230472', '01224230478', '01222746390', '01222745510', '01222719929', '01221574359', '01222746366', '01222779929', '01223239865', '01223219128', '01224230518', '01223187436', '01223188269', '01222754503', '01222742885', '01222745938', '01222724503', '01222704504', '01222742752', '01222694503', '01224230546', '01221341991', '01224224149', '01220800623', '01220435025', '01224230511', '01224230515', '01224230461', '01224230533', '01224230451', '01223209883', '01223209884', '01223219126', '01223209881', '01223192283', '01222654504', '01222755541', '01222766541', '01222709541', '01222744754', '01222719541', '01222739541', '01222587543', '01222666541', '01221291991', '01223192386', '01222714503', '01224230446', '01224230532', '01222667543', '01222764503', '01222586543', '01222684504', '01222699987', '01222742956', '01222684501', '01222699984', '01224230479', '01221731209', '01224230558', '01224230495', '01222739987', '01222739986', '01221388812', '01221388441', '01221721213', '01221961213', '01223187386', '01223192395', '01224273086', '01222567452', '01222587452', '01221566970', '01221566958', '01222714504', '01222664504', '01222676543', '01222742757', '01222647452', '01222744504', '01222749989', '01222746383', '01222776543', '01222745635', '01222597452', '01222745363', '01222779984', '01224230436', '01222758870', '01221474412', '01221474414', '01222779987', '01224273013', '01222745527', '01222745458', '01222664501', '01222779986', '01224230496', '01221566963', '01221574336', '01224230433', '01222767541', '01222742927', '01222742916', '01222689984', '01222687452', '01222742760', '01224230525', '01222797541', '01224230439', '01224272937', '01224272982', '01224230449', '01224230506', '01222746381', '01224230477', '01224273037', '01223192327', '01223192308', '01223192263', '01223192287', '01223192392', '01224230491', '01221421994', '01221441994', '01222749929', '01222659986', '01224230473', '01223187393', '01224230530', '01223239872', '01224230488', '01223187389', '01223209885', '01224273039', '01224273091', '01224230570', '01224272955', '01224230483', '01224230513', '01224230482', '01223239867', '01224230507', '01224230517', '01224273038', '01224230490', '01222704501', '01222798870', '01223239866', '01222754501', '01222709929', '01222748870', '01224230528', '01222683542', '01222664503', '01222654503', '01222674504', '01222746482', '012227694504', '01222719989', '01221448178', '01222744503', '01223192284', '01223187417', '01223187414', '01222759929', '01221311993', '01221243882', '01221361991', '01223192328', '01221371991', '01221474413', '01221273883', '01222654501', '01222799985', '01221253884', '01220800593', '01222742949', '01222746459', '01222684503', '01224230460', '01224230565', '01224230465', '01221388068', '01221391442', '01221391244', '01221391199', '01221391155', '01224230476', '01221574346', '01221567020', '01222765541', '01222734504', '01221566961', '01221566960', '01223189591', '01221566971', '01223187435', '01221574354', '01223188887', '01221574324', '01221567011', '01222742946', '01222636543', '01222659984', '01222745943', '01222563542', '01224230564', '01224230568', '01224230541', '01220800748', '01222744780', '01224230541', '01224230539', '01224230534', '01222745479', '01222729989', '01222577452', '01222746397', '01222779985', '01222769989', '01222729987', '01222688541', '01222618542', '01224230435', '01224230487', '01223209889', '01223209891', '01223209888', '01224230504', '01224230486', '01224230469', '01224230510', '01222746461', '01224230443', '01222796541', '01224230512', '01222742798', '01222746421', '01222753541', '01222744501', '01222749984', '01222749985', '01222742888', '01222742934', '01222788870', '01222746472', '01222597541', '01222769542', '01222616541', '01222742704', '01224230437', '01222724501', '01221283886', '01222564542', '01222742908', '01222745934', '01222745495', '01222745859', '01224230516', '01224230500', '01221390965', '01221387937', '01221474387', '01221351991', '01221431994', '01221261996', '01222769984', '01223187402', '01223187398', '01223187384', '01223187403', '01223187406', '01224272944', '01221429366', '01221429367', '01221429369', '01221471994', '01221474403', '01221474402', '01221474406', '01221474407', '01221341993', '01221371993', '01223192410', '01223192453', '01221243885', '01221243887', '01224230464', '01223192393', '01223192394', '01223187395', '01224230458', '01224230459', '01222746380', '01222794503', '01222759989', '01220800701', '01222734543', '01222747452', '01223187394', '01223187387', '01221463494', '01221429368', '01221390254', '01221388836', '01221474404', '01221474405', '01222789986']
    #inv_list = ['01224230502', '01224273014', '01224272948', '01223187306', '01223187305', '01221392626', '01221392897', '01224272943', '01224273042', '01223187310', '01223187316', '01223181056', '01223181052', '01223187319', '01223192261', '01223187358', '01224230567', '01224273017', '01223187286', '01223180993', '01220553054', '01224273061', '01224273022', '01221392027', '01221389654', '01221390900', '01221387086', '01221387826', '01223187380', '01221399481', '01221393131', '01221393546', '01224273046', '01224273052', '01223239879', '01223239880', '01223239878', '01223239876', '01223192275', '01223192271', '01223192368', '01223192376', '01223192373', '01223181052', '01223181049', '01224273085', '01224273018', '01224273092', '01224273096', '01223180966', '01223180976', '01224230447', '01224230455', '01224230466', '01224230441', '01224230521', '01224272948', '01224273045', '01224272958', '01224230559', '01224273026', '01224273079', '01224272971', '01223192371', '01223187370', '01223192249', '01220800675', '01224272988']
    led_list = ['01222799986', '01220800574', '01224230529', '01222714543', '01224230467', '01223239869', '01224230576', '01222679989', '01222746396', '01222746350', '01224230549', '01223192391', '01221343888', '01224230577', '01222729929', '01224230493', '01224230501', '01224230526', '01221386983', '01223239875', '01223239870', '01221451993', '01221251996', '01224230542', '01224230434', '01224230480', '01224230484', '01224230485', '01224230470', '01222746456', '01222742834', '01223219133', '01223219131', '01223219130', '01223219129', '01223192247', '01222745462', '01221574357', '01222699986', '01222742200', '01222649984', '01222754504', '01222739929', '01224230571', '01222674503', '01224230527', '01224230569', '01222669986', '01223187397', '01223209886', '01222764501', '01222742912', '01224272962', '01222745935', '01222745933', '01222745947', '01222742969', '01222742878', '01222746463', '01223239874', '01223239873', '01222704503', '01223187431', '01223187430', '01224272938', '01222745939', '01222674501', '01220684147', '01222694501', '01222734501', '01223187419', '01223188270', '01223189537', '01222769929', '01221574356', '01224230509', '01224230472', '01224230478', '01222746390', '01222745510', '01222719929', '01221574359', '01222746366', '01222779929', '01223239865', '01223219128', '01224230518', '01223187436', '01223188269', '01222754503', '01222742885', '01222745938', '01222724503', '01222704504', '01222742752', '01222694503', '01224230546', '01221341991', '01224224149', '01220800623', '01220435025', '01224230511', '01224230515', '01224230461', '01224230533', '01224230451', '01223209883', '01223209884', '01223219126', '01223209881', '01223192283', '01222654504', '01222755541', '01222766541', '01222709541', '01222744754', '01222719541', '01222739541', '01222587543', '01222666541', '01221291991', '01223192386', '01222714503', '01224230446', '01224230532', '01222667543', '01222764503', '01222586543', '01222684504', '01222699987', '01222742956', '01222684501', '01222699984', '01224230479', '01221731209', '01224230558', '01224230495', '01222739987', '01222739986', '01221388812', '01221388441', '01221721213', '01221961213', '01223187386', '01223192395', '01224273086', '01222567452', '01222587452', '01221566970', '01222714504', '01222664504', '01222676543', '01222742757', '01222647452', '01222744504', '01222749989', '01222746383', '01222776543', '01222745635', '01222597452', '01222745363', '01222779984', '01224230436', '01222758870', '01221474412', '01221474414', '01222779987', '01224273013', '01222745527', '01222745458', '01222664501', '01222779986', '01224230496', '01221566963', '01221574336', '01224230433', '01222767541', '01222742927', '01222742916', '01222689984', '01222687452', '01222742760', '01224230525', '01222797541', '01224230439', '01224272937', '01224272982', '01224230449', '01224230506', '01222746381', '01224230477', '01224273037', '01223192327', '01223192308', '01223192263', '01223192287', '01223192392', '01224230491', '01221421994', '01221441994', '01222749929', '01222659986', '01224230473', '01224230530', '01223239872', '01224230488', '01224273039', '01224273091', '01224230570', '01224272955', '01224230483', '01224230513', '01224230482', '01223239867', '01224230507', '01224230517', '01224273038', '01224230490', '01222704501', '01222798870', '01223239866', '01222754501', '01222709929', '01222748870', '01224230528', '01222683542', '01222664503', '01222654503', '01222674504', '01222746482', '01222719989', '01221448178', '01222744503', '01223192284', '01223187417', '01223187414', '01222759929', '01221311993', '01221243882', '01221361991', '01223192328', '01221371991', '01221474413', '01221273883', '01222654501', '01222799985', '01221253884', '01220800593', '01222742949', '01222746459', '01222684503', '01224230460', '01224230565', '01224230465', '01221388068', '01221391442', '01221391244', '01221391199', '01221391155', '01224230476', '01221574346', '01221567020', '01222765541', '01222734504', '01221566961', '01221566960', '01223189591', '01221566971', '01223187435', '01221574354', '01223188887', '01221574324', '01221567011', '01222742946', '01222636543', '01222659984', '01222745943', '01222563542', '01224230564', '01224230568', '01224230541', '01220800748', '01222744780', '01224230541', '01224230539', '01224230534', '01222745479', '01222729989', '01222577452', '01222746397', '01222779985', '01222769989', '01222729987', '01222688541', '01222618542', '01224230435', '01224230487', '01223209889', '01223209891', '01223209888', '01224230504', '01224230486', '01224230469', '01224230510', '01222746461', '01224230443', '01222796541', '01224230512', '01222742798', '01222746421', '01222753541', '01222744501', '01222749984', '01222749985', '01222742888', '01222742934', '01222788870', '01222746472', '01222597541', '01222769542', '01222616541', '01222742704', '01224230437', '01222724501', '01221283886', '01222564542', '01222742908', '01222745934', '01222745495', '01222745859', '01224230516', '01224230500', '01221390965', '01221387937', '01221474387', '01221351991', '01221431994', '01221261996', '01222769984', '01223187402', '01223187398', '01223187384', '01223187403', '01223187406', '01224272944', '01221429366', '01221429367', '01221429369', '01221471994', '01221474403', '01221474402', '01221474406', '01221474407', '01221341993', '01221371993', '01223192410', '01223192453', '01221243885', '01221243887', '01224230464', '01223192393', '01223192394', '01223187395', '01224230458', '01224230459', '01222746380', '01222794503', '01222759989', '01220800701', '01222734543', '01222747452', '01223187394', '01223187387', '01221463494', '01221429368', '01221390254', '01221388836', '01221474404', '01221474405', '01222789986']
    inv_list = ['01224230502', '01224273014', '01221392626', '01221392897', '01224272943', '01224273042', '01223181056', '01223181052', '01224230567', '01224273017', '01223187286', '01223180993', '01220553054', '01224273061', '01224273022', '01221392027', '01221389654', '01221390900', '01221387086', '01221387826', '01223187380', '01221399481', '01221393131', '01221393546', '01224273046', '01224273052', '01223239879', '01223239880', '01223239878', '01223239876', '01223192368', '01223192373', '01223181052', '01224273085', '01224273018', '01224273096', '01223180966', '01223180976', '01224230447', '01224230455', '01224230466', '01224230441', '01224230521', '01224273045', '01224272958', '01224230559', '01224273026', '01224273079', '01224272971', '01220800675', '01224272988']
    print '<총 {0!r}개의 LED와 {1!r}개의 인버터 데이터 추출>\n'.format(len(led_list), len(inv_list))

    led_count = 0                               # lte 처리 갯수
    inv_count = 0
    start_time = datetime.datetime.now()        # 프로그램 시작값

    # 3. 입력된 list를 for문으로 하나씩 get함
    # 4. get한 list에서 얻은 한달치 value값을 비교
    # 5. 설정한 outlier값과 같거나 이상일시 txt로 log기록 및 print 출력
    ### 시작일 ~ 끝일까지 하루 data씩 get (get data 많으면 opentsdb가 timeout될 수 있기 때문에)
    for led in led_list:
        print led
        apt_cnt = 0
        #iterate every days and must be started w/ start of the day
        sum_value = 0
        tmp_time = datetime.datetime.now()
        end = first
        while is_past(end, last):
            start = end
            end = add_time(start, days=1)
            modem_holiday = is_weekend(start)
            query_result = tsdb_query(query, start, end, metric_in, led, modem_holiday)
            print query_result
            exit()
            for group in query_result:
                Find_Tags(metric_in, group['dps'], group['tags'])
            if apt_cnt == 1:
                total_led_apt_cnt += 1
                break
        led_count += 1
        print 'elapsed time: {0!s}, {1!s}'.format(datetime.datetime.now() - tmp_time, datetime.datetime.now() - start_time)
        print '<총 {0!r}/{1!r}개의 LED와 {2!r}/{3!r}개의 인버터 데이터 처리>\n'.format(led_count, len(led_list), inv_count, len(inv_list))
    print 'total elapsed time: {0!s}'.format(datetime.datetime.now() - start_time)
    
    # 3. 입력된 list를 for문으로 하나씩 get함
    # 4. get한 list에서 얻은 한달치 value값을 비교
    # 5. 설정한 outlier값과 같거나 이상일시 txt로 log기록 및 print 출력
    ### 시작일 ~ 끝일까지 하루 data씩 get (get data 많으면 opentsdb가 timeout될 수 있기 때문에)    
    for inv in inv_list:
        print inv
        apt_cnt = 0
        #iterate every days and must be started w/ start of the day
        tmp_time = datetime.datetime.now()
        end = first
        while is_past(end, last):
            start = end
            end = add_time(start, days=1)
            modem_holiday = is_weekend(start)
            query_result = tsdb_query(query, start, end, metric_in, inv, modem_holiday)
            for group in query_result:
                Find_Tags(metric_in, group['dps'], group['tags'])
            if apt_cnt == 1:
                total_inv_apt_cnt += 1
                break
        inv_count += 1
        print 'elapsed time: {0!s}, {1!s}'.format(datetime.datetime.now() - tmp_time, datetime.datetime.now() - start_time)
        print '<총 {0!r}/{1!r}개의 LED와 {2!r}/{3!r}개의 인버터 데이터 처리>\n'.format(led_count, len(led_list), inv_count, len(inv_list))
    
    Write_TagsLists(total_led_apt_cnt, total_inv_apt_cnt) # 기록
    print '일반건물_cnt 작성완료!'
    print 'total led : %d' % total_led_apt_cnt
    print 'total inv : %d' % total_inv_apt_cnt
    print 'total elapsed time: {0!s}'.format(datetime.datetime.now() - start_time)
