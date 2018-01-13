# -*- coding: utf-8 -*-
# Author : hwijinkim , https://github.com/jeonghoonkang

# openTSDB를 사용하기 위한 class
# last modified by 20180103

import sys
sys.path.insert(0, '/home/bornagain/kdatahub/EE-data-analysis/lib')
sys.path.insert(0, 'C:\Users\Be Pious\git\kdatahub\EE-data-analysis\lib')
sys.path.insert(0, 'C:\Users\Be Pious\git\kdatahub\EE-data-analysis\YKPK\KHJ\Jins_Utills')
sys.path.insert(0, '/home/bornagain/kdatahub/EE-data-analysis/lib/tools')
sys.path.insert(0, 'C:\Users\Be Pious\git\kdatahub\EE-data-analysis\lib\tools')

import json
import Jins_Utills
import in_list

HOST = '125.140.110.217'
PORT = 4242

if __name__ == "__main__":
    u, p, stime, etime, recent, metric, write_metric, val = Jins_Utills.parse_args()

    choice = input('1 = windows\n2 = linux\n')
    if choice == 1:
        with open('C:/Users/Be Pious/git/kdatahub/EE-data-analysis/lib/tools/count_list.json') as data_file:
            data_json = json.load(data_file)
    else:
        with open('/home/bornagain/kdatahub/EE-data-analysis/lib/tools/count_list.json') as data_file:
            data_json = json.load(data_file)

    inlist = in_list.total_vlist
    print " will prcessing %d lte numbers" %(len(inlist))
    
    ret = Jins_Utills.insert_op_rate(u, metric, write_metric, inlist, stime, etime, data_json, HOST, PORT)
    print ret
    exit()

    outfile = metric
    of = open (outfile+'_daily_opertaion_rate_1127.txt', 'w+')
    of.write(metric+'=')
    of.write(str(ret))
    of.close()
