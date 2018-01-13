# -*- coding: utf-8 -*-

# Python Ver : Python 2.7.14
# Author : hwijinkim , https://github.com/jeonghoonkang
# last modified by 20171120

# Excel에서 원하는 tag를 찾기 위한 class
# 배열 안에 중복 및 중복되지 않는 요소 찾기
# 사용자가 valid, invalid 리스트를 구할지 console창에서 입력으로 선택할 수 있음.
# ex) 1 - valid list, 2 - invalid list

#file.py
import sys
sys.path.insert(0, 'C:\Users\Be Pious\git\kdatahub\EE-data-analysis\lib')

import in_list

if __name__ == '__main__':
    
    # valid list
    led_valid_list = []
    inv_valid_list = []
    
    # invalid list
    invalid_list = []
    
    # total list
    total_list = []
    
    #led valid_cnt : 393    
    #inverter valid_cnt : 52
    
#     print len(in_list.excel_led_all_info_list)
#     exit()
#     for i in in_list.excel_led_all_info_list:
#         print len()
#         print i['sa_num']
#     exit()

#     print in_list.excel_led_all_info_list[0]['sa_num']
#     exit()
    
#     for i in range(len(in_list.excel_led_all_info_list)):
#         for a in in_list.excel_led_all_info_list[i]['sa_num']:
#             print a
#             exit()
#             if j in in_list.all_sanum_list:
#                 led_valid_list.append(j)        
#     print '\n# led_valid_list count = %s' % len(led_valid_list)
#     print 'led_valid_list = %s\n' % led_valid_list
#     
#     exit()
    
#     print in_list.excel_led_all_info_list[1]['sa_num']
#     exit()
    for i in sanum_total_valid_list:
        for j in in_list.excel_led_all_info_list:
            print a
    
    for a in in_list.excel_led_all_info_list:
        print a['sa_num']
        exit()
        if j in in_list.all_sanum_list:
            led_valid_list.append(j)
    print '\n# led_valid_list count = %s' % len(led_valid_list)
    print 'led_valid_list = %s\n' % led_valid_list
    
    
    for i in in_list.all_sanum_list:
        if i in in_list.excel_led_all_info_list:
            led_valid_list.append(i)
    print '\n# led_valid_list count = %s' % len(led_valid_list)
    print 'led_valid_list = %s\n' % led_valid_list

    for i in in_list.coolboil_list:
        if i in in_list.valid_inverter:
            inv_valid_list.append(i)
    print '# inv_valid_list count = %s' % len(inv_valid_list)
    print 'inv_valid_list = %s\n' % inv_valid_list

    print '# total_valid_list count= %s' % len(led_valid_list + inv_valid_list)
    print 'total_valid_list = %s' % (led_valid_list + inv_valid_list)
    
    