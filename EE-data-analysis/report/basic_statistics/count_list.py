# -*- coding: utf-8 -*-
# Author : jeonghoonkang https://github.com/jeonghoonkang

from __future__ import print_function
import _out_list_0801_0101 as nodata

import sys
sys.path.append("../../lib")
import _input_list_17_0904 as inputd

# 0 ~ 14
keys = [01, 03, 05, 07, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
nodata_dict = {}
dup_list = []
for i in keys:
    nodata_dict[i] = []

tot = len(nodata.zero_list)
count = 0
allday = 153

def duple_check():
    all_list = inputd.modem_list
    #print (all_list)
    for k in all_list:
        exists_flag = 0
        if any(k[0] in v for v in all_list ):
            exists_flag += 1
        if exists_flag > 1 : 
            print (" 시리얼 아이디 중복존재 갯수 = %d " %exists_flag )
            print (k[0])
            dup_list.append(k[0])
    return dup_list
    
def rate_print():
    global count
    print ("total =", tot)
    for i in range(0,tot):
        val = nodata.zero_list[i][1]
        if val >= allday :
            nodata_dict[100].append(nodata.zero_list[i][0])
        elif val > (allday * 0.95) :
            nodata_dict[95].append(nodata.zero_list[i][0])
        elif val > (allday * 0.90) :
            nodata_dict[90].append(nodata.zero_list[i][0])
        elif val > (allday * 0.80) :
            nodata_dict[80].append(nodata.zero_list[i][0])
        elif val > (allday * 0.70) :
            nodata_dict[70].append(nodata.zero_list[i][0])
        elif val > (allday * 0.60) :
            nodata_dict[60].append(nodata.zero_list[i][0])
        elif val > (allday * 0.50) :
            nodata_dict[50].append(nodata.zero_list[i][0])
        elif val > (allday * 0.40) :
            nodata_dict[40].append(nodata.zero_list[i][0])
        elif val > (allday * 0.30) :
            nodata_dict[30].append(nodata.zero_list[i][0])
        elif val > (allday * 0.20) :
            nodata_dict[20].append(nodata.zero_list[i][0])
        elif val > (allday * 0.10) :
            nodata_dict[10].append(nodata.zero_list[i][0])
        elif val > (allday * 0.07) :
            nodata_dict[07].append(nodata.zero_list[i][0])
        elif val > (allday * 0.05) :
            nodata_dict[05].append(nodata.zero_list[i][0])
        elif val > (allday * 0.03) :
            nodata_dict[03].append(nodata.zero_list[i][0])
        elif val > (allday * 0.01) :
            nodata_dict[01].append(nodata.zero_list[i][0])
        count += 1

    for k,v in nodata_dict.items():
        print ( "  no %d %% day of all data = %d" %(k, len(v)))
    print ("  count = %d" %count)

if __name__ == "__main__" :

    duple_check()
    rate_print()

    f = open('_count_dict.out','w')
    f.write('no_data_dict = ')
    f.write(str(nodata_dict))
    f.write('\n\n')
    f.close()


