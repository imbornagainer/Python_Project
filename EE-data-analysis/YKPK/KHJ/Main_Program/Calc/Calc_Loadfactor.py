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

def run(in_list, metric_op_name, device_type, host, port):

    start = '2016/07/01-00:00:00'
    end = '2017/07/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 365, metric_op_name, device_type, host, port, in_list)

    start = '2016/07/01-00:00:00'
    end = '2016/08/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 31, metric_op_name, device_type, host, port, in_list)

    start = '2016/08/01-00:00:00'
    end = '2016/09/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 31, metric_op_name, device_type, host, port, in_list)

    start = '2016/09/01-00:00:00'
    end = '2016/10/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 30, metric_op_name, device_type, host, port, in_list)

    start = '2016/10/01-00:00:00'
    end = '2016/11/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 31, metric_op_name, device_type, host, port, in_list)

    start = '2016/11/01-00:00:00'
    end = '2016/12/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 30, metric_op_name, device_type, host, port, in_list)

    start = '2016/12/01-00:00:00'
    end = '2017/01/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 31, metric_op_name, device_type, host, port, in_list)

    start = '2017/01/01-00:00:00'
    end = '2017/02/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 30, metric_op_name, device_type, host, port, in_list)

    start = '2017/02/01-00:00:00'
    end = '2017/03/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 28, metric_op_name, device_type, host, port, in_list)

    start = '2017/03/01-00:00:00'
    end = '2017/04/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 31, metric_op_name, device_type, host, port, in_list)

    start = '2017/04/01-00:00:00'
    end = '2017/05/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 30, metric_op_name, device_type, host, port, in_list)

    start = '2017/05/01-00:00:00'
    end = '2017/06/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 31, metric_op_name, device_type, host, port, in_list)

    start = '2017/06/01-00:00:00'
    end = '2017/07/01-00:00:00'
    Jins_Utills.yr_operation_rate(start, end, 30, metric_op_name, device_type, host, port, in_list)

if __name__ == "__main__":

    HOST = '125.140.110.217'
    PORT = 4242

    metric_op_name = 'zimsum:rc05_operation_rate_v6'
    device_type    = 'inverter'

    run(in_list, metric_op_name, device_type, HOST, PORT)
