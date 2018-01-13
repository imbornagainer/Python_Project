# -*- coding: utf-8 -*-
import openpyxl
import information_list
import numpy as np

def insert_tsdb(mdsid,size,factory,bigcompany):
    dictionary = {"공장": "factory", "일반건물": "office", "마트": "mart", "공동주택": "apt", "대형마트": "mart", "기타": "etc",  # 건물용도
                  "대기업": "bigcompany", "중견": "middlecompany", "중소": "smallcompany", "비영리법인": "etc", "해당없음": "etc",
                  "병원": "hospital",  # 사업장구분
                  "금속": "metal", "산업기타": "industryEtc", "건물기타": "building_etc", "제지목재": "wood", "요업": "ceramic",
                  "백화점": "departmentStore", "섬유": "fiber", "학교": "school", "식품": "food", "화공": "ceramic",
                  "상용": "sangyong",  # 업종별-세부용도
                  "LED": "led", "인버터": "inverter", "형광등": "heungwanglamp", "메탈할라이드": "metalhalide",  # 품목
                  np.NaN: "none", "블로워": "blower", "컴프래서": "compressor", "펌프": "pump", "팬": "fan", }
    tag=[]
    try:
        tag=led_tag[str(r[19].value)][2:5]
    except:
        if mdsid[0:2] == '06':
            try:
                tag=led_tag['00-' + mdsid[3:5] + mdsid[6:13]][2:5]
            except:
                try:
                    tag.append(dictionary[str(factory.encode('utf-8'))])
                except:
                    tag.append('none')
                try:
                    tag.append(dictionary[str(bigcompany.encode('utf-8'))])
                except:
                    tag.append('none')
                tag.append('none')
        else:
            try:
                tag.append(dictionary[str(factory.encode('utf-8'))])
            except:
                tag.append('none')
            try:
                tag.append(dictionary[str(bigcompany.encode('utf-8'))])
            except:
                tag.append('none')
            tag.append('none')
    tag.append('led')
    print str(mdsid)+","+str(size)+","+str(tag)

# main function
if __name__ == "__main__":

    ######
    #  '16EE_led_inverter.xlsx' 는 led,인버터 다 들어있는 엑셀파일!!
    excel_document = openpyxl.load_workbook('16EE_led_inverter.xlsx')
    sheet = excel_document.get_sheet_by_name(u'LED')  # 인버터 시트 가져오기!

    size = information_list.sizedic  # 사전계측용량 엑셀에서 가져온 딕셔너리형태 key: 사업장번호, value : 사전용량
    ###인버터는 16EE~ 엑셀에 사전계측용량이 안 들어 있기 때문에 따로 사전용량이 적혀진 엑셀에서 검색해서 사용해야한다.

    led_tag = information_list.led_tag  # 인버터관련 태그정보가 든 딕셔너리  key: MDSID, value : Tag정보들

    count=0
    for r in sheet.rows:
        rowindex=r[0].row
        try:
            size[str(r[1].value)] #사전계측용량 정보가 있는것 만 tsdb에 입력!!
            if r[18].value!=None:
                insert_tsdb(str(r[18].value),r[17].value,r[12].value,r[4].value)#mdsid,사전계측용량
                count=count+1
        except:
            None

    print "총 "+str(count) +"개의 데이터 존재 (06->00으로 바꾼경우) "

