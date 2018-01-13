#!/usr/bin/python
# -*- coding: utf-8 -*-

# MDSID 가 누리텔레콤서버에 존재하는지 데이터어떻게 출력되는지 확인하는 기본코드
import cx_Oracle



# update 15 minutes one TSDB
def updateMINONE(in_sttime, in_entime, in_mdsid):
        starttime = in_sttime
        endtime = in_entime
        mdsid = in_mdsid

        sql_tmp = "select ELE.LP_TIME, ELE.VALUE_00, ELE.VALUE_15, ELE.VALUE_30, ELE.VALUE_45, ECU.NAME, ECO.LOCATION, ECO.SIC, ELE.MDS_ID, ELE.DEVICE_SERIAL, ECU.CUSTOMERNO, ELE.CHANNEL from EMNV_LP_EM_VIEW  ELE join EMNV_CONTRACT_VIEW ECO on ELE.MDS_ID = ECO.MDS_ID join EMNV_CUSTOMER_VIEW ECU on ECO.CUSTOMERNO = ECU.CUSTOMERNO where (ELE.CHANNEL=1) and (ELE.LP_TIME between '%s' and '%s') and (ELE.MDS_ID='%s') order by ELE.MDS_ID ASC, ELE.LP_TIME ASC" %(starttime, endtime, mdsid)

        cur.execute(sql_tmp)
        for result in cur:
            print result

# main function
if __name__ == "__main__":
        count_n=0
        sttime = "2016110100"
        entime = "2016110123"

        #체크할 MDSID 리스트들
        black_list = ['00-360000185', '00-360000184', '00-360000262', '00-360000260', '00-360000247', '00-360000243', '00-360000132', '00-450083464', '00-450083524', '00-360000172', '00-360000170', '00-360000175', '00-360000232', '00-360000234', '00-360000237', '00-360000259', '00-360000258', '00-360000252', '00-360000250', '00-450083470', '00-360000283', '00-360000225', '00-360000222']

        con = cx_Oracle.connect('keti_user/keti1357!#@125.141.144.149/aimir')
        cur = con.cursor()
        real_no_oracle=[]
        for mds_id in black_list:
            print mds_id
            print '\n'
            updateMINONE(sttime, entime, mds_id)



        cur.close()
        con.close()


