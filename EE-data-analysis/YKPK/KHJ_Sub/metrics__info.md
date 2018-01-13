### OpenTSDB Metric에 대한 info
##### OpenTSDB URL : http://125.140.110.217:4242

### 해야할일
#### metric : rc04_simple_data_v3
* 오라클DB 데이터를 그대로 복사하여 옮김
* LTE 모뎀번호만 Tag로 저장함 
* 다음 메트릭 만들때 해야할일
  * 측정 이상한 데이터 삭제

#### metric : rc05_operation_tag_v3 (완료)
  ```
* 실전용 metric (완료)
		* 시작시간 : 2017-11-08 17:12:05
		* 소요시간 : 1시간 08분 07초
		* copy한 data 갯수 : 455개
		* excel_list만 copy
		* excel에 세부사항 추가
		* outlier(값 100이상) 제거 및 가동률 계산(value/max_value)*100
		* rc05_excel_copy_tag_v4에서 list에 가동률 계산한 metric(원하는 modem_list만 뽑아서 copy - rm_outlier_add_tag_daily_onelist_input_v0.1.py)
		* list와 시간을 기준으로 get함
  		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
  	* rc05_excel_copy_tag_v4에서 data를 get한 후 가동률 구한 후 copy (밑은 copy된 tag lists)
  		* modem_num 	- 모뎀시리얼넘버
  		* _mds_id   	- 계량기시리얼넘버
  		* company   	- 기업유형(사업장)
  		* building  	- 건물용도
  		* load      	- 부하형태
  		* device_type	- 계측 설비형태
  		* holiday		- 주일(토,일)
		* detail		- 세부사항
  
  * 파일위치 : rm_outlier_add_tag_daily_onelist_input_v0.1.py

building - u'공장': 'factory', u'일반건물': 'office', u'마트': 'mart', u'병원': 'hospital', u'전자대리점': 'mart', u'공동주택': 'apt', u'대형마트': 'mart', u'기타': 'etc'

company - u'대기업': 'bigcompany', u'중견': 'middlecompany', u'중소': 'smallcompany', u'비영리법인': 'etc', u'해당없음': 'etc'

device_type - u'LED': 'led', u'인버터': 'inverter', u'형광등': 'heungwanglamp', u'메탈할라이드': 'metalhalide'

load - np.NaN: 'none', u'블로워': 'blower', u'컴프래서': 'compressor', u'펌프': 'pump', u'팬': 'fan'

```

#### metric : rc05_operation_tag_v2 (완료)
  ```
* 실전용 metric (완료)
		* 시작시간 : 2017-11-08
		* 소요시간 : 1시간 04분 14초
		* copy한 data 갯수 : 455개
		* excel_list만 copy
		* excel에 병원, 학교, 마트 추가
		* outlier(값 100이상) 제거 및 가동률 계산(value/max_value)*100
		* rc05_excel_copy_tag_v4에서 list에 가동률 계산한 metric(원하는 modem_list만 뽑아서 copy - rm_outlier_add_tag_daily_onelist_input_v0.1.py)
		* list와 시간을 기준으로 get함
  		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
  	* rc05_excel_copy_tag_v4에서 data를 get한 후 가동률 구한 후 copy (밑은 copy된 tag lists)
  		* modem_num 	- 모뎀시리얼넘버
  		* _mds_id   	- 계량기시리얼넘버
  		* company   	- 기업유형(사업장)
  		* building  	- 건물용도
  		* load      	- 부하형태
  		* device_type	- 계측 설비형태
  		* holiday	- 주일(토,일)
  
  * 파일위치 : rm_outlier_add_tag_daily_onelist_input_v0.1.py

building - u'공장': 'factory', u'일반건물': 'office', u'마트': 'mart', u'병원': 'hospital', u'전자대리점': 'mart', u'공동주택': 'apt', u'대형마트': 'mart', u'기타': 'etc'

company - u'대기업': 'bigcompany', u'중견': 'middlecompany', u'중소': 'smallcompany', u'비영리법인': 'etc', u'해당없음': 'etc'

device_type - u'LED': 'led', u'인버터': 'inverter', u'형광등': 'heungwanglamp', u'메탈할라이드': 'metalhalide'

load - np.NaN: 'none', u'블로워': 'blower', u'컴프래서': 'compressor', u'펌프': 'pump', u'팬': 'fan'

```

#### metric : rc05_excel_copy_tag_v4 (완료)
  ```
* 실전용 metric (완료)
		* 시작시간 : 2017-11-07 23:18:05
		* 소요시간 : 48분 14초
		* copy한 data 갯수 : 455개
		* excel_list만 copy
		* excel에 병원, 학교, 마트 추가
		* outlier(값 100이상) 제거
		* rc05_excel_copy_tag_v4에서 list에 가동률 계산한 metric(원하는 modem_list만 뽑아서 copy - add_tags_kjh.py)
		* list와 시간을 기준으로 get함
  		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
  	* rc05_excel_copy_tag_v4에서 data를 get한 후 가동률 구한 후 copy (밑은 copy된 tag lists)
  		* modem_num 	- 모뎀시리얼넘버
  		* _mds_id   	- 계량기시리얼넘버
  		* company   	- 기업유형(사업장)
  		* building  	- 건물용도
  		* load      	- 부하형태
  		* device_type	- 계측 설비형태
  		* holiday	- 주일(토,일)
  
  * 파일위치 : add_tags_kjh.1.py

building - u'공장': 'factory', u'일반건물': 'office', u'마트': 'mart', u'병원': 'hospital', u'전자대리점': 'mart', u'공동주택': 'apt', u'대형마트': 'mart', u'기타': 'etc'

company - u'대기업': 'bigcompany', u'중견': 'middlecompany', u'중소': 'smallcompany', u'비영리법인': 'etc', u'해당없음': 'etc'

device_type - u'LED': 'led', u'인버터': 'inverter', u'형광등': 'heungwanglamp', u'메탈할라이드': 'metalhalide'

load - np.NaN: 'none', u'블로워': 'blower', u'컴프래서': 'compressor', u'펌프': 'pump', u'팬': 'fan'

```
  
#### metric : rc05_operation_tag_v1 (완료)
  ```
  * 실전용 metric (완료)
  	* 시작시간 : 2017-11-07 23:18:05
  	* 소요시간 : 42분 49초
  	* copy한 data 갯수 : 553개
  	* modem_list만 copy
  	* outlier(값 100이상) 제거 및 가동률 계산(value/max_value)*100
  	* rc05_no_outlier_copy_tag_v20에서 list에 가동률 계산한 metric(원하는 modem_list만 뽑아서 copy - rm_outlier_add_tag_daily_onelist_input_v0.1.py)
  	* list와 시간을 기준으로 get함
  		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
  	* rc04_simple_data_v3의 data를 get한 후 가동률 구한 후 copy (밑은 copy된 tag lists)
  		* modem_num 	- 모뎀시리얼넘버
  		* _mds_id   	- 계량기시리얼넘버
  		* company   	- 기업유형(사업장)
  		* building  	- 건물용도
  		* load      	- 부하형태
  		* device_type	- 계측 설비형태
  		* holiday	- 주일(토,일)

  * no_outlier_adj_daily_multilist_khj_ver0.3.py
  * 파일위치 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/05/01-00:00:00&m=avg:rc05_operation_tag_v1&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

building - u'공장': 'factory', u'일반건물': 'office', u'마트': 'mart', u'공동주택': 'apt', u'대형마트': 'mart', u'기타': 'etc'

company - u'대기업': 'bigcompany', u'중견': 'middlecompany', u'중소': 'smallcompany', u'비영리법인': 'etc', u'해당없음': 'etc'

device_type - u'LED': 'led', u'인버터': 'inverter', u'형광등': 'heungwanglamp', u'메탈할라이드': 'metalhalide'

load - np.NaN: 'none', u'블로워': 'blower', u'컴프래서': 'compressor', u'펌프': 'pump', u'팬': 'fan'

```

#### metric : rc05_no_outlier_copy_tag_v20 (완료)
```
* 실전용 metric (완료)
	* 시작시간 : 2017-11-01 17:53:00
	* 값이 100 초과인것은 삭제한 metric
	* rc04_simple_data_v3을 copy한 metric(원하는 modem_list만 뽑아서 copy - add_tags_kjh.py )
	* excel와 시간을 기준으로 get함
		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
	* rc04_simple_data_v3의 data를 get한 후 outlier제외후 copy (밑은 copy된 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* company   	- 기업유형(사업장)
		* building  	- 건물용도
		* load      	- 부하형태
		* device_type	- 계측 설비형태
		* holiday	- 주일(토,일)

* rc05_no_outlier_copy_tag_v20 , 데이터가 깔끔해진것 같음
* 파일위치 : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/add_tags_kjh.py
* http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=sum:rc05_no_outlier_copy_tag_v20&o=&yrange=%5B0:%5D&wxh=805x340&style=linespoint
```



#### metric : rc05_no_outlier_led_interver_tag_v1 (완료)
```
* 실전용 metric (완료)
	* 시작시간 : 2017-11-02 16:26:00
	* 소요시간 : 32분 37초
	* copy한 data 갯수 : 494개
	* led와 inverter tag 추가
	* outlier(값 100이상) 제거 및 txt log 기록
	* log txt 경로 : /home/bornagain/kdatahub/EE-data-analysis/YKPK/KHJ/outlier_lists_171102_v1.txt
	* rc04_simple_data_v3에서 list에 포함된 data만 copy한 metric(원하는 modem_list만 뽑아서 tag 추가후 copy - no_outlier_adj_daily_multilist_khj_ver0.3.py)
	* list와 시간을 기준으로 get함
		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
	* rc04_simple_data_v3의 data를 get한 후 outlier제외후 copy 및 tag(device_type)추가(밑은 copy된 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* device_type	- 계측 설비형태
		* holiday		- 주일(토,일)

* no_outlier_adj_daily_multilist_khj_ver0.3.py
* 파일위치 : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/no_outlier_adj_daily_multilist_khj_ver0.3.py
* http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/05/01-00:00:00&m=sum:rc05_no_outlier_led_interver_tag_v1&o=&yrange=%5B0:%5D&wxh=1090x340&style=linespoint
```

#### metric : rc05_no_outlier_lte_v1 (완료)
```
* 실전용 metric (완료)
	* 시작시간 : 2017-11-02 17:51:00
	* 소요시간 : 28분
	* copy한 data 갯수 : 362개
	* valid_list만 copy
	* outlier(값 100이상) 제거 및 txt log 기록
	* log txt 경로 : /home/bornagain/kdatahub/EE-data-analysis/YKPK/KHJ/outlier_lists_171102_lte_v1.txt
	* rc04_simple_data_v3에서 list에 포함된 data만 copy한 metric(원하는 valid_list만 뽑아서 copy - no_outlier_copy_daily_onelist_khj_ver0.3.py)
	* list와 시간을 기준으로 get함
		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
	* rc04_simple_data_v3의 data를 get한 후 outlier제외후 copy 및 tag(device_type)추가(밑은 copy된 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* device_type	- 계측 설비형태
		* holiday	- 주일(토,일)

* no_outlier_adj_daily_multilist_khj_ver0.3.py
* 파일위치 : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/no_outlier_copy_daily_onelist_khj_ver0.3.py
* http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/05/01-00:00:00&m=sum:rc05_no_outlier_lte_v1&o=&yrange=%5B0:%5D&wxh=1090x340&style=linespoint
```

#### metric : rc05_no_outlier_modem_v1 (완료)
```
* 실전용 metric (완료)
	* 시작시간 : 2017-11-02 20:25:00
	* 소요시간 : 37분 24초
	* copy한 data 갯수 : 553개
	* modem_list만 copy
	* outlier(값 100이상) 제거 및 txt log 기록
	* log txt 경로 : /home/bornagain/kdatahub/EE-data-analysis/YKPK/KHJ/outlier_lists_171102_modem_v1.txt
	* rc04_simple_data_v3에서 list에 포함된 data만 copy한 metric(원하는 modem_list만 뽑아서 copy - no_outlier_copy_daily_onelist_khj_ver0.3.py)
	* list와 시간을 기준으로 get함
		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
	* rc04_simple_data_v3의 data를 get한 후 outlier제외후 copy 및 tag(device_type)추가(밑은 copy된 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* device_type	- 계측 설비형태
		* holiday	- 주일(토,일)

* no_outlier_adj_daily_multilist_khj_ver0.3.py
* 파일위치 : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/no_outlier_copy_daily_onelist_khj_ver0.3.py
* http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/05/01-00:00:00&m=sum:rc05_no_outlier_modem_v1&o=&yrange=%5B0:%5D&wxh=1090x340&style=linespoint
```


#### metric : rc04_add_tag_v4
	* rc04_simple_data_v3의 data를 get하여 excel의 data를 참고하여 device_type을 구분하여 tag를 추가한 metric
	* tag의 info는 excel을 참조함
		* https://github.com/imbornagainer/MyProject/blob/master/kdata_hub/KHJ/ref_list_kjh.xlsx
	* rc04_simple_data_v3에 tag를 추가함 (밑은 추가한 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* company   	- 기업유형(사업장)
		* building  	- 건물용도
		* load      	- 부하형태
		* device_type	- 계측 설비형태
		* holiday	- 주일(토,일)
	* 실행 소스코드 ?

#### metric : rc03_add_led_tag_v9
	* rc04_simple_data_v3의 data를 get하여 _input_list_17_0906.py의 Modem_list의 값만 뽑아서 device_type로 구분하여 tag를 추가한 metric
	* tag의 info는 py을 참조함
		* https://github.com/imbornagainer/MyProject/blob/master/kdata_hub/lib/_input_list_17_0906.py
	* rc04_simple_data_v3에 tag를 추가함 (밑은 추가한 tag lists)
		* modem_num 			- 모뎀시리얼넘버
		* _mds_id   			- 계량기시리얼넘버
		* modem_led_inverter 		- 계측 설비형태
		* holiday			- 주일(토,일)

#### metric : rc04_khj_copy_v5
	* rc04_add_tag_v4의 metric을 copy한 metric
	* tag가 아닌 시간을 기준으로 get함
		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
	* rc04_add_tag_v4의 data를 get한 후 copy (밑은 copy된 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* company   	- 기업유형(사업장)
		* building  	- 건물용도
		* load      	- 부하형태
		* device_type	- 계측 설비형태
		* holiday	- 주일(토,일)

#### metric : rc05_adj_copy_test_tag_v4
    * test용 metric - 테스트 완료
	* rc04_simple_data_v3의 metric을 copy한 metric(원하는 modem_list만 뽑아서 copy - adj_copy_all_khj.py )
	* 정상 copy, adj 정상확인
	* tag와 시간을 기준으로 get함
		* ex) From 2016/07/01-00:00:00 ~ To 2017/08/01-00:00:00
	* rc04_simple_data_v3의 data를 get한 후 copy (밑은 copy된 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* led_inverter  - 계측 설비형태
		* holiday	- 주일(토,일)

#### metric : rc05_adj_copy_test_tag_v7
    * test용 metric - 테스트 완료
	* rc04_simple_data_v3을 copy한 metric(원하는 modem_list만 뽑아서 copy - adj_copy_daily_khj.py )
	* 정상 copy, adj 정상확인
	* tag와 시간을 기준으로 get함
		* ex) From 2016/07/01-00:00:00 ~ To 2017/07/31-00:00:00
	* rc04_simple_data_v3의 data를 get한 후 copy (밑은 copy된 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* led_inverter  - 계측 설비형태
		* holiday	- 주일(토,일)

#### metric : rc05_adj_copy_tag_v6 (중단)
```
* 미래비엠의 값을 삭제한 실전용 metric (stop copy)
* 17/10/27-11:20:21 copy 시작 ~ 17/17/27-14:13 copy  (outlier 제거하는 source 구축으로 인해)
* rc04_simple_data_v3을 copy한 metric(원하는 modem_list만 뽑아서 copy - adj_copy_daily_khj.py )
* 정상 copy, adj 정상확인
* tag와 시간을 기준으로 get함
	* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
* rc04_simple_data_v3의 data를 get한 후 copy (밑은 copy된 tag lists)
	* modem_num 	- 모뎀시리얼넘버
	* _mds_id   	- 계량기시리얼넘버
	* led_inverter  - 계측 설비형태
	* holiday	- 주일(토,일)
```

#### metric : rc05_adj_copy_test_tag_v10
```
* test용 metric - 테스트 완료
	* rc04_simple_data_v3을 copy한 metric(원하는 modem_list만 뽑아서 copy - no_outlier_copy_daily_khj.py )
	* 정상 copy, adj 정상확인
	* tag와 시간을 기준으로 get함
		* ex) From 2016/07/27-00:00:00 ~ To 2017/07/28-00:00:00
	* rc04_simple_data_v3의 data를 get한 후 outlier제외후 copy (밑은 copy된 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* led_inverter  - 계측 설비형태
		* holiday	- 주일(토,일)
```

#### metric : rc05_no_outlier_copy_tag_v1 (중지) - 노트북으로 실행할때 너무느림
```
* 실전용 metric (중지)
	* 시작시간 : 2017-10-27 16:13:14
	* rc04_simple_data_v3을 copy한 metric(원하는 modem_list만 뽑아서 copy - no_outlier_copy_daily_khj.py )
	* tag와 시간을 기준으로 get함
		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
	* rc04_simple_data_v3의 data를 get한 후 outlier제외후 copy (밑은 copy된 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* led_inverter  - 계측 설비형태
		* holiday	- 주일(토,일)
```

#### metric : rc05_no_outlier_copy_tag_v19 (중지) - 진행중 request time out...
```
* 실전용 metric (중지)
	* 시작시간 : 2017-11-01 16:14:00
	* 값이 100 초과인것은 삭제한 metric
	* rc04_simple_data_v3을 copy한 metric(원하는 modem_list만 뽑아서 copy - no_outlier_copy_daily_khj.py )
	* tag와 시간을 기준으로 get함
		* ex) From 2016/07/01-00:00:00 ~ To 2017/05/01-00:00:00
	* rc04_simple_data_v3의 data를 get한 후 outlier제외후 copy (밑은 copy된 tag lists)
		* modem_num 	- 모뎀시리얼넘버
		* _mds_id   	- 계량기시리얼넘버
		* led_inverter  - 계측 설비형태
		* holiday	- 주일(토,일)
```
