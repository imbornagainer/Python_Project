
import sys
import os
import getopt
import logging
import copy
import json
import datetime
import gzip
import shutil

sys.path.insert(0, '../')
import in_list

import pip
installed_packages = [package.project_name for package in pip.get_installed_distributions()]
requested_packages = []
for package in requested_packages:
    if package in installed_packages:
        pass
    else:
        print(package + ' must be already installed to use copy_tsdb.py')
        sys.exit(1)
from tsdb_tool import tsdb, esc
from tsdb_tool import tsdb as outtsdb

def dataProcess(tsdb, option, dps, tags, start):
    result_dps  = {}
    result_tags = copy.deepcopy(tags)
    if 'hol' in option and option['hol']:
        result_tags[tsdb.column('holiday')] = tsdb.is_weekend(start)
    if 'bin' in option and option['bin']:
        for i in range(int(24*60 / 15)):
            ts = tsdb.ts2str(tsdb.datetime2ts(tsdb.add_time(start, minutes=i*15)))
            if ts in dps:
                result_dps[ts] = option['max']
            else:
                result_dps[ts] = option['min']
    elif 'top' in option or 'bot' in option:
        for i in range(int(24*60 / 15)):
            ts = tsdb.ts2str(tsdb.datetime2ts(tsdb.add_time(start, minutes=i*15)))
            if ts in dps:
                pass #result_dps[ts] = option['max']
                if 'top' in option and option['top'] <= float(dps[ts]):
                    result_dps[ts] = option['max']
                elif 'bot' in option and option['bot'] >= float(dps[ts]):
                    result_dps[ts] = option['min']
                else:
                    result_dps[ts] = dps[ts]
            else:
                if 'fil' in option:
                    result_dps[ts] = option['fil']
    else:
        if 'fil' in option:
            for i in range(int(24*60 / 15)):
                ts = tsdb.ts2str(tsdb.datetime2ts(tsdb.add_time(start, minutes=i*15)))
                if ts in dps:
                    result_dps[ts] = dps[ts]
                else:
                    result_dps[ts] = option['fil']
        else:
            result_dps = copy.deepcopy(dps)
    return result_dps, result_tags

def checkDataProcessOptions(option):
    if 'hol' in option:
        print('Option {0!r} : {1!r}'.format('hol', option['hol']))
        pass
    if 'bin' in option and option['bin']:
        print('Option {0!r} : {1!r}'.format('bin', option['bin']))
        if 'top' in option or 'bot' in option or 'fil' in option:
            return False
    if 'max' not in option:
        option['max'] = 1.0
    if 'min' not in option:
        option['min'] = 0.0
    if option['max'] < option['min']:
        return False
    if 'top' in option and option['top'] > option['max']:
        return False
    if 'bot' in option and option['bot'] < option['min']:
        return False
    return True

def help(err):
    print('usage:')
    print('\t-i iii : specify the input metric')
    print('\t-o ooo : specify the output metric')
    print('\t-r rrr : specify the reference json file')
    print('\t-s sss : specify the start datetime by sss=YYYY/MM/DD')
    print('\t-e eee : specify the duration of days, 0 for days until now')
    print('\t-m mmm : specify the option of data processing')
    print('\t   hol : add holiday tag')
    print('\t   bin : process binary transform')
    print('\t   max : specify max value by max=value')
    print('\t   min : specify min value by min=value')
    print('\t   top : specify top bound by top=value')
    print('\t   bot : specify bottom bound by bot=value')
    print('\t   fil : fill at empty timestamp by fil=value')
    print('\t-t     : turn on test mode, data points will not be put')
    print('\t-d     : turn on debug logging')
    print('\t-q     : turn on logging w/ ANSI color')
    print('\tex) python copy_tsdb.py -i rc05_operation_tag_v3 -o rc05_operation_tag_v3_copied -r ref_list.json -e 1 -t')
    sys.exit(err)

def init_logging(name, file, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:\t%(message)s'))
    logger.addHandler(ch)
    ch = logging.FileHandler("{0}.log".format(file), mode='w')
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:\t%(message)s'))
    logger.addHandler(ch)
    return logger

if __name__ == '__main__':
    if sys.version_info < (3,6,0):
        sys.stderr.write('You need python 3.6 or later to run this script.\n')
        sys.exit(1)

    input_metric  = ''
    output_metric = ''
    reference     = ''
    start_date    = '2016/07/01'
    duration      = 0
    option        = {}
    test_enable   = False
    log_level     = logging.INFO
    esc_enable    = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:r:s:e:m:tdq')
    except getopt.GetoptError as err:
        print(err)
        help(2)

    if opts:
        for o, a in opts:
            if o == '-i':
                input_metric = a
            elif o == '-o':
                output_metric = a
            elif o == '-r':
                reference = a
            elif o == '-s':
                start_date = a
            elif o == '-e':
                duration = a
            elif o == '-m':
                m = a.split('=')
                if m[0] == 'hol':
                    option[m[0]] = True
                elif m[0] == 'bin':
                    option[m[0]] = True
                elif m[0] == 'max' and len(m) > 1:
                    option[m[0]] = float(m[1])
                elif m[0] == 'min' and len(m) > 1:
                    option[m[0]] = float(m[1])
                elif m[0] == 'top' and len(m) > 1:
                    option[m[0]] = float(m[1])
                elif m[0] == 'bot' and len(m) > 1:
                    option[m[0]] = float(m[1])
                elif m[0] == 'fil' and len(m) > 1:
                    option[m[0]] = float(m[1])
                else:
                    help(1)
            elif o == '-t':
                test_enable = True
            elif o == '-d':
                log_level = logging.DEBUG
            elif o == '-q':
                esc_enable = True
            else:
                help(1)

    if not input_metric or not output_metric or not reference:
        help(1)
    try:
        tmp = open(reference)
        tmp.close()
    except:
        print('No such file or directory: {0}'.format(reference))
        help(1)

    if not checkDataProcessOptions(option):
        print('This combination of options not supported: {0}'.format(option))
        help(1)

    # Init logging
    ESC = esc(esc_enable)
    log = init_logging(__name__, os.path.splitext(os.path.basename(__file__))[0], log_level)

    first = start_date + '-00:00:00'
    last  = first
    metric_in  = 'none:' + input_metric
    metric_out = output_metric

    ofile   = './out/' + metric_out +'.txt' 
    out_file   = open( ofile , 'w')

    tsdb = tsdb('125.140.110.217', 4242, test_enable)
    outtsdb = outtsdb('tinyos.asuscomm.com', 44242, test_enable)

    if int(duration) == 0:
        last = tsdb.datetime2str(datetime.datetime.now())
    else:
        last = tsdb.add_time(first, days=int(duration))

    #1. get tags from json file created by extract_xls
    device_list = {}
    with open(reference) as file:
        device_list = json.load(file)
    if not device_list:
        log.error(ESC.RED('Reference json file is invalid.'))
        sys.exit(1)
    super_tag = {}
    for key in device_list:
        if key == 'superTag':
            log.info(ESC.CYAN('Super tags {0!r} will be added.'.format(device_list[key])))
            super_tag = device_list[key]
            device_list.pop(key)
            break
    for key in device_list:
        for skey in super_tag:
            for dev in device_list[key]:
                dev[skey] = super_tag[skey]

    log.info(ESC.GREEN('Input: {0!s}, Output: {1!s}, start: {2!s}, end: {3!s}'.format(input_metric, output_metric, first, last)))
    log.info(ESC.GREEN('Referenc: {0!s}, Option: {1!s}'.format(reference, option)))
    for key in device_list:
        log.info(ESC.GREEN('Total {0!r} of {1!s} extracted.'.format(len(device_list[key]), key)))

    #2. query data points from tsdb using modem number
    #3. add tags and put data points to tsdb
    start_time = datetime.datetime.now()
    for key in device_list: # 'led', 'inverter' key in the ref json file
        dev_count = 0
        for dev in device_list[key]: # 'tags' key in ref json file
            #log.info(ESC.BLUE('modem_num: {0!s}'.format(dev[tsdb.column('modem_num')])))
            log.debug(ESC.NONE(dev))
            #iterate every days and must be started w/ start of the day
            tmp_time = datetime.datetime.now()
            end = first
            while tsdb.is_past(end, last):
                start = end
                end = tsdb.add_time(start, days=1)
                for tag_i in (device_list[key][dev]): #buidling, detail
                    t_name = tag_i
                    for tag_ii in (device_list[key][dev][tag_i]):
                        print (tag_ii)
                        tags = { 'device_type' : key , t_name : tag_ii }
                        log.debug(ESC.NONE(tags))
                        query_result = tsdb.query(start, tsdb.add_time(end, minutes=-1), metric_in, tags )
                        #if tag_ii == 'office' :
                        #    print (query_result)
                        #    exit()

                        #print (query_result)
                        #query_result = tsdb.query(start, tsdb.add_time(end, minutes=-1), metric_in, {'modem_num': dev[tsdb.column('modem_num')] } )
                        if query_result:
                            processed = False
                            for group in query_result:
                                if processed:
                                    log.warning(ESC.YELLOW('Another group exist:'))
                                    #log.warning(ESC.YELLOW('Another group exist: {0!r}'.format(group)))
                                    #exit( "processed error ")
                                    #break #only one group will be process
                                while True:
                                    # data processing should be performed by the unit of 1 day
                                    dps, tags = dataProcess(tsdb, option, group['dps'], tags, start)
                                    result = ''
                                    result = outtsdb.put_telnet(metric_out, dps, tags, out_file)
                                    if result != '':
                                        log.warning(ESC.YELLOW('Error on put: ' + result))
                                    else:
                                        break
                                processed = True
                dev_count += 1
            log.info(ESC.CYAN('Elapsed time: {0!s} / {1!s}'.format(datetime.datetime.now() - tmp_time, datetime.datetime.now() - start_time)))
            log.info(ESC.CYAN('Total {0!r}/{1!r} of {2!s} processed.'.format(dev_count, len(device_list[key]), key)))

    log.info(ESC.GREEN('Total elapsed time: {0!s}'.format(datetime.datetime.now() - start_time)))

    #4. make the file for batch importing using CLI
    if out_file:
        out_file.close()
        with open(ofile, 'rb') as f_in, gzip.open(ofile + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
