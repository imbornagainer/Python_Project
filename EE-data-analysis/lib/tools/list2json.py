import sys
import os
import getopt
import copy
import json
from extract_xls import xls2list

import pip
installed_packages = [package.project_name for package in pip.get_installed_distributions()]
requested_packages = ['numpy']
for package in requested_packages:
    if package in installed_packages:
        pass
    else:
        print(package + ' must be already installed to use list2json.py')
        sys.exit(1)
import numpy as np

# pip3 install openpyxl, numpy


def help(err):
    print('usage:')
    print('\t-i iii : specify the input python script w/o .py')
    print('\t-l lll : specify the name of list')
    print('\t-r rrr : specify the reference json file')
    print('\t-s sss : specify the position of the sheet')
    print('\t-o ooo : specify the output json file')
    print('\tex) python list2json.py -i in_list -l led_list -r ref_list.xlsx -s 2 -o led_list.json')
    sys.exit(err)

if __name__ == '__main__':
    if sys.version_info < (3,6,0):
        sys.stderr.write('You need python 3.6 or later to run this script.\n')
        sys.exit(1)

    input_file   = ''
    output_file  = ''
    list_name    = 'valid_list'
    reference    = ''
    sheet        = 0
    input_module = None
    json_list    = { 'all' : [] }

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:l:r:s:o:')
    except getopt.GetoptError as err:
        print(err)
        help(2)

    if opts:
        for o, a in opts:
            if o == '-i':
                input_file = a
            elif o == '-l':
                list_name = a
            elif o == '-r':
                reference = a
            elif o == '-s':
                sheet = a
            elif o == '-o':
                output_file = a
            else:
                help(1)

    if not input_file or not output_file:
        help(1)

    # Rearrange columns to match your sheet
    column_ref = {
        'company': ['E', 'company'],
        'device': ['F', 'device_type'],
        'building': ['M', 'building'],
        'load': ['W', 'load'],
        'led_serial': ['S', '_mds_id'],
        'led_modem_serial': ['T', 'modem_num'],
        'led_size': ['R', 'size'],
        'inv_serial': ['AB', '_mds_id'],
        'inv_modem_serial': ['AC', 'modem_num'],
        'inv_size': ['Z', 'size'],
        'business': ['AL', 'business'],
        }

    tag_ref = {
        u'공장': 'factory', u'일반건물': 'office', u'마트': 'mart', u'공동주택': 'apt', u'대형마트': 'mart', u'기타': 'etc',  # 건물용도
        u'대기업': 'bigcompany', u'중견': 'middlecompany', u'중소': 'smallcompany', u'비영리법인': 'etc', u'해당없음': 'etc',
        u'병원': 'hospital',  # 사업장구분
        u'금속': 'metal', u'산업기타': 'industryEtc', u'건물기타': 'building_etc', u'제지목재': 'wood', u'요업': 'ceramic',
        u'백화점': 'departmentStore', u'섬유': 'fiber', u'학교': 'school', u'식품': 'food', u'화공': 'ceramic',
        u'상용': 'sangyong',  # 업종별-세부용도
        u'LED': 'led', u'인버터': 'inverter', u'형광등': 'heungwanglamp', u'메탈할라이드': 'metalhalide',  # 품목
        np.NaN: 'none', u'블로워': 'blower', u'컴프래서': 'compressor', u'펌프': 'pump', u'팬': 'fan',
        }

    if reference:
        xls = xls2list()
        ws = xls.load(reference, int(sheet))
        if not ws:
            print('Input file is invalid.')
            sys.exit(1)

        device_list = xls.convert(column_ref, tag_ref)
    else:
        device_list = {}

    print('Input: {0}, List: {1}, Output: {2}'.format(input_file, list_name, output_file))

    try:
        input_module = __import__(input_file)
    except:
        print('Input module is not a valid python script.')
        help(1)

    if list_name in dir(input_module):
        for el in getattr(input_module, list_name):
            if type('') == type(el):
                tmp = { 'modem_num': el }
            elif type(u'') == type(el):
                tmp = { 'modem_num': el.decode('utf-8') }
            elif type([]) == type(el):
                if type('') == type(el[0]):
                    tmp = { 'modem_num': el[0] }
                elif type(u'') == type(el[0]):
                    tmp = { 'modem_num': el[0].decode('utf-8') }
            else:
                print('Skip: Unknown type of list element, ', el)
            if tmp:
                if device_list:
                    ref = {}
                    for devs in device_list:
                        for dev in device_list[devs]:
                            if tmp['modem_num'].encode('utf-8') == dev[xls.column('modem_num')]:
                                ref = xls.decode(dev)
                    if ref:
                        json_list['all'].append(copy.deepcopy(ref))
                    else:
                        print(tmp['modem_num'], ': not in reference excel.')
                else:
                    json_list['all'].append(copy.deepcopy(tmp))
        print('Total {0!r} of devices counted.'.format(len(getattr(input_module, list_name))))
        print('Total {0!r} of devices extracted.'.format(len(json_list['all'])))
        with open(output_file, 'w') as f:
            json.dump(json_list, f, ensure_ascii=False)
    else:
        print('There is no ' + list_name + ' in ' + input_file)
