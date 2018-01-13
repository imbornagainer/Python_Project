import sys
import os
import getopt
import copy
import json


def help(err):
    print('usage:')
    print('\t-r rrr : specify the reference json file')
    print('\tex) python ex_json2list.py -i led_list.json')
    sys.exit(err)

if __name__ == '__main__':
    if sys.version_info < (3,6,0):
        sys.stderr.write('You need python 3.6 or later to run this script.\n')
        sys.exit(1)

    reference     = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'r:')

    except getopt.GetoptError as err:
        print(err)
        help(2)

    if opts:
        for o, a in opts:
            if o == '-r':
                reference = a
            else:
                help(1)

    if not reference:
        help(1)
        
    print (reference)

    device_list = {}
    with open(reference) as file:
        device_list = json.load(file)
    if not device_list:
        print('Reference json file is invalid.')
        sys.exit(1)

    for devs in device_list:
        for dev in device_list[devs]:
            #print(dev)
            pass
        print('Total {0!r} of {1!r} devices extracted.'.format(len(device_list[devs]), devs))


    # Example of getting input list containing only modem_num
    input_list = {}
    for devs in device_list:
        input_list[devs] = []
        for dev in device_list[devs]:
            input_list[devs].append(copy.deepcopy(dev['modem_num']))
        print('{0!s}_list = '.format(devs), input_list[devs])

    # Example of counting input list
    for devs in device_list:
        print('{0!s}_list_num = {1!s}'.format(devs, len(device_list[devs])))
