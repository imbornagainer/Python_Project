import sys
import os
import getopt
import logging
import copy
import pickle
import json
import socket
import datetime
import time
import gzip
import shutil

#import pip
#installed_packages = [package.project_name for package in pip.get_installed_distributions()]
#requested_packages = ['requests', 'openpyxl', 'numpy']
#for package in requested_packages:
#    if package in installed_packages:
#        pass
#    else:
#        print(package + ' must be already installed to use tsdb_tool.py')
#        sys.exit(1)
import requests
from requests.adapters import HTTPAdapter

from requests.packages.urllib3.util.retry import Retry
#from requests.packages import urlilb3
#from urllib3.util.retry import Retry

from openpyxl import load_workbook
import numpy as np


class tsdb:
    def __init__(self, host='125.140.110.217', port=4242, test=False):
        self.host  = host
        self.port  = port
        self.test  = test
        self.api_query = 'http://{0!s}:{1!r}/api/query'.format(self.host, self.port)
        self.api_put   = 'http://{0!s}:{1!r}/api/put?summary'.format(self.host, self.port)
        self.column_name = {
            'metric':           'metric',
            'tags':             'tags',
            'dps':              'dps',
            'aggregateTags':    'aggregateTags',
            'device_serial':    '_mds_id',
            'modem_serial':     'modem_num',
            'holiday':          'holiday',
            'company':          'company',
            'device':           'device_type',
            'building':         'building',
            'load':             'load',
            'size':             'size',
            'business':         'business',
            'device_type':      'device_type',
            'serial':           '_mds_id',
            'modem_num':        'modem_num',
            'led_serial':       '_mds_id',
            'led_modem_serial': 'modem_num',
            'led_size':         'size',
            'inv_serial':       '_mds_id',
            'inv_modem_serial': 'modem_num',
            'inv_size':         'size',
            }

    def column(self, str):
        if str in self.column_name:
            return self.column_name[str]
        else:
            return ''

    def pack_dps(self, metric, dps, tags):
        pack = []
        tag = {'metric': metric, 'tags': tags}
        for dp in dps:
            sdp = copy.copy(tag)
            sdp['timestamp'] = int(dp.encode('utf8'))
            sdp['value'] = dps[dp]
            pack.append(sdp)
        return pack

    def requests_retry_session(self,
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

    def query(self, start, end, metric, tags):
        param = {}
        if start: param['start'] = start
        if end: param['end'] = end
        param['m'] = metric + '{'
        for i, tag in enumerate(tags):
            param['m'] += tag + '={0!s}'.format(tags[tag])
            if i < len(tags) - 1:
                param['m'] += ','
        param['m'] += '}'
        if 0:
            response = requests.get(self.api_query, params=param)
            if response.ok:
                return response.json()
            else:
                return []
        else:
            try:
                response = self.requests_retry_session().get(self.api_query, params=param, timeout=5)
            except Exception as x:
                pass
            else:
                if response.ok:
                    return response.json()
            return []

    def put(self, metric, dps, tags, file=None):
        # not yet supported test mode and file dump
        result = ''
        packed_data = self.pack_dps(metric, dps, tags)
        for i in xrange(0, len(packed_data), 8):
            tmp = json.dumps(packed_data[i:i+8])
            if 0:
                response = requests.post(self.api_put, data=tmp)
                if response.text: result = response.text
            else:
                try:
                    response = self.requests_retry_session().post(self.api_put, data=tmp, timeout=5)
                except Exception as x:
                    result = 'Request for put timeout'
                else:
                    if response.text: result = response.text
        return result

    def put_telnet(self, metric, dps, tags, file=None):
        result = ''
        if not self.test:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            retry = 5
            while 1:
                try:
                    sock.connect((self.host, self.port))
                except:
                    result = 'socket error: ' + self.host
                    retry -= 1
                    if retry > 0:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        continue
                    else:
                        result = 'skip this dps'
                        return result
                else:
                    break
            send = ''
            count = 0
            packed_data = self.pack_dps(metric, dps, tags)
        for dp in packed_data:
            if len(send) >= 1024:
                if not self.test:
                    sock.sendall(send.encode('utf-8'))
                if file: file.write(send)
                send = ''
            send += 'put'
            send += ' {0!s}'.format(dp['metric'])
            send += ' {0!r}'.format(dp['timestamp'])
            send += ' {0!r}'.format(dp['value'])
            if 'tags' in dp:
                for key in dp['tags']:
                    send += ' {0!s}'.format(key) + '={0!s}'.format(dp['tags'][key])
            send += '\n'
            count += 1
        if len(send) > 0:
            if not self.test:
                sock.sendall(send.encode('utf-8'))
            if file: file.write(send)
            send = ''
        if not self.test:
            sock.close()
        return result

    def ts2datetime(self, ts_str):
        return datetime.datetime.fromtimestamp(int(ts_str)).strftime('%Y/%m/%d-%H:%M:%S')

    def datetime2ts(self, dt_str):
        dt = datetime.datetime.strptime(dt_str, "%Y/%m/%d-%H:%M:%S")
        return time.mktime(dt.timetuple())

    def ts2str(self, ts):
        return str(int(ts))

    def str2datetime(self, dt_str):
        return datetime.datetime.strptime(dt_str, "%Y/%m/%d-%H:%M:%S")

    def datetime2str(self, dt):
        return dt.strftime('%Y/%m/%d-%H:%M:%S')

    def add_time(self, dt_str, days=0, hours=0, minutes=0, seconds=0):
        return self.datetime2str(self.str2datetime(dt_str) + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds))

    def is_past(self, dt_str1, dt_str2):
        return self.datetime2ts(dt_str1) < self.datetime2ts(dt_str2)

    def is_weekend(self, dt_str):
        if self.str2datetime(dt_str).weekday() >= 5: return '1'
        else: return '0'

class esc:
    def __init__(self, enable=False):
        self.aes = {
            'none':     '0',
            'black':    '30',
            'red':      '31',
            'green':    '32',
            'yellow':   '33',
            'blue':     '34',
            'magenta':  '35',
            'cyan':     '36',
            'white':    '37'
            }
        self.func = {}
        self.enable = enable
        for i in self.aes:
            self.aes[i] = '\033[' + self.aes[i] + 'm'
            self.func[i] = self.conv(i)
            setattr(self, i.lower(), self.func[i])
            setattr(self, i.upper(), self.func[i])

    def conv(self, aes):
        if self.enable:
            return lambda x: self.aes[aes] + str(x) + self.aes['none']
        else:
            return lambda x: str(x)
