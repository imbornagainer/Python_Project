# -*- coding: utf-8 -*-

#엑셀(csv)파일들 간의 셀 비교 후 사업장아이디 또는 MDSID 를 공통으로하는 데이터 추출  + 한글을 영어로 변경하는 사전추가

import numpy as np
import pandas as pd
################################
#필요한 태그 요구사항!

# LED(형광등,메탈할라이드) - mdsid,사업장번호,건물정보(공장,마트),사업장정보(대기업,중소기업),세부용도(금속,섬유)
# INVERTER                 - mdsid,사업장번호,건물정보(공장,마트),사업장정보(대기업,중소기업),세부용도(금속,섬유),부하형태(팬,블로워)

###############################
led_id=[]
inverter_id=[]
saupjang_info=pd.read_csv("saupjang_info.csv")#사업장정보 csv 파일로 바꾼것!
inverter_info=pd.read_csv("inverter_info.csv")#EE자원 엑셀 중 인버터정보를 csv파일로 바꾼것
led_info=pd.read_csv("led_info.csv")#EE자원 엑셀 중 led정보를 csv파일로 바꾼것

list_info=pd.read_csv("insertlist.csv")#추천리스트400개

#사업장정보,엘이디인버터 엑셀들에서 얻을 수 있는 정보들을 영어로 바꾸기 위한 사전!
dictionary={"공장": "factory","일반건물":"office","마트":"mart","공동주택":"apt","대형마트":"mart","기타":"etc", #용도
                     "대기업":"bigcompany","중견":"middlecompany","중소":"smallcompany","비영리법인":"etc","해당없음":"etc","병원":"hospital", #사업장구분
                     "금속":"metal","산업기타":"industryEtc","건물기타":"building_etc","제지목재":"wood","요업":"ceramic",
                     "백화점":"departmentStore","섬유":"fiber","학교":"school","식품":"food","화공":"ceramic","상용":"sangyong",#세부용도
                     "LED":"led","인버터":"inverter","형광등":"heungwanglamp","메탈할라이드":"metalhalide",#품목
                     np.NaN:"none","블로워":"blower","컴프래서":"compressor","펌프":"pump","팬":"fan",}#부하형태

for id in list_info.iterrows():#추천리스트400개
    insertdata=[]
    if id[1][0]==1:#default1_led2_inverter3 -사업장엑셀에있는지(파란색),엘이디(빨간색),인버터(보라색)
        #사업장엑셀에 정보가 있는 경우
        info_data=saupjang_info[saupjang_info['사업장번호'] == id[1][2]]#사업장 아이디 일치하는 것 찾기
        # pandas 시리즈 객체의 value추출법! :sieries object.values[index]
        insertdata.append(id[1][1])       #mdsid
        insertdata.append(id[1][2])       #사업장번호
        insertdata.append(dictionary[info_data['품목'].values[0]]) #인버터,led정보
        insertdata.append(dictionary[info_data['용도'].values[0]]) # 공장 마트 정보
        insertdata.append(dictionary[info_data['사업장구분'].values[0]]) # 중소기업 대기업정보
        insertdata.append(dictionary[info_data['세부용도'].values[0]])  #섬유,금속 정보

        if dictionary[info_data['품목'].values[0]]=='led':
            led_id.append(insertdata)#엘이디 정보 모음리스트에 넣기

        else:#인버터의 경우 팬,블로워정보는 빈칸으로 두기(정보를 찾을 수 없어서)
            insertdata.append('none')#팬,블로워정보 -없을 때에는 none으로 대체함! 빈 데이터는 tsdb에 들어가지 않는다!!!!!!!!!!!!
            inverter_id.append(insertdata)#인버터 정보 모음리스트에 넣기

    elif id[1][0]==2:#엘이디 엑셀에 정보가 있는 경우
        info_data = led_info[led_info['계량기시리얼넘버'] == (id[1][1])]#mdsid로 검색해 일치하는 것 찾기!!
        insertdata.append(id[1][1])  # mdsid
        insertdata.append(id[1][2])       #사업장번호
        insertdata.append(dictionary[info_data['계측설비형태'].values[0]])#led/형광등/메탈할라이드
        insertdata.append(dictionary[info_data['건물용도'].values[0]])#공장,마트
        insertdata.append(dictionary[info_data['기업유형(사업장)'].values[0]])#대기업,중견기업

        info_data=saupjang_info[saupjang_info['사업장번호'] == id[1][2]]#사업장 아이디 일치하는 것 찾기->세부정보 채우기
        if len(info_data)>0:#사업장 엑셀에 정보가 있는 경우
            insertdata.append(dictionary[info_data['세부용도'].values[0]])
        else:
            insertdata.append('none')

        led_id.append(insertdata)#엘이디 정보 모음리스트에 넣기

    else:#인버터 엑셀에 정보가 있는 경우
        info_data = inverter_info[inverter_info['계량기시리얼넘버'] == str(id[1][1])]  #mdsid로 검색해 일치하는 것 찾기!!
        insertdata.append(id[1][1])  # mdsid
        insertdata.append(id[1][2])       #사업장번호
        insertdata.append('inverter')
        insertdata.append(dictionary[info_data['건물용도'].values[0]])#공장,마트
        insertdata.append('none')#인버터엑셀에는 대기업/중견/의 기업정보가 없다.사업장에서 검색해서 체워야함!!
        buha=dictionary[info_data['부하형태'].values[0]]

        info_data = saupjang_info[saupjang_info['사업장번호'] == id[1][2]]  # 사업장 아이디 일치하는 것 찾기
        if len(info_data) > 0:  # 사업장 엑셀에 정보가 있는 경우 세부용도추가
            insertdata.append(dictionary[info_data['세부용도'].values[0]])
            insertdata[3]=dictionary[info_data['사업장구분'].values[0]]#기업정보가 존재하면 빈값에서 값 바꿔주기
        else:
            insertdata.append('none')

        insertdata.append(buha)#순서를 지키기 위해 부하형태(팬,펌프,,)는 맨마지막에 넣기
        inverter_id.append(insertdata)#인버터 정보 모음리스트에 넣기

print "인버터 갯수 : "+ str(len(inverter_id))
for a in inverter_id:
    print a
print "led 갯수 : " + str(len(led_id))
for b in led_id:
    print b
###############################################################
#led_id,inverter_id 이 리스트를 이용해서 tsdb에 데이터 저장함! #
###############################################################
