import sys
import os
import getopt
import logging
import copy
import json
import datetime
import gzip
import shutil

#import pip
#installed_packages = [package.project_name for package in pip.get_installed_distributions()]
#requested_packages = []
#for package in requested_packages:
#    if package in installed_packages:
#        pass
#    else:
#        print(package + ' must be already installed to use count_tsdb.py')
#        sys.exit(1)

from tsdb_tool import tsdb, esc


def help(err):
    print('usage:')
    print('\t-i iii : specify the input metric')
    print('\t-o ooo : specify the output metric')
    print('\t-r rrr : specify the reference json file')
    print('\t-x     : turn on substraction mode')
    print('\t-s sss : specify the start datetime by sss=YYYY/MM/DD')
    print('\t-e eee : specify the duration of days, 0 for days until now')
    print('\t-t     : turn on test mode, data points will not be put')
    print('\t-d     : turn on debug logging')
    print('\t-q     : turn on logging w/ ANSI color')
    print('\tex) python count_tsdb.py -i rc05_operation_rate_v6 -o rc05_operation_rate_v6_count -r count_list -e 1 -t')
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
    sub_mode      = False
    start_date    = '2016/07/01'
    duration      = 0
    test_enable   = False
    log_level     = logging.INFO
    esc_enable    = False

    # Init logging
    ESC = esc(esc_enable)
    log = init_logging(__name__, os.path.splitext(os.path.basename(__file__))[0], log_level)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:r:s:e:txdq')
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
            elif o == '-x':
                sub_mode = True
                log.info(ESC.CYAN("************** SUBSTRACTION MODE ******************"))
            elif o == '-s':
                start_date = a
            elif o == '-e':
                duration = a
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



    first = start_date + '-00:00:00'
    last  = first
    metric_in  = 'none:' + input_metric
    metric_out = output_metric
    out_file   = open(metric_out, 'w')

    tsdb = tsdb('125.140.110.217', 4242, test_enable)

    if int(duration) == 0:
        last = tsdb.datetime2str(datetime.datetime.now())
    else:
        last = tsdb.add_time(first, days=int(duration))

    with open(reference) as file:
        ref_list = json.load(file)
    if not ref_list:
        log.error(ESC.RED('Reference json file is invalid.'))
        sys.exit(1)

    log.info(ESC.GREEN('Input: {0!s}, Output: {1!s}, Reference: {2!s}, start: {3!s}, end: {4!s}'.format(input_metric, output_metric, reference, first, last)))

    #1. reference list parsing
    #2. query data points from tsdb w/ tags
    #3. count dps, add tags and put data points to tsdb
    start_time = datetime.datetime.now()
    for dev_type in ref_list:    #  led, inverter
        log.info(ESC.GREEN('Device Type: {0!r}'.format(dev_type)))
        tag_list = ref_list[dev_type]['tags']
        for key in tag_list: # key is total, buildlng, device_type.... or
            for tag in tag_list[key]: # tag --> building.office etc
                tmp_time = datetime.datetime.now()
                #iterate every days and must be started w/ start of the day
                end = first
                while tsdb.is_past(end, last):
                    start = end
                    end = tsdb.add_time(start, days=1)
                    device_list = []
                    result_dps  = {}
                    result_tags = { 'device_type': dev_type }
                    #result_tags[tsdb.column('holiday')] = tsdb.is_weekend(start)
                    #result_tags[key] = tag
                    for i in range(int(24*60 / 15)):
                        ts = tsdb.ts2str(tsdb.datetime2ts(tsdb.add_time(start, minutes=i*15)))
                        if sub_mode: #옵션 -x
                            result_dps[ts] = int(tag_list[key][tag])
                        else:
                            result_dps[ts] = 0

                    if tag == 'total':
                        query_tags = {'device_type': dev_type}
                        continue # dont't count this tag total is just for all
                    else: # Be sure that dicts have differenct pointer, different instance
                        query_tags = {'device_type': dev_type, key: tag}
                        result_tags = {'device_type': dev_type, key: tag}
                        if key == 'building' or key == 'load' :
                            result_tags['totcount'] = 'total'
                        else:
                            result_tags['totcount'] = 'each'

                    query_result = tsdb.query(start, tsdb.add_time(end, minutes=-1), metric_in, query_tags) # none dps 갯수 읽기
                    if len(query_result) < 1:
                        log.info(ESC.NONE(" return no data by query from TSDB"))
                        log.info(ESC.NONE(query_tags))

                    if query_result:
                        for group in query_result:
                            if group['tags']['modem_num'] in device_list:
                                log.warning(ESC.YELLOW('modem_num: {0!r} is in device_list'.format(group['tags']['modem_num'])))
                            else:
                                device_list.append(group['tags']['modem_num'])
                            for i in range(int(24*60 / 15)):
                                ts = tsdb.ts2str(tsdb.datetime2ts(tsdb.add_time(start, minutes=i*15)))
                                if ts in group['dps']:
                                    if sub_mode:
                                        result_dps[ts] -= 1
                                    else:
                                        result_dps[ts] += 1
                        log.debug(ESC.NONE(result_dps))
                        while True:
                            result = tsdb.put_telnet(metric_out, result_dps, result_tags, out_file)
                            if result != '':
                                log.warning(ESC.YELLOW('Error on put: ' + result))
                            else:
                                break
                log.info(ESC.CYAN('Elapsed time: {0!s}: {1!s} / {2!s}'.format(tag, datetime.datetime.now() - tmp_time, datetime.datetime.now() - start_time)))

    log.info(ESC.GREEN('Total elapsed time: {0!s}'.format(datetime.datetime.now() - start_time)))

    #4. make the file for batch importing using CLI
    if out_file:
        out_file.close()
        with open(metric_out, 'rb') as f_in, gzip.open(metric_out + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
