# -*- coding: utf-8 -*-
import openpyxl
import information_list


def insert_tsdb(mdsid,size,factory,fan_pump):
    factory_dic = {'공장': 'factory', '일반건물': 'office'}
    fan_pump_dic = {'팬': 'fan', '펌프': 'pump', '블로워': 'blower', '콤프레셔': 'compressor', '컴프래서': 'compressor'}

    tag=[]
    try:
        tag=inverter_tag[str(r[19].value)][2:5]
    except:
        if mdsid[0:2] == '06':
            try:
                tag=inverter_tag['00-' + mdsid[3:5] + mdsid[6:13]][2:5]
            except:
                try:
                    tag.append(factory_dic[str(factory.encode('utf-8'))])
                except:
                    None
        else:
            try:
                tag.append(factory_dic[str(factory.encode('utf-8'))])
            except:
                None

    try:
        tag.append(fan_pump_dic[str(fan_pump.encode('utf-8'))])
    except:
        None
    tag.append('inverter')
    print str(mdsid)+","+str(size)+","+str(tag)

# main function
if __name__ == "__main__":

    ######
    #  '16EE_led_inverter.xlsx' 는 led,인버터 다 들어있는 엑셀파일!!
    excel_document = openpyxl.load_workbook('16EE_led_inverter.xlsx')
    sheet = excel_document.get_sheet_by_name(u'INVERTER')  # 인버터 시트 가져오기!

    size = information_list.sizedic  # 사전계측용량 엑셀에서 가져온 딕셔너리형태 key: 사업장번호, value : 사전용량
    ###인버터는 16EE~ 엑셀에 사전계측용량이 안 들어 있기 때문에 따로 사전용량이 적혀진 엑셀에서 검색해서 사용해야한다.

    inverter_tag = information_list.inverter_tag  # 인버터관련 태그정보가 든 딕셔너리  key: MDSID, value : Tag정보들

    count=0
    for r in sheet.rows:
        rowindex=r[0].row
        try:
            size[str(r[1].value)] #사전계측용량 정보가 있는것 만 tsdb에 입력!!
            if r[19].value!=None:
                insert_tsdb(str(r[19].value),size[str(r[1].value)],r[12].value,r[14].value)#mdsid,사전계측용량
                count=count+1
        except:
            None

    print "총 "+str(count) +"개의 데이터 존재 (06->00으로 바꾼경우) "

