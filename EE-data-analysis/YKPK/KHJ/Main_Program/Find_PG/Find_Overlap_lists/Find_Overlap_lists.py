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
    
    #choice_num = raw_input("구하고 싶은 lists의 번호를 입력해주세요.\n\n1 - valid list\n2 - invalid list\n\n입력할 번호 : ")

#     w_count={}
#     
#     for lst in in_list.test_inv2:
#         try: w_count[lst] += 1
#         except: w_count[lst]=1
#     print w_count
#     
#     exit()
    
    #if choice_num == '1':
    led_list = ['01220800574', '01224230529', '01222714543', '01224230467', '01224230577', '01222699986', '01222742200', '01222669986', '01223187397', '01222674501', '01220684147', '01222694501', '01224230478', '01222719929', '01222694503', '01221341991', '01224230533', '01224230451', '01222755541', '01222766541', '01223192386', '01222714503', '01222586543', '01221731209', '01222739987', '01223192395', '01224273086', '01222647452', '01222779984', '01222664501', '01224230439', '01224230506', '01222746381', '01224230477', '01224273037', '01223192392', '01222749929', '01222659986', '01224230473', '01223187393', '01224230530', '01222798870', '01222742949', '01222769984', '01224272944', '01221471994', '01221243885', '01221243887', '01224230464', '01223187395', '01224230458', '01220800701', '01222747452', '01221463494', '01221429368']
    inv_list = ['01224230567', '01224273017', '01224273061', '01224273096', '01224230521', '01224230559']
    #led_valid_list = ['01222714543', '01222647452', '01222747452', '01222664501', '01224230478', '01224230477', '01222714503', '01221243887', '01221243885', '01222742949', '01221429368', '01224230506', '01223187395', '01223187397', '01224230439', '01222779984', '01224273086', '01222798870', '01222755541', '01224230529', '01222659986', '01222766541', '01222746381', '01220800701', '01222694503', '01224230530', '01224230533', '01224230473', '01222749929', '01220684147', '01222769984', '01224230577', '01224230451', '01224230458', '01222586543', '01222742200', '01222739987', '01222699986', '01223192395', '01223192392', '01222669986', '01222694501', '01221471994', '01221463494', '01221731209', '01222719929', '01224230467', '01224230464', '01224273037', '01224272944', '01222674501', '01221341991', '01220800574', '01223192386']

    for j in led_list:
        print j
        if j in in_list.valid_led:
            led_valid_list.append(j)
    print '\n# led_valid_list count = %s' % len(led_valid_list)
    print 'led_valid_list = %s\n' % led_valid_list
    
    for j in in_list.valid_inverter:
        if j in inv_list:
            inv_valid_list.append(j)
    print '# inv_valid_list count = %s' % len(inv_valid_list)
    print 'inv_valid_list = %s\n' % inv_valid_list

    print '# total_valid_list count= %s' % len(led_valid_list + inv_valid_list)
    print 'total_valid_list = %s' % (led_valid_list + inv_valid_list)
        
#     elif choice_num == '2':
    for i in inv_list:
        if i not in in_list.valid_inverter:
            invalid_list.append(i)
    print '\n# invalid_list count = %s' % len(invalid_list)
    print 'invalid_list = %s' % invalid_list
    
#     for i in in_list.valid_led:
#         if i not in led_list:
#             invalid_list.append(i)
#     print '\n# invalid_list count = %s' % len(invalid_list)
#     print 'invalid_list = %s' % invalid_list
# 
#     else:
#         print '잘못된 번호를 입력하셨습니다.\n옳바른 번호를 입력해주세요.'