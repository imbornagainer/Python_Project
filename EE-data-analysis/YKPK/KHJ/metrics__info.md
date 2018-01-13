OpenTSDB Metric에 대한 info

##### OpenTSDB URL : http://125.140.110.217:4242


| 순서   | 메트릭 이름                                   | 확인사항                                   | 작업일자  |
| ---- | ---------------------------------------- | -------------------------------------- | ----- |
| 1    | rc04_simple_data_v3                      | LTE modem_num 만 들어 있음                  |       |
| 2    | rc05_excel_copy_tag_v8                   | 태그추가, outlier 제거                       |  01.10     |
| 3    | rc06_operation_rate_v3 -> v5                  | 가동 바이너리 표시, 업종 기타 추가함  (진행중)         | 12.10 |
| 4    | rc04_totoal_cnt__002   -> 003                 | (변화하는) 총 갯수, 미전송 갯수 제거           | 12.12 |
|      |                                          | none dps 를 먼저 구해야함 (시간많이걸림)       | 12.11 |
|      |                                          | rc05_none_dp_v5 (12.11)                | 12.11 |
| 4-1  | rc06_op_rate_v3                            |     | 1.8 |
|      |                                          |                                        |       |
| 5    | rc05_op_rate_v12(opreation 개선)           | operation rate / total 갯수 계산 tot_gasun |       |
| 6    | ___d_tag_test_load_rate_5 , 진행중, screen 이름 calc                | holiday tag = 1 없음, 모두 0               |  12.13      |
| 7    | rc06_ld_rate_v3  |                                        |   1.8    |
| 8    | oprate___test___001(가동율 1일평균)          |                                        |       |
| 9    | ___ldrate___test___001___(사용율 1일평균)      |                                        |       |
| 10   | 동절기, 하절기 적용                              |                                        |       |

#### rc06_operation_rate_v5(진행중)
- metric in - rc05_excel_copy_tag_v8
- 가동수
- 소스위치 : EE-data-analysis\YKPK\KHJ\Main_Program\MetricCopy_etc\MetricCopy_outlier_deleting\Main\1. Binary_process\BBR_rc01.py
- 링크 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=zimsum:rc06_operation_rate_v5&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc05_excel_copy_tag_v8(완료)
- metric in - rc04_simple_data_v3
- outlier, tag 추가 (원본 데이터에서)
- 소스위치 : EE-data-analysis\YKPK\KHJ\Main_Program\MetricCopy_etc\MetricCopy_outlier_deleting\Main\1. Binary_process\BBR_rc01.py
- 링크 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=zimsum:rc05_excel_copy_tag_v8&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc06_BRR_cool_tag_v2
- metric in - ___d_test_cool_tag_v3
- 소스위치 : EE-data-analysis\YKPK\KHJ\Main_Program\MetricCopy_etc\MetricCopy_outlier_deleting\Main\1. Binary_process\BBR_rc01.py
- 링크 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=zimsum:rc06_BRR_cool_tag_v2&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### ___ldrate___test___001___
- metric in - rc06_ld_rate_v3
- 소스위치 : EE-data-analysis\unit_test\1day_opr.py
- 링크 : http://tinyos.asuscomm.com:44242/#start=2016/06/01-00:00:00&end=2016/06/02-00:00:00&m=avg:___ldrate___test___001___&o=&yrange=%5B0:%5D&wxh=938x757&style=linespoint

#### ___oprate___test___001___
- metric in - rc06_op_rate_v3
- 소스위치 : EE-data-analysis\unit_test\1day_opr.py
- 링크 : http://tinyos.asuscomm.com:44242/#start=2016/06/01-00:00:00&end=2016/06/02-00:00:00&m=avg:___oprate___test___001___&o=&yrange=%5B0:%5D&wxh=938x757&style=linespoint

#### rc06_op_rate_daily_v5
- metric in - rc06_op_rate_v3
- 소스위치 : EE-data-analysis\unit_test\1day_opr.py
- 링크 : http://125.140.110.217:4242/#start=2016/06/01-00:00:00&end=2016/06/02-00:00:00&m=avg:rc06_op_rate_daily_v6%7Bdevice_type=inverter%7D&o=&yrange=%5B0:%5D&wxh=1006x570&style=linespoint

#### rc05_none_dp_v7
- ___d_test_cool_tag_v3와 rc04_simple_cool_v1 사용한 none dps
- 소스위치 : EE-data-analysis\report\none_dps.py
- 링크 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=count:rc05_none_dp_v7&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc06_op_rate_v3
- rc06_operation_rate_v3와 rc04_totoal_cnt__002 사용한 가동율(op rate)
- 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_operationRate.py
- 링크 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=zimsum:rc06_operation_rate_v3%7Bdevice_type=inverter%7D&o=&m=avg:rc06_op_rate_v2&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc06_op_rate_v2
- rc06_operation_rate_v3와 rc04_totoal_cnt__002 사용한 가동율(op rate)
- 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_operationRate.py
- 링크 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=zimsum:rc06_operation_rate_v3%7Bdevice_type=inverter%7D&o=&m=sum:rc06_op_rate_v2&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc06_ld_rate_v3
- rc06_op_rate_ 가동율 하절기, 동절기
- 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Loadfactor.py
- 링크 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=avg:rc06_op_rate_season_v2%7Bseason=winter%7D&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc06_op_rate_season_v2
- rc06_op_rate_ 가동율 하절기, 동절기
- 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Loadfactor.py
- 링크 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=avg:rc06_op_rate_season_v2%7Bseason=winter%7D&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc06_ld_rate_daily_v1
- rc06_ld_rate_v2 사용율의 일일평균
- 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Operation.py
- 링크 : http://125.140.110.217:4242/#start=2016/06/01-00:00:00&end=2016/06/02-00:00:00&m=avg:rc06_ld_rate_daily_v1%7Bdetail=medical%7D&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc06_op_rate_daily_v3
- rc06_op_rate_ 가동율의 일일평균
- 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Operation.py
- 링크 : http://125.140.110.217:4242/#start=2016/06/01-00:00:00&end=2016/06/02-00:00:00&m=avg:rc06_op_rate_daily_v3&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc06_ld_rate_v2
- 사용율의 동절기/하절기/주중/주말(op rate)
- 태그중 season이 summer / winter
- holiday - 0,1
- 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Loadfactor.py
- 링크 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=avg:rc06_ld_rate_v2&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc06_op_rate_season_v1
- rc06_op_rate_ 가동율의 동절기/하절기(op rate)
- 태그중 season이 summer / winter 로 구분됨.
- 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Operation.py
- 링크 : http://125.140.110.217:4242/#start=2016/06/01-00:00:00&end=2017/07/01-00:00:00&m=avg:rc06_op_rate_season_v1&o=&yrange=%5B0:%5D&key=out%20bottom%20center&wxh=1008x500&style=points

#### rc06_op_rate_daily_v2
- rc06_op_rate_의 일별 가동율(op rate)
- 16/06/01 ~ 16/06/02
- 태그중 season이 summer / winter 로 구분됨.
- 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Operation.py
- 링크 : http://125.140.110.217:4242/#start=2016/06/01-00:00:00&end=2017/07/01-00:00:00&m=avg:rc06_op_rate_season_v1&o=&yrange=%5B0:%5D&key=out%20bottom%20center&wxh=1008x500&style=points

#### rc06_op_rate_
- rc06_operation_rate_v3와 rc04_totoal_cnt__002 사용한 가동율(op rate)
- 태그중 totcount 가 total / each 로 구분됨.
- 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_operationRate.py
- 링크 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=avg:rc06_op_rate_%7Bdetail=carpart%7D&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc04_totoal_cnt__002

- 가동율(op rate) 구할때 분모로 사용되는 수
- 태그중 totcount 가 total / each 로 구분됨. 
  - Led 총 갯수를 질의할땐, total
  - 나머지경우 led / detail:carpart 호출할때는 totocount 아무런 데이터 넣지 않아도 됨
- total count 완료 _20171212_
- 다음 JSON을 보면, 엑셀에 적힌 최대 숫자가 있음. EE-data-analysis/lib/tools/count_list.json
  - 이 최대숫자에서 전송이 안된 (none dps) 포인트를 빼어준 데이터임
- 링크 : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=none:rc04_totoal_cnt__002%7Bdetail=carpart,device_type=led%7D&o=&yrange=%5B0:%5D&key=out%20bottom%20center&wxh=1008x500&style=points

#### rc06_operation_rate_v3

 - 기타 업종 추가함 _20171210_
 - 소스위치 : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/report/cp_metric_with_change_tag.py
 - opentsdb : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=zimsum:rc06_operation_rate_v3&o=&yrange=%5B0:%5D&wxh=1006x570&style=linespoint  
 - 소요시간 30분  
 - rc05_operation_rate_v6 에 detail 세부업종 추가

#### rc06_op_rate_v1

  - 아직 불완전함 (12.10)
  - 가동율 rc06_operation_rate_v1로 구한 것
  ```
  u'자동차부품': 'carpart', u'기계설비': 'machineEquipment', u'반도체': 'semiconductor', 
  u'전자전기': 'electronicShock', u'의료': 'medical'
  ```
  - 소요시간 :
  - 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_operationRate.py
  - opentsdb : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2016/08/01-00:00:00&m=avg:rc06_op_rate_v1&o=&yrange=%5B0:%5D&key=out%20bottom%20center&wxh=1006x970&style=points

#### rc06_operation_rate_v1 , v2
  - 불완전함 (12.10)
  - 가동수(operation_rate_v6) tag 새로 input
  - 뭔가 문제가 있음 입력되는 데이터포인트수가   
      ```
        u'자동차부품': 'carpart', u'기계설비': 'machineEquipment', u'반도체': 'semiconductor', 
        u'전자전기': 'electronicShock', u'의료': 'medical'
      ```
  ```
  - 소요시간 : 20분
  - 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Adjust.py
  - opentsdb : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=avg:rc06_operation_rate_v1&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc05_op_rate_season_v2
  - 가동율 v12으로 하절기, 동절기 다시 구함
  - 저장 시작.
  - 종료시간
  - 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Operation.py
  - opentsdb : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/03/01-00:00:00&m=avg:rc05_op_rate_season_v2%7Bdevice_type=led,season=winter%7D&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc05_op_rate_v12
  - 가동율
  - 저장 시작.
  - 종료시간
  - 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_operationRate.py
  - opentsdb : http://125.140.110.217:4242/#start=2016/09/18-16:07:00&end=2016/09/18-22:29:56&m=count:rc05_op_rate_v12&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc05_op_rate_season_daily_v1
  - rc05_op_rate_season_v1 일일평균
  - 가동율
  - 저장 시작.
  - 종료시간
  - 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_daily_Operation.py
  - opentsdb : http://125.140.110.217:4242/#start=2016/06/01-00:00:00&end=2016/06/03-00:00:00&m=avg:rc05_op_rate_season_daily_v1%7Bseason=winter%7D&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc05_ld_rate_season_daily_v1
  - rc05_ld_rate_season_v1 일일평균
  - 사용율
  - 저장 시작.
  - 종료시간
  - 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_daily_Operation.py
  - opentsdb : http://125.140.110.217:4242/#start=2016/06/01-00:00:00&end=2016/06/03-00:00:00&m=avg:rc05_ld_rate_season_daily_v1%7Bseason=winter%7D&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc05_op_rate_season_v1
  - rc05_op_rate_v11 metric에서 계절태그 추가
  - 저장 시작.
  - 종료시간
  - 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Operation.py
  - opentsdb : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/03/01-00:00:00&m=avg:rc05_ld_rate_season_v1%7Bseason=summer%7D&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc05_ld_rate_season_v1
  - rc05_ld_rate_v4 metric에서 계절태그 추가
  - 저장 시작.
  - 종료시간
  - 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Loadfactor.py
  - opentsdb : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/03/01-00:00:00&m=avg:rc05_ld_rate_season_v1%7Bseason=summer%7D&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

#### rc05_ld_rate_v4
  - 부하율, 사용률, 각 LTE 모뎀의 MAX 값 기준
  - holiday 및 다른 문제점 개선한 메트릭
  - 저장 시작.
  - 종료시간
  - 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Loadfactor.py
  - http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/03/01-00:00:00&m=avg:rc05_ld_rate_v4%7Bdevice_type=led%7D&o=&m=zimsum:rc05_none_dp_v4&o=&yrange=%5B0:%5D&wxh=993x532&style=linespoint

#### rc05_op_rate_v11
  - 가동율 그래프(%로 구현)
  - holiday 추가
  - 기간 16.07.01 ~ 17.07.01
  - 소스위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_operationRate.py
  - http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/03/01-00:00:00&m=avg:rc05_op_rate_v11%7Bdevice_type=led%7D&o=&yrange=%5B0:%5D&wxh=993x532&style=linespoint

#### rc05_tot_daily_opr_test_v2
* 일별 하루 가동율
  - 기간 16.06.01 ~ 16.06.02

#### rc05_tot_daily_lr_test_v2
* 일별 하루 사용율
  - 기간 16.06.01 ~ 16.06.02

#### rc05_load_rate_v2

* 부하율, 사용률, 각 LTE 모뎀의 MAX 값 기준
* holiday 문제점 개선한 메트릭
* 저장 시작.
* 종료시간

#### metric : rc05_daily_opr_weekend_v2

가동율 주말(일별) 누적 그래프
  - 기간 16.07.01 ~ 17.07.01

tag정보
  - kdatahub\EE-data-analysis\lib\tools\count_list.json
  - totcount : total(LED), each(inverter)
  - holiday : 1

소요시간 20분 내외

소스위치
- kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_daily_Operate.py

#### metric : rc05_daily_opr_weekdays_v2

가동율 주중(일별) 누적 그래프
  - 기간 16.07.01 ~ 17.07.01

tag정보
  - kdatahub\EE-data-analysis\lib\tools\count_list.json
  - totcount : total(LED), each(inverter)
  - holiday : 0

소요시간 20분 내외

소스위치
- kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_daily_Operate.py

#### metric : rc05_daily_opr_v1

가동율 1년 일별 누적 그래프
  - 기간 16.07.01 ~ 17.07.01

tag정보
  - kdatahub\EE-data-analysis\lib\tools\count_list.json
  - totcount : total(LED), each(inverter)

소요시간 20분 내외

소스위치
- kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_daily_Operate.py

#### metric : rc05_op_rate_v10

가동율 그래프(%로 구현)
  - 기간 16.07.01 ~ 17.07.01

tag정보
  - kdatahub\EE-data-analysis\lib\tools\count_list.json
  - totcount : total(LED), each(inverter)

소요시간 20분 내외

소스위치
- kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_operationRate.py

#### metric : ___d_test_cool_tag_v3

EHP 냉난방기 입력, 태그추가 device_type

소요시간 20분 내외

.../lib/add_tag.py

#### metric : rc04_cool_tag_v2

EHP 냉난방기 입력, load 추가

소요시간 20분 내외

.../lib/add_tag.py

#### metric : rc04_totoal_cnt__001

.../lib/tools/count_tsdb.py (python3 으로 실행)

가동율을 구하기 위한 분모 (none DP 만큼 빼어준 숫자)

30분내외

totcount 태그를 추가함

totcount : total => 전체 갯수, each => 그외

전체 갯수를 구할때, totcount 태그를 정해주지 않으면, 2가 곱해진, 2배 큰 숫자가 구해짐

led, buidling, office 이런식으로 사용하면 됨 ==> 해당 태그의 LTE 모뎀 갯수



#### metric : rc05_excel_copy_tag_v7 (완료)

* 엑셀의 outlier를 반영하기 위해서(엑셀을 기준으로)
* get : rc04_simple_data_v3 -> tag, outlier 처리
  ```
  #### tag정보
  u'공장': 'factory', u'일반건물': 'office', u'마트': 'mart', u'공동주택': 'apt', u'대형마트': 'bigmart', u'기타': 'etc',      
  # building
  u'대기업': 'bigcompany', u'중견': 'middlecompany', u'중소': 'smallcompany', u'비영리법인': 'biyoung', u'해당없음': 'nono', 
  # company
  u'병원': 'hospital', u'전자대리점': 'electricmart', # business
  u'금속': 'metal', u'산업기타': 'industryEtc', u'건물기타': 'building_etc', u'제지목재': 'wood', u'요업': 'ceramic',		 
  # business
  u'백화점': 'departmentStore', u'섬유': 'fiber', u'학교': 'school', u'식품': 'food', u'화공': 'fceramic',	
  # business 
  u'상용': 'sangyong',  
  # business
  u'LED': 'led', u'인버터': 'inverter', u'형광등': 'heungwanglamp', u'메탈할라이드': 'metalhalide',  			
  # device_type
   np.NaN: 'none', u'블로워': 'blower', u'컴프래서': 'compressor', u'펌프': 'pump', u'팬': 'fan',	 					   # load 
  ```
* outlier처리 0,None은 제외, 0.001이상, 200이하는 허용)
* (EE)list_002.xlsx의 Data를 가져옴
* 저장 시작. 11/21, PM 1:34
* 종료시간

#### metric : rc05_none_rate_v3
* value가 none인 data를 1처리
* valid list에만 처리 - in_list.py의 total_vlist
* 저장 시작. 11/21, AM 10:05
* 종료시간### OpenTSDB Metric에 대한 info
##### OpenTSDB URL : http://125.140.110.217:4242

#### metric : rc05_none_rate_v3
* value가 none인 data를 1처리
* valid list에만 처리 - in_list.py의 total_vlist
* 저장 시작. 11/21, AM 10:05
* 종료시간

#### metric : ___d_tag_test_load_rate_4
* 부하율, 사용률, 각 LTE 모뎀의 MAX 값 기준
* run_loadrate.sh loadrate
* 저장 시작 완료. 11/20, PM 10:36
* 종료시간

#### metric : rc04_simple_cool_v1
* 추가해야하는 냉난방기 리스트 입력중, 11/19
* 오라클원본, 데이터, in_list.coolbiol_list : 94
* 저장 완료. 11/20, PM 10:00

#### metric : rc04_simple_data_v3
* 오라클DB 데이터를 그대로 복사하여 옮김
* LTE 모뎀번호만 Tag로 저장함 
* 다음 메트릭 만들때 해야할일
  * 측정 이상한 데이터 삭제

#### metric : rc05_operation_rate_v6 (완료)
* 2017 / 11/ 15 / 밤
* 0 & none값 제거 및 binary 처리
* list와 시간을 기준으로 get함
  * ex) From 2016/07/01-00:00:00 ~ To 2017/07/01-00:00:00
* 코드 : \kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\MetricCopy_etc\MetricCopy_outlier_deleting\Main\1. Binary_process\no_zero_value_copy_daily_onelist_binary_khj_ver0.1.py

#### metric : rc05_excel_copy_tag_v5 (완료)
* 2017 / 11/ 15 / 늦은 저녁
* outlier 제거 및 tag추가
* list와 시간을 기준으로 get함
  * ex) From 2016/07/01-00:00:00 ~ To 2017/07/01-00:00:00
* 코드 : \kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\MetricCopy_etc\MetricCopy_Tag_adding\add_tags_kjh.py

#### metric : __kjh_whole_brc01_
* 2017 / 11/ 14 / 아침
* 전체 LTE미터를 합산하여 BRR 계산
* http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2016/07/03-08:57:51&m=avg:__kjh_whole_brc01_&o=&yrange=%5B0:%5D&wxh=1177x1140&style=linespoint
* 코드 : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/Main_Program/MetricCopy_outlier_deleting/Main/1.%20Binary_process/BBR_rc01.py

#### metric : rc05_operation_rate_v3 (완료)
  ```
* 실전용 metric (완료)
  * binary 처리한 것(가동됬냐 안됬냐 처리)
  * 2017 / 11/ 13 / 아침
  * 데이터가 있는 것은 1, none이거나 0이면 값 없음(제외)
  * list와 시간을 기준으로 get함
    * ex) From 2016/07/01-00:00:00 ~ To 2016/08/01-00:00:00
  * rc05_excel_copy_tag_v4에서 data를 get한 후 binary 처리후 copy (밑은 copy된 tag lists)
    * modem_num 	- 모뎀시리얼넘버
      * _mds_id   - 계량기시리얼넘버
      * company   - 기업유형(사업장)
      * building  - 건물용도
      * load      - 부하형태
      * device_type- 계측 설비형태
      * holiday- 주일(토,일)
      * detail- 세부사항

  * 파일위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\MetricCopy_outlier_deleting\Main\1. Binary_process\no_zero_value_copy_daily_onelist_binary_khj_ver0.1.py
  * opentsdb_URL : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2016/08/01-00:00:00&m=avg:rc05_operation_rate_v3&o=&yrange=%5B0:%5D&wxh=1177x1140&style=linespoint

building - u'공장': 'factory', u'일반건물': 'office', u'마트': 'mart', u'병원': 'hospital', u'전자대리점': 'mart', u'공동주택': 'apt', u'대형마트': 'mart', u'기타': 'etc'

company - u'대기업': 'bigcompany', u'중견': 'middlecompany', u'중소': 'smallcompany', u'비영리법인': 'etc', u'해당없음': 'etc'

device_type - u'LED': 'led', u'인버터': 'inverter', u'형광등': 'heungwanglamp', u'메탈할라이드': 'metalhalide'

load - np.NaN: 'none', u'블로워': 'blower', u'컴프래서': 'compressor', u'펌프': 'pump', u'팬': 'fan'

  ```

#### metric : rc05_BRR_15min_v2 (완료)
  ```
* 실전용 metric (완료)
   * 시작시간 : 2017-11-13 17:36:05
     * 소요시간 : 07분 10초
     * copy한 data 갯수 : 431개
       * 1값이 있는 것만 copy BRR	
     * 가동률 계산(count_modem / total_modem)*100 - (갯수 / 전체갯수) * 100
     * rc05_excel_copy_tag_v4에서 list에 가동률 계산한 metric(원하는 modem_list만 뽑아서 copy - no_zero_value_copy_daily_onelist_binary_khj_ver0.1.py)
     * list와 시간을 기준으로 get함
       * ex) From 2016/07/01-00:00:00 ~ To 2016/08/01-00:00:00
     * rc05_excel_copy_tag_v4에서 data를 get한 후 가동률 구한 후 copy (밑은 copy된 tag lists)
       * modem_num 	- 모뎀시리얼넘버
         * _mds_id   - 계량기시리얼넘버
         * company   - 기업유형(사업장)
         * building  - 건물용도
         * load      - 부하형태
         * device_type- 계측 설비형태
           * holiday- 주일(토,일)
         * detail- 세부사항

  * 파일위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\MetricCopy_outlier_deleting\Main\no_zero_value_copy_daily_onelist_binary_khj_ver0.1.py
  * opentsdb_URL : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2016/08/01-00:00:00&m=avg:rc05_BRR_15min_v2&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

building - u'공장': 'factory', u'일반건물': 'office', u'마트': 'mart', u'병원': 'hospital', u'전자대리점': 'mart', u'공동주택': 'apt', u'대형마트': 'mart', u'기타': 'etc'

company - u'대기업': 'bigcompany', u'중견': 'middlecompany', u'중소': 'smallcompany', u'비영리법인': 'etc', u'해당없음': 'etc'

device_type - u'LED': 'led', u'인버터': 'inverter', u'형광등': 'heungwanglamp', u'메탈할라이드': 'metalhalide'

load - np.NaN: 'none', u'블로워': 'blower', u'컴프래서': 'compressor', u'펌프': 'pump', u'팬': 'fan'

  ```

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
         * _mds_id   - 계량기시리얼넘버
         * company   - 기업유형(사업장)
         * building  - 건물용도
         * load      - 부하형태
         * device_type- 계측 설비형태
           * holiday- 주일(토,일)
         * detail- 세부사항

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
         * _mds_id   - 계량기시리얼넘버
         * company   - 기업유형(사업장)
         * building  - 건물용도
         * load      - 부하형태
         * device_type- 계측 설비형태
         * holiday- 주일(토,일)

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
         * _mds_id   - 계량기시리얼넘버
         * company   - 기업유형(사업장)
         * building  - 건물용도
         * load      - 부하형태
         * device_type- 계측 설비형태
         * holiday- 주일(토,일)

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
           * _mds_id   - 계량기시리얼넘버
           * company   - 기업유형(사업장)
           * building  - 건물용도
           * load      - 부하형태
           * device_type- 계측 설비형태
           * holiday- 주일(토,일)

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
      * _mds_id   - 계량기시리얼넘버
      * company   - 기업유형(사업장)
      * building  - 건물용도
      * load      - 부하형태
      * device_type- 계측 설비형태
      * holiday- 주일(토,일)

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
      * _mds_id   - 계량기시리얼넘버
      * device_type- 계측 설비형태
        * holiday- 주일(토,일)

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
      * _mds_id   - 계량기시리얼넘버
      * device_type- 계측 설비형태
      * holiday- 주일(토,일)

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
      * _mds_id   - 계량기시리얼넘버
      * device_type- 계측 설비형태
      * holiday- 주일(토,일)

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
    * _mds_id   - 계량기시리얼넘버
  * led_inverter  - 계측 설비형태
    * holiday- 주일(토,일)
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
      * _mds_id   - 계량기시리얼넘버
    * led_inverter  - 계측 설비형태
      * holiday- 주일(토,일)
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
      * _mds_id   - 계량기시리얼넘버
    * led_inverter  - 계측 설비형태
      * holiday- 주일(토,일)
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
      * _mds_id   - 계량기시리얼넘버
    * led_inverter  - 계측 설비형태
      * holiday- 주일(토,일)
```


#### metric : ___d_tag_test_load_rate_4
* 부하율, 사용률, 각 LTE 모뎀의 MAX 값 기준
* run_loadrate.sh loadrate
* 저장 시작 완료. 11/20, PM 10:36
* 종료시간

#### metric : rc04_simple_cool_v1
* 추가해야하는 냉난방기 리스트 입력중, 11/19
* 오라클원본, 데이터, in_list.coolbiol_list : 94
* 저장 완료. 11/20, PM 10:00

#### metric : rc04_simple_data_v3
* 오라클DB 데이터를 그대로 복사하여 옮김
* LTE 모뎀번호만 Tag로 저장함 
* 다음 메트릭 만들때 해야할일
  * 측정 이상한 데이터 삭제

#### metric : rc05_operation_rate_v6 (완료)
* 2017 / 11/ 15 / 밤
* 0 & none값 제거 및 binary 처리
* list와 시간을 기준으로 get함
  * ex) From 2016/07/01-00:00:00 ~ To 2017/07/01-00:00:00
* 코드 : \kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\MetricCopy_etc\MetricCopy_outlier_deleting\Main\1. Binary_process\no_zero_value_copy_daily_onelist_binary_khj_ver0.1.py

#### metric : rc05_excel_copy_tag_v5 (완료)
* 2017 / 11/ 15 / 늦은 저녁
* outlier 제거 및 tag추가
* list와 시간을 기준으로 get함
  * ex) From 2016/07/01-00:00:00 ~ To 2017/07/01-00:00:00
* 코드 : \kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\MetricCopy_etc\MetricCopy_Tag_adding\add_tags_kjh.py

#### metric : __kjh_whole_brc01_
* 2017 / 11/ 14 / 아침
* 전체 LTE미터를 합산하여 BRR 계산
* http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2016/07/03-08:57:51&m=avg:__kjh_whole_brc01_&o=&yrange=%5B0:%5D&wxh=1177x1140&style=linespoint
* 코드 : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/Main_Program/MetricCopy_outlier_deleting/Main/1.%20Binary_process/BBR_rc01.py

#### metric : rc05_operation_rate_v3 (완료)
```
* 실전용 metric (완료)
  * binary 처리한 것(가동됬냐 안됬냐 처리)
  * 2017 / 11/ 13 / 아침
  * 데이터가 있는 것은 1, none이거나 0이면 값 없음(제외)
  * list와 시간을 기준으로 get함
    * ex) From 2016/07/01-00:00:00 ~ To 2016/08/01-00:00:00
  * rc05_excel_copy_tag_v4에서 data를 get한 후 binary 처리후 copy (밑은 copy된 tag lists)
    * modem_num 	- 모뎀시리얼넘버
      * _mds_id   - 계량기시리얼넘버
      * company   - 기업유형(사업장)
      * building  - 건물용도
      * load      - 부하형태
      * device_type- 계측 설비형태
      * holiday- 주일(토,일)
      * detail- 세부사항

  * 파일위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\MetricCopy_outlier_deleting\Main\1. Binary_process\no_zero_value_copy_daily_onelist_binary_khj_ver0.1.py
  * opentsdb_URL : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2016/08/01-00:00:00&m=avg:rc05_operation_rate_v3&o=&yrange=%5B0:%5D&wxh=1177x1140&style=linespoint

building - u'공장': 'factory', u'일반건물': 'office', u'마트': 'mart', u'병원': 'hospital', u'전자대리점': 'mart', u'공동주택': 'apt', u'대형마트': 'mart', u'기타': 'etc'

company - u'대기업': 'bigcompany', u'중견': 'middlecompany', u'중소': 'smallcompany', u'비영리법인': 'etc', u'해당없음': 'etc'

device_type - u'LED': 'led', u'인버터': 'inverter', u'형광등': 'heungwanglamp', u'메탈할라이드': 'metalhalide'

load - np.NaN: 'none', u'블로워': 'blower', u'컴프래서': 'compressor', u'펌프': 'pump', u'팬': 'fan'

  ```

#### metric : rc05_BRR_15min_v2 (완료)
  ```
* 실전용 metric (완료)
   * 시작시간 : 2017-11-13 17:36:05
     * 소요시간 : 07분 10초
     * copy한 data 갯수 : 431개
       * 1값이 있는 것만 copy BRR	
     * 가동률 계산(count_modem / total_modem)*100 - (갯수 / 전체갯수) * 100
     * rc05_excel_copy_tag_v4에서 list에 가동률 계산한 metric(원하는 modem_list만 뽑아서 copy - no_zero_value_copy_daily_onelist_binary_khj_ver0.1.py)
     * list와 시간을 기준으로 get함
       * ex) From 2016/07/01-00:00:00 ~ To 2016/08/01-00:00:00
     * rc05_excel_copy_tag_v4에서 data를 get한 후 가동률 구한 후 copy (밑은 copy된 tag lists)
       * modem_num 	- 모뎀시리얼넘버
         * _mds_id   - 계량기시리얼넘버
         * company   - 기업유형(사업장)
         * building  - 건물용도
         * load      - 부하형태
         * device_type- 계측 설비형태
           * holiday- 주일(토,일)
         * detail- 세부사항

  * 파일위치 : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\MetricCopy_outlier_deleting\Main\no_zero_value_copy_daily_onelist_binary_khj_ver0.1.py
  * opentsdb_URL : http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2016/08/01-00:00:00&m=avg:rc05_BRR_15min_v2&o=&yrange=%5B0:%5D&wxh=1006x970&style=linespoint

building - u'공장': 'factory', u'일반건물': 'office', u'마트': 'mart', u'병원': 'hospital', u'전자대리점': 'mart', u'공동주택': 'apt', u'대형마트': 'mart', u'기타': 'etc'

company - u'대기업': 'bigcompany', u'중견': 'middlecompany', u'중소': 'smallcompany', u'비영리법인': 'etc', u'해당없음': 'etc'

device_type - u'LED': 'led', u'인버터': 'inverter', u'형광등': 'heungwanglamp', u'메탈할라이드': 'metalhalide'

load - np.NaN: 'none', u'블로워': 'blower', u'컴프래서': 'compressor', u'펌프': 'pump', u'팬': 'fan'

  ```

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
         * _mds_id   - 계량기시리얼넘버
         * company   - 기업유형(사업장)
         * building  - 건물용도
         * load      - 부하형태
         * device_type- 계측 설비형태
           * holiday- 주일(토,일)
         * detail- 세부사항

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
         * _mds_id   - 계량기시리얼넘버
         * company   - 기업유형(사업장)
         * building  - 건물용도
         * load      - 부하형태
         * device_type- 계측 설비형태
         * holiday- 주일(토,일)

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
         * _mds_id   - 계량기시리얼넘버
         * company   - 기업유형(사업장)
         * building  - 건물용도
         * load      - 부하형태
         * device_type- 계측 설비형태
         * holiday- 주일(토,일)

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
           * _mds_id   - 계량기시리얼넘버
           * company   - 기업유형(사업장)
           * building  - 건물용도
           * load      - 부하형태
           * device_type- 계측 설비형태
           * holiday- 주일(토,일)

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
      * _mds_id   - 계량기시리얼넘버
      * company   - 기업유형(사업장)
      * building  - 건물용도
      * load      - 부하형태
      * device_type- 계측 설비형태
      * holiday- 주일(토,일)

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
      * _mds_id   - 계량기시리얼넘버
      * device_type- 계측 설비형태
        * holiday- 주일(토,일)

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
      * _mds_id   - 계량기시리얼넘버
      * device_type- 계측 설비형태
      * holiday- 주일(토,일)

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
      * _mds_id   - 계량기시리얼넘버
      * device_type- 계측 설비형태
      * holiday- 주일(토,일)

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
    * _mds_id   - 계량기시리얼넘버
  * led_inverter  - 계측 설비형태
    * holiday- 주일(토,일)
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
      * _mds_id   - 계량기시리얼넘버
    * led_inverter  - 계측 설비형태
      * holiday- 주일(토,일)
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
      * _mds_id   - 계량기시리얼넘버
    * led_inverter  - 계측 설비형태
      * holiday- 주일(토,일)
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
      * _mds_id   - 계량기시리얼넘버
    * led_inverter  - 계측 설비형태
      * holiday- 주일(토,일)
```

```
