import sys
import os
import getopt
import logging
import copy
import json
import datetime
import gzip
import shutil

import pip
installed_packages = [package.project_name for package in pip.get_installed_distributions()]
requested_packages = []
for package in requested_packages:
    if package in installed_packages:
        pass
    else:
        print(package + ' must be already installed to use add_tags.py')
        sys.exit(1)
from tsdb_tool import tsdb, esc


def help(err):
    print('usage:')
    print('\t-i iii : specify the input metric')
    print('\t-o ooo : specify the output metric')
    print('\t-r rrr : specify the reference json file')
    print('\t-s sss : specify the start datetime by sss=YYYY/MM/DD')
    print('\t-e eee : specify the duration of days, 0 for days until now')
    print('\t-t     : turn on test mode, data points will not be put')
    print('\t-d     : turn on debug logging')
    print('\tex) python add_tags.py -i rc04_simple_data_v3 -o rc04_simple_data_v3_tags_added -r ref_list.json -e 1 -t')
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
    test_mode     = False
    log_level     = logging.INFO
    esc_enable    = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:r:s:e:tdq')
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
            elif o == '-t':
                test_mode = True
            elif o == '-d':
                log_level = logging.DEBUG
            elif o == '-q':
                esc_enable = True
            else:
                help(1)

    if not input_metric or not output_metric or not reference:
        help(1)

    # Init logging
    ESC = esc(esc_enable)
    log = init_logging(__name__, os.path.splitext(os.path.basename(__file__))[0], log_level)

    first = start_date + '-00:00:00'
    last  = first
    metric_in  = 'none:' + input_metric
    metric_out = output_metric
    out_file   = open(metric_out, 'w')

    tsdb = tsdb('125.140.110.217', 4242, test_mode)

    if duration == 0:
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

    log.info(ESC.GREEN('Input: {0!s}, Output: {1!s}, reference: {2!s}, start: {3!s}, end: {4!s}'.format(input_metric, output_metric, reference, first, last)))
    for key in device_list:
        log.info(ESC.GREEN('Total {0!r} of {1!s} extracted.'.format(len(device_list[key]), key)))

    #2. query data points from tsdb using modem number
    #3. add tags and put data points to tsdb
    start_time = datetime.datetime.now()
    for key in device_list:
        dev_count = 0
        for dev in device_list[key]:
            log.info(ESC.BLUE('modem_num: {0!s}'.format(dev[tsdb.column('modem_num')])))
            log.debug(ESC.NONE(dev))
            #iterate every days and must be started w/ start of the day
            tmp_time = datetime.datetime.now()
            end = first
            while tsdb.is_past(end, last):
                start = end
                end = tsdb.add_time(start, days=1)
                dev[tsdb.column('holiday')] = tsdb.is_weekend(start)
                query_result = tsdb.query(start, end, metric_in, {'modem_num': dev[tsdb.column('modem_num')]})
                if query_result:
                    for group in query_result:
                        tsdb.put_telnet(metric_out, group['dps'], dev, out_file)
            dev_count += 1
            log.info(ESC.CYAN('Elapsed time: {0!s} / {1!s}'.format(datetime.datetime.now() - tmp_time, datetime.datetime.now() - start_time)))
            log.info(ESC.CYAN('Total {0!r}/{1!r} of {2!s} proccessed.'.format(dev_count, len(device_list[key]), key)))

    log.info(ESC.GREEN('Total elapsed time: {0!s}'.format(datetime.datetime.now() - start_time)))

    #4. make the file for batch importing using CLI
    if out_file:
        out_file.close()
        with open(metric_out, 'rb') as f_in, gzip.open(metric_out + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
