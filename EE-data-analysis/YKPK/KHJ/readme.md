#### 중요 정보

* 작업중인 메트릭 정보
  * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/metrics__info.md

#### 작업 진행 내용

* 12/06
 * 하절기, 동절기 Tag 추가 필요
   * 하절기 7월~9월 동절기 10월 ~ 2월 
 * 업종리스트에 자동차부품등 추가필요
   * 기존 산업기타에서 세부업종 4개 추가
   
* 11/27

  * 냉난방기 Tag Add 하기 92개 리스트 
    * in_list 에 추가
    * 원본 메트릭에. 태그 추가하여 새로운 메트릭에 저장
    * HWP의 EHP 부분 완료

* 11/24

  |  번호  | 완료   | 미완료                                |
  | :--: | :--- | :--------------------------------- |
  |  1   |      | 인버터 숫자 채워 넣기 (HWP) - 갯수 파악         |
  |  2   |      | 냉난방기 Tag add 하기 - rc04_tag_cool_v1 |
  |  3   |      | 기준갯수 구하는 코드                        |
  |  4   |      | 가동율을 %로 그래프로 그리기                   |

  * (2) 냉난방기 엑셀 참고, 메트릭 ( rc04_simple_cool_v1)
    * http://125.140.110.217:4242/#start=2016/07/01-00:00:00&end=2017/07/01-00:00:00&m=zimsum:rc04_simple_cool_v1&o=&yrange=%5B0:%5D&wxh=1045x532&style=linespoint


  * (3) 상수 (LED 갯수 - none 갯수
    * LED 갯수는 in_list 에 있음
    * none 갯수는 메트릭 rc05_none_dp_v4  에서 읽어옴
  * (4)
    * 현재는 (입력된 갯수),  (총갯수) 수치로만 작성됨
    * 비율로 구해야 함 100% 기준
```
백분율 =  100 * TX  / (U - NX) 
전송수 TX = query(operation_rate, tag={예로, led, office}, 시간 t1 기간) 
전송안된수 NX = query(none_dp, tag={예로, led, office}, 시간 t1 기간) 
엑셀에서 구한 대상 총수 U = (dict 안에 들어 있음 dict_LED_빌딩)
(지금 생각해보니, 수집된 데이터중에 0인 비율을 찾아도 될것 것 같음)
```

* 11/23

  - 총 갯수에서 rc05_none_dp_v4 를 빼어주는 코드 구현해야함
    - 예) LED갯수 (393) 에서  rc05_none_dp_v4(tag=led) 갯수를 빼어주어야 함
    - *기준갯수* : 15분 단위로 데이터가 수신되어야 하는
  - 가동율 수치 구하는 코드는 1차 완료되었음
    - calc.py
    - https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/report/calc.py

  * Tag Mark정보
    - https://github.com/jeonghoonkang/kdatahub/tree/master/EE-data-analysis/report

  * LED, INVERTER - 가동률, 사용률 수치정보
    - https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/report/rate.md

  * 보고서 표 작성하기(가동율, 사용율)

    * LED (완료)
      * 전체 1년, 7-8월, 9-10월, 11월-2월, 3월-6월
      * LED 전체, LED 빌딩별, LED 업종별

    * INVERTER (완료 - 월별 가동률을 제외한)
      * 전체 1년, 7-8월, 9-10월, 11월-2월, 3월-6월
      * INVERTER 전체, INVERTER 부하별, INVERTER 업종별

    * 가동률
      * metric - rc05_operation_rate_v6
      * source - kdatahub\EE-data-analysis\report\calc.py
      * 공식
        * duration = 기간갯수(96*날수)
        * 96은 15분의 갯수 즉, 하루를 뜻함
          * 15*4 = 60 (한시간)
          * 4*24 = 96 (하루)
        * base_num = (led_유효갯수 * duration - none갯수) / duration
          * val  = dps의 합
        * val / (base_num * duration)

    * 부하율
      * metric - ___d_tag_test_load_rate_4
      * source - kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Load_factor.py
      * 공식 : (dps_value의 합 / dps_key의 갯수)

    * 업종추가(미정)
      * (EE)list_002.xlsx -> 대리 -> 세부사항 확인후 추가입력할 것인지 말것인지의 여부에 따라서 metric 추가생성

    * 그래프 생성
      * 표를 그래프로 생성하기

    * Load표 info update하기
      * report의 readme.md
        * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/report/readme.md

* 11/22

  * TSDB에 none인 데이터 포인트를 metric 으로 입력 - rc05_none_dp_v4(완료)
    - 입력후 각 LTE 모뎀 갯수에서 빼어서, 새로운 total 갯수 메트릭으로 입력
    - 총 갯수에서 rc05_none_dp_v4 를 빼어주는 코드 구현해야함 
      - 예) LED갯수 (393) 에서  rc05_none_dp_v4(tag=led) 갯수를 빼어주어야 함
      - *기준갯수* : 15분 단위로 데이터가 수신되어야 하는 
  * 오늘 점심시간까지 끝내야하는 것
    * 앞쪽 갯수 확실히 표로 깔끔히 정리
      * 오피스의 경우도, LED / INVERTER 분리해서 통계
    * LED 가동율 숫자로 계산해서 출력
      * API 로 1년치 데이터를 호출해서, 모두 합산해서 평균
    * 분류 방법
      * 전체 1년, 7-8월, 9-10월, 11월-2월, 3월-6월
      * LED 전체, LED 빌딩별, LED 업종별

* 11/21

  * 보고서 부하율(LED는 사용율) 그래프 정리 (완료)
  * TSDB에 none인 데이터 포인트를 metric 으로 입력 - rc05_none_rate_v4(진행중)
    * 입력후 각 LTE 모뎀 갯수에서 빼어서, 새로운 total 갯수 메트릭으로 입력
  * 목표대비 실적을 위한 dict 새로 만들기 (완료)
    * lib/in_list.py - goal_led_list, goal_inv_list
  * TSDB에 Excel - outlier, tag metric 새로입력
    * rc05_excel_copy_tag_v7(outlier 새로설정 0.001 < value <= 200)

* 11/20 (완료)

  * 각 LTE 모뎀 갯수 요약 정리
  * 오라클에서 openTSDB로 데이터 연계 입력 정리 순서 확인
  * 보고서 가동율 
  * 보고서 부하율 (LED는 사용율)   

* 11/17

  * 16일 완료 안된것 진행(해야 함)

  * 목표대비 실적을 위한 dict 만들것 (완료)
    * 코드 위치 : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/lib/in_list.py
  * 추가된 리스트 이름 : goal_led_list, goal_inv_list
  * 엑셀 : (EE)list_002.xlsx
    * LTE modem_num : 목표 측정
      * 계측용량  : 엑셀 3번 sheet, R3
      * 인버터용량 : 엑셀 3번 sheet, Z3

  * TAG 입력하여, 갯수 뽑아주는 code (완료)
    * 코드 위치 : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/Main_Program/Find_PG/Find_excel_list/find_excel_data_makelists_ver0.1.py
    * 입력예 : inverter, factory, blower 입력하면
    * 출력 : 해당 tag가 적용된 LTE modum_num list 와 갯수 출력 (파일+화면)

  * 보고서 한글파일로 제일 앞에 (완료)
  - 파일위치 : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/lib/EE분석보고서_2017_1117_작성.hwp
    - 갯수를 정리한 표를 만들것
      - 총 갯수 / LED 갯수 / 인버터갯수
    - 세부적으로 LED 는
      - 건물 종류, 비즈니스 종류, 기업분류로 표를 만들것
    - 인버터는
      - 부하종류, 비즈니스 종류, 건물종류별로 통계 수치를 표로 만들것

  * max dict 의 최대값이 0인 경우, 다시확인 (확인완료)
  * Binary처리된 rc05_operation_rate_v6의 경우는 발견안됨
  * max_dic.py의 dic에는 확인이 되었으나, 이 경우는 551개인 경우임(모든 LTE넘버)
    * BRC의 가동 내용이 있는 LTE modem_num 경우에....
      * 대부분은 max dict 가 값이 있으나
      * 어떤 경우는 max dict 가 0인 경우가 있음    ​

* 11/16

  * 데이터가 안들어온 LTE 번호는 삭제 (완료)    

    * rc05_operation_rate_v6의 메트릭에서 1년치중 Data가 있는것과 없는것 list를 정리
        * (EE)list_002.xlsx에서 뽑은 tag들의 num을 기준으로 list 정리

    * lib/in_list.py에 정리 (밑의 표의 lists 정리, 수신상태는 보류 - 과정에 따라 결정)

    | 디바이스 종류       | 건물종류           | 비즈니스 종류         | 기업분류          | 부하         |
    | ------------- | -------------- | --------------- | ------------- | ---------- |
    | KEY (device)  | KEY (building) | KEY (business)  | KEY (company) | KEY (load) |
    | LED           | factory        | hospital        | bigcompany    | blower     |
    | INVERTER      | office         | metal           | midcompany    | compressor |
    | metalhalide   | mart           | wood            | smallcompany  | pump       |
    | heungwanglamp | apt            | ceramic         | non_profit    | fan        |
    |               | etc            | departmentstore | etc           | led        |
    |               |                | fiber           |               |            |
    |               |                | school          |               |            |
    |               |                | food            |               |            |
    |               |                | sanyong         |               |            |

  * 추가 LTE 전력량계 데이터를 메트릭에 추가 (준비 완료 - 실행만 하면 됨, but 서버접속에 어려움)
    * Tag 달아서 추가
    * lib/in_list.py - load_list, load_list_json (추가할 엑셀 정보를 기록한 json, modem_num list)
      1. Oracle db에서 해당 modem_num get(읽어오기)해서 TSDB 메트릭에 put - modem_num
        * source 위치 - https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/ketiwork_20170614/tsdb_insert_device_serial_20171116.py (실행만 하면 됨 - 소스 수정해둠)
      2. 1번의 TSDB에 json_list의 load tag를 추가하여 새로운 TSDB 메트릭 생성 - json_list의 modem_num과 load를
        * source 위치 - https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/Main_Program/MetricCopy_etc/MetricCopy_outlier_deleting/Sub/no_outlier_copy_daily_onelist_khj_ver0.3.py(설정값 설정후 )

    * 각 Tag 항목별로 그래프 그리고, 가동율 통계 (진행해야 함)
      * 작성방법
      * https://github.com/jeonghoonkang/kdatahub/issues/15

* 11/15

  * 엑셀을 정리하여 정확한 갯수를 파악할것

    * LED, Inverter, 데이터 없는 갯수

  * LED, Inverter JSON 을 기반으로 LIST 를 만들어서 파일에 기록할것

    * 참고) ~/lib 디렉토리 안에 있는, in_list.py

    | 디바이스 종류       | 건물종류           | 비즈니스 종류         | 기업분류          | 부하         | 수신상태       |
    | ------------- | -------------- | --------------- | ------------- | ---------- | ---------- |
    | KEY (device)  | KEY (building) | KEY (business)  | KEY (company) | KEY (load) | KEY (save) |
    | LED           | factory        | hospital        | bigcompany    | blower     | data_no    |
    | INVERTER      | office         | metal           | midcompany    | compressor | data_90    |
    | metalhalide   | mart           | wood            | smallcompany  | pump       | data_80    |
    | heungwanglamp | apt            | ceramic         | non_profit    | fan        | data_70    |
    |               | etc            | departmentstore | etc           | led        | data_60    |
    |               |                | fiber           |               |            | data_50    |
    |               |                | school          |               |            | data_40    |
    |               |                | food            |               |            | data_30    |
    |               |                | sanyong         |               |            | data_20    |
    |               |                |                 |               |            | data_10    |
    |               |                |                 |               |            | data_0     |
    |               |                |                 |               |            |            |

  * LIST 마다 해야할 작업

    * 각 LIST 의 갯수 카운트, 작성
      * 참고) ~/lib 디렉토리 안에 있는, in_list.py
    * 각 LIST에 대한 가동율 그래프를 그림
      * 0, 1 로만 기록된 가동율


##### 그외 참고 자료

- 태그 Tag 정보

```
# 건물용도(building)
u'공장': 'factory', u'일반건물': 'office', u'마트': 'mart', u'공동주택': 'apt', u'대형마트': 'bigmart', u'기타': 'etc', u'병원': 'hospital', u'전자대리점': 'electricmart',

# 사업장구분(company)
u'대기업': 'bigcompany', u'중견': 'middlecompany', u'중소': 'smallcompany', u'비영리법인': 'biyoung', u'해당없음': 'nono',

# 업종별-세부용도(business, detail)
u'금속': 'metal', u'산업기타': 'industryEtc', u'건물기타': 'building_etc', u'제지목재': 'wood', u'요업': 'ceramic', u'백화점': 'departmentStore', u'섬유': 'fiber', u'학교': 'school', u'식품': 'food', u'화공': 'fceramic', u'상용': 'sangyong',

# 품목(device_type)
u'LED': 'led', u'인버터': 'inverter', u'형광등': 'heungwanglamp', u'메탈할라이드': 'metalhalide',

# 부하(load)
u'블로워': 'blower', u'컴프래서': 'compressor', u'펌프': 'pump', u'팬': 'fan',

#예외(값 안쓴것)
np.NaN: 'none'
```

#### 

##### 보고서 주요 내용

```
    1.1 종합 가동율 및 부하율
	1.1.2 LED 가동율
	1.1.3 인버터 가동율
	1.2 에너지 사용량
	1.2.1 목표대비 실적
	1.2.2 목표대비 실적이 높은 경우
	1.2.3 목표대비 실적이 낮은 경우
	1.3 측정 패턴
	1.3.1 주중 가동율
	1.3.2 주중, LED, FAN, Blower, Pump 가동율
	1.4 최대 피크 패턴
	1.4.1 LED 최대피크 현황
	1.4.2 인버터 최대피크 현황
	1.5 날씨 상관도

	2.유형별 분석
	2.1 일반건물 (업무용, 상업용)
	2.2 공장
	2.3 유통매장
	2.4 공동주택 (지하주차장)
	2.5 학교
	2.6 백화점
	2.7 기타

	3.업종별 분석
	3.1 식품
	3.2 섬유
	3.3 제지, 목재
	3.4 화공
	3.5 금속
	3.6 산업기타

	4.기업 규모별 분석 (품목별 구분)
	4.1 대기업
	4.2 중견기업
	4.3 중소기업
```

##### 코드별 실행방법

> 향후 실행방법은, 소스코드가 있는 디렉토리에, run.sh 형태로 저장해 놓는다
>
> 설명은 readme 중심으로 가볍게 작성

* metric_copy_khj.py - 메트릭 복사코드 실행방법

  1. parse_args 함수에서 get(얻고)하고 싶은 정보들을 작성한다. (help의 like 형식대로 작성하면 된다.)
    ```
    parser.add_argument("-url", default="125.140.110.217", help="URL input, or run fails")
    parser.add_argument("-start", default='2016/07/01-00:00:00', help="start time input, like 2016/07/01-00:00:00")
    parser.add_argument("-end", default='2016/07/02-00:00:00', help="end time input, like 2016/07/02-00:00:00")
    parser.add_argument("-port", default=4242, help="port input, like 4242")
    parser.add_argument("-recent", default="True", help="Time input for recent value")
    parser.add_argument("-m", default="rc04_add_tag_v4", help="metric name")
    ```

  2. main 함수에서 new_metric에 값을 넣어준다.
    * get한 data를 입력하고 싶은 metric의 이름을 입력한다.

  3. input_data에 get에서 얻은 tags값을 입력한다.
    * get한 metric이 변경되었다면 data에 따라서 tags의 name들을 get에서 얻은 data에 맞게 변경해주어야 한다. (밑의 소스를 수정하면 됨)
  ```
  	modem_num = get_list_data[i]['tags']['modem_num']
  	mds_id = get_list_data[i]['tags']['_mds_id']
  	holiday = get_list_data[i]['tags']['holiday']
  	load = get_list_data[i]['tags']['load']
  	company = get_list_data[i]['tags']['company']
  	device_type = get_list_data[i]['tags']['device_type']
  	building = get_list_data[i]['tags']['building']

  	input_data = {
  	    "metric": new_metric,
  	    "timestamp": unix_time,
  	    "value": value,
  	    "tags": {
  		"_mds_id": mds_id,
  		"modem_num": modem_num,
  		"device_type": device_type,
  		"company": company,
  		"load": load,
  		"building":building,
  		"holiday": holiday,
  	    }
  	}
  ```

* adj_copy_all_khj.py - 메트릭 수정 및 복사코드 실행방법
  *	이 소스는 metric의 모든 data를 기간의 범위를 기준으로 get하고 put한다. (data양이 많을때는 Max retries exceeded가 발생할 수 있음. 주의바람 - data가 적을때 속도면에서는 좋음)
  1. parse_args 함수에서 get(얻고)하고 싶은 정보들을 작성한다. (help의 like 형식대로 작성하면 된다.)
    ```
    parser.add_argument("-url", default="125.140.110.217", help="URL input, or run fails")
    parser.add_argument("-start", default='2016/07/01-00:00:00', help="start time input, like 2016/07/01-00:00:00")
    parser.add_argument("-end", default='2017/05/01-00:00:00', help="end time input, like 2016/07/02-00:00:00")
    parser.add_argument("-port", default=4242, help="port input, like 4242")
    parser.add_argument("-recent", default="True", help="Time input for recent value")
    parser.add_argument("-m", default="rc04_simple_data_v3", help="metric name")
    ```

  2. main 함수에서 new_metric에 값을 넣어준다.
    * get한 data를 입력하고 싶은 metric의 이름을 입력한다.

  3. input_data에 get에서 얻은 tags값을 입력한다.
    * get한 metric이 변경되었다면 data에 따라서 tags의 name들을 get에서 얻은 data에 맞게 변경해주어야 한다. (밑의 소스를 수정하면 됨)
  ```
  	mds_id = get_list_data[i]['tags']['_mds_id']
  	holiday = get_list_data[i]['tags']['holiday']
  	led_inverter = get_list_data[i]['tags']['led_inverter']

  	input_data = {
  		"metric": new_metric,
  		"timestamp": unix_time,
  		"value": value,
  		"tags": {
  			"holiday": holiday,
  			"_mds_id": mds_id,
  			"modem_num": adj_modem_num,
  			"led_inverter": led_inverter,
  		}
  	}
  ```

* adj_copy_daily_khj.py - 메트릭 수정 및 복사코드 실행방법
  *	이 함수는 metric의 data를 기간의 시작부터 끝까지 하루씩 get하고 put한다. (get하는 data가 너무 많아 Max retries exceeded를 방지하기 위해 만든 소스)
  1. parse_args 함수에서 get(얻고)하고 싶은 정보들을 작성한다. (help의 like 형식대로 작성하면 된다.)
    ```
    parser.add_argument("-url", default="125.140.110.217", help="URL input, or run fails")
    parser.add_argument("-start", default='2016/07/01-00:00:00', help="start time input, like 2016/07/01-00:00:00")
    parser.add_argument("-end", default='2017/05/01-00:00:00', help="end time input, like 2016/07/02-00:00:00")
    parser.add_argument("-port", default=4242, help="port input, like 4242")
    parser.add_argument("-recent", default="True", help="Time input for recent value")
    parser.add_argument("-m", default="rc04_simple_data_v3", help="metric name")
    ```

  2. main 함수에서 new_metric에 값을 넣어준다.
    * get한 data를 입력하고 싶은 metric의 이름을 입력한다.

  3. input_data에 get에서 얻은 tags값을 입력한다.
    * get한 metric이 변경되었다면 data에 따라서 tags의 name들을 get에서 얻은 data에 맞게 변경해주어야 한다. (밑의 소스를 수정하면 됨)
  ```
  	mds_id = get_list_data[i]['tags']['_mds_id']
  	holiday = get_list_data[i]['tags']['holiday']
  	led_inverter = get_list_data[i]['tags']['led_inverter']

  	input_data = {
  		"metric": new_metric,
  		"timestamp": unix_time,
  		"value": value,
  		"tags": {
  			"holiday": holiday,
  			"_mds_id": mds_id,
  			"modem_num": adj_modem_num,
  			"led_inverter": led_inverter,
  		}
  	}
  ```

* no_outlier_copy_daily_khj.py - 메트릭 수정, 복사, outlier제거 소스 실행방법
  * 이 함수는 metric의 data를 기간의 시작부터 끝까지 하루씩 get하고 put한다.
    * get하는 data가 너무 많아 Max retries exceeded를 방지하기 위한 소스
    * data 중에서 outlier만 제거하기 위한 소스
  1. parse_args 함수에서 get(얻고)하고 싶은 정보들을 작성한다. (help의 like 형식대로 작성하면 된다.)
    ```
    parser.add_argument("-url", default="125.140.110.217", help="URL input, or run fails")
    parser.add_argument("-start", default='2016/07/01-00:00:00', help="start time input, like 2016/07/01-00:00:00")
    parser.add_argument("-end", default='2017/05/01-00:00:00', help="end time input, like 2016/07/02-00:00:00")
    parser.add_argument("-port", default=4242, help="port input, like 4242")
    parser.add_argument("-recent", default="True", help="Time input for recent value")
    parser.add_argument("-m", default="rc04_simple_data_v3", help="metric name")
    ```

  2. main 함수에서 new_metric에 값을 넣어준다.
    * get한 data를 입력하고 싶은 metric의 이름을 입력한다.

  3. input_data에 get에서 얻은 tags값을 입력한다.
    * get한 metric이 변경되었다면 data에 따라서 tags의 name들을 get에서 얻은 data에 맞게 변경해주어야 한다. (밑의 소스를 수정하면 됨)
  ```
  	mds_id = get_list_data[i]['tags']['_mds_id']
  	holiday = get_list_data[i]['tags']['holiday']
  	led_inverter = get_list_data[i]['tags']['led_inverter']

  	input_data = {
  		"metric": new_metric,
  		"timestamp": unix_time,
  		"value": value,
  		"tags": {
  			"holiday": holiday,
  			"_mds_id": mds_id,
  			"modem_num": adj_modem_num,
  			"led_inverter": led_inverter,
  		}
  	}
  ```

  4. value값의 조건을 설정한다. - outlier을 제외하기 위해
  ```
  	for (unix_time, value) in get_list_data[i]['dps'].items():
  					if (float(value) < 9000.0):  # 9000.0 으로 설정(value가 float형이므로 9000.0으로 입력)
  ```

  5. outlier log 경로를 설정해준다. - 2개의 경로를 동일하게 설정해주면 된다.
    * 경로가 2개인 이유는 w는 새로만들기 및 덮어쓰기, a는 있던 파일에 이어쓰기이다. (즉, 덮어쓰기를 방지하기 위한 조건이다.)
  ```
  	if chk_num == 1:
  		f = open('D:\BigData_EE\outlier_lists_171027.txt', 'w')
  	else:
  		f = open('D:\BigData_EE\outlier_lists_171027.txt', 'a')
  ```

* copyTSDB.py - 복사코드 실행방법
  * 이 코드는 socket방식으로 전송한다.
  1. parse_args 함수에서 get(얻고)하고 싶은 정보들을 작성한다. (help의 like 형식대로 작성하면 된다.)
    ```
    parser.add_argument("-url",    default="http://125.140.110.217", help="URL input, or run fails")
    parser.add_argument("-start",  default='20160701', help="start time input, like 2016110100")
    parser.add_argument("-end",    default='20160702', help="end time input, like 2016110223")
    parser.add_argument("-port",   default=4242, help="port input, like 4242")
    parser.add_argument("-recent", default=True, help="Time input for recent value")
    parser.add_argument("-m", default='rc04_simple_data_v3', help="metric ")
    parser.add_argument("-wm", default='rc05_no_outlier_copy_test_tag_v5', help="write-metric ")
    ```

  2. 실행하면 끝

* no_outlier_copy_daily_onelist_khj_ver0.3.py - 복사코드 실행방법
  * 이 코드는 socket방식으로 전송한다.
  1. main 함수 안에서 밑의 변수들을 설정
    ```
    # 1. 설정값 입력
    host  = '125.140.110.217'                                       # get할 url
    port  = 4242                                                    # get할 port 번호
    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)       # opentsdb에서 get할 url 주소
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
    first = '2016/07/01-00:00:00'                                   # get 시작일
    last  = '2017/05/01-00:00:00'                                   # get 종료일
    metric_in  = 'none:rc04_simple_data_v3'                         # get할 metric명
    metric_out = 'rc05_no_outlier_lte_v1'                           # put할 metric명
    chk_number = 0                                                  # outlier 횟수
    ```

  2. get할 metric에서 가져올 특정 list 설정 (방법 2중 1택)
    ```
    1. from _input_list_17_0906 import modem_list, led_modem_list, inverter_modem_list #파일에서 가져오기
    2. led_list = [] # 값을 배열리스트로 해당소스에 저장하기
    ```

  3. for문 작성시 위에서 설정한 특정 list의 변수명이 같아야 한다.
    ```
    for lte in lte_list: # ex) 2번의 list를 for문으로 작성시
    ```

  4. outlier 범위설정 및 경로 설정
    ```
    1.	# value값 설정 - 지금은 101미만 인것만
    	if (dp['value'] < 101.0):   # 100이하인 값만 put, 아닌 값은 outlier로 간주 txt로 log저장

    2.	# outlier log 기록함수
    	# open의 경로명을 설정해주어야 한다.
    	def Chk_Outlier(chk_num, adj_modem_num,mds_id,unix_time, value):
    		if chk_num == 1:
    			f = open('outlier_lists_171102_lte_v1.txt', 'w')    # 경로설정 / 덮어쓰기
    			f.write('%d:\n' % chk_num)
    			f.write('modem_num : %s\n' % adj_modem_num)
    			f.write('_mds_id   : %s\n' % mds_id)
    			f.write('unix_time : %s\n' % ts2datetime(unix_time))
    			f.write('value     : %s\n' % value)
    			f.write('\n')
    			f.close()
    		else:
    			f = open('outlier_lists_171102_lte_v1.txt', 'a')    # 경로설정 / 이어쓰기
    			f.write('%d:\n' % chk_num)
    			f.write('modem_num : %s\n' % adj_modem_num)
    			f.write('_mds_id   : %s\n' % mds_id)
    			f.write('unix_time : %s\n' % ts2datetime(unix_time))
    			f.write('value     : %s\n' % value)
    			f.write('\n')
    			f.close()
    ```
  5. 실행

* no_outlier_copy_daily_multilist_khj_ver0.3.py - 복사코드 실행방법
  * 이 코드는 socket방식으로 전송한다.
  1. main 함수 안에서 밑의 변수들을 설정
    ```
    # 1. 설정값 입력
    host  = '125.140.110.217'                                       # get할 url
    port  = 4242                                                    # get할 port 번호
    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)       # opentsdb에서 get할 url 주소
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
    first = '2016/07/01-00:00:00'                                   # get 시작일
    last  = '2017/05/01-00:00:00'                                   # get 종료일
    metric_in  = 'none:rc04_simple_data_v3'                         # get할 metric명
    metric_out = 'rc05_no_outlier_lte_v1'                           # put할 metric명
    chk_number = 0                                                  # outlier 횟수
    ```

  2. get할 metric에서 가져올 특정 list 설정 (방법 2중 1택)
    ```
    1. from _input_list_17_0906 import modem_list, led_modem_list, inverter_modem_list #파일에서 가져오기
    2. led_list = [] # 값을 배열리스트로 해당소스에 저장하기
    ```

  3. for문 작성시 위에서 설정한 특정 list의 변수명이 같아야 한다.
    ```
    for lte in lte_list: # ex) 2번의 list를 for문으로 작성시
    ```

  4. outlier 범위설정 및 경로 설정
    ```
    1.	# value값 설정 - 지금은 101미만 인것만
    	if (dp['value'] < 101.0):   # 100이하인 값만 put, 아닌 값은 outlier로 간주 txt로 log저장

    2.	# outlier log 기록함수
    	# open의 경로명을 설정해주어야 한다.
    	def Chk_Outlier(chk_num, adj_modem_num,mds_id,unix_time, value):
    		if chk_num == 1:
    			f = open('outlier_lists_171102_lte_v1.txt', 'w')    # 경로설정 / 덮어쓰기
    			f.write('%d:\n' % chk_num)
    			f.write('modem_num : %s\n' % adj_modem_num)
    			f.write('_mds_id   : %s\n' % mds_id)
    			f.write('unix_time : %s\n' % ts2datetime(unix_time))
    			f.write('value     : %s\n' % value)
    			f.write('\n')
    			f.close()
    		else:
    			f = open('outlier_lists_171102_lte_v1.txt', 'a')    # 경로설정 / 이어쓰기
    			f.write('%d:\n' % chk_num)
    			f.write('modem_num : %s\n' % adj_modem_num)
    			f.write('_mds_id   : %s\n' % mds_id)
    			f.write('unix_time : %s\n' % ts2datetime(unix_time))
    			f.write('value     : %s\n' % value)
    			f.write('\n')
    			f.close()
    ```

  5. 실행

* no_outlier_adj_daily_multilist_khj_ver0.3.py - get data 수정 후 복사 코드 실행방법
  * 이 코드는 socket방식으로 전송한다.
  1. main 함수 안에서 밑의 변수들을 설정
    ```
    # 1. 설정값 입력
    host  = '125.140.110.217'                                       # get할 url
    port  = 4242                                                    # get할 port 번호
    query = 'http://{0!s}:{1!r}/api/query'.format(host, port)       # opentsdb에서 get할 url 주소
    put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
    first = '2016/07/01-00:00:00'                                   # get 시작일
    last  = '2017/05/01-00:00:00'                                   # get 종료일
    metric_in  = 'none:rc04_simple_data_v3'                         # get할 metric명
    metric_out = 'rc05_no_outlier_lte_v1'                           # put할 metric명
    chk_number = 0                                                  # outlier 횟수
    ```

  2. get할 metric에서 가져올 특정 list 설정 (방법 2중 1택)
    ```
    1. from _input_list_17_0906 import modem_list, led_modem_list, inverter_modem_list #파일에서 가져오기
    2. led_list = [] # 값을 배열리스트로 해당소스에 저장하기
    ```

  3. for문 작성시 위에서 설정한 특정 list의 변수명이 같아야 한다.
    ```
    for lte in lte_list: # ex) 2번의 list를 for문으로 작성시
    ```

  4. outlier 범위설정 및 경로 설정
    ```
    1.	# value값 설정 - 지금은 101미만 인것만
    	if (dp['value'] < 101.0):   # 100이하인 값만 put, 아닌 값은 outlier로 간주 txt로 log저장

    2.	# outlier log 기록함수
    	# open의 경로명을 설정해주어야 한다.
    	def Chk_Outlier(chk_num, adj_modem_num,mds_id,unix_time, value):
    		if chk_num == 1:
    			f = open('outlier_lists_171102_lte_v1.txt', 'w')    # 경로설정 / 덮어쓰기
    			f.write('%d:\n' % chk_num)
    			f.write('modem_num : %s\n' % adj_modem_num)
    			f.write('_mds_id   : %s\n' % mds_id)
    			f.write('unix_time : %s\n' % ts2datetime(unix_time))
    			f.write('value     : %s\n' % value)
    			f.write('\n')
    			f.close()
    		else:
    			f = open('outlier_lists_171102_lte_v1.txt', 'a')    # 경로설정 / 이어쓰기
    			f.write('%d:\n' % chk_num)
    			f.write('modem_num : %s\n' % adj_modem_num)
    			f.write('_mds_id   : %s\n' % mds_id)
    			f.write('unix_time : %s\n' % ts2datetime(unix_time))
    			f.write('value     : %s\n' % value)
    			f.write('\n')
    			f.close()
    ```
  5. get한 tags 수정(adj)
    ```
    1. tsdb_put_telnet의 tag인자를 tags에 원하는 모양으로 수정(adj)
    	def tsdb_put_telnet(host, port, metric, dps, tag, device_type, file='False'):

    	tags = {    # 받은 tag를 원하는 모양으로 가공
    		"holiday": tag['holiday'],
    		"_mds_id": tag['_mds_id'],
    		"modem_num": tag['modem_num'],
    		"device_type": device_type
    	}
    ```

  6. 실행

* Metric info - 테스트가 끝나고, 분석에 사용할 데이터 info
  * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/metrics__info.md

* Data 단계별로 진행되는 사항 - 오라클에서 데이터 읽어오는 부분부터 해서 단계별로 진행되는 사항
    1. 에너지공단에서 (에너지 절감 지원사업)으로 경쟁 모집
    2. 선정된 업체는 현장에 에너지 절감형 LED, 인버터 등을 새로 설치하고, 해당
       비용중 일부를 에너지공단에서 지원받음
    3. 설치시에. 전체 설치중 5% 부분에 대해 LTE 전력량계를 설치함
    4. 이 LTE 전력량계는 (옴니시스템, 누리텔레콤 등)에서 설치함. 해당 LTE 전력량계의 정보는 엑셀파일로 작성 보관함
    5. 이 LTE 전력량계는 15분 단위로 ORACLE DB에 측정 값을 저장한다
    6. ORACLE DB에 저장된 DATA를 OPENTS DB에 전송, 복사 저장한다
      - 이 DATA는 순수한 DATA이다
        - DEVICE_TYPE에 대한 구분이 없는 모든 DATA라는 것을 뜻함
        - LTE 모뎀 전화번호만 들어있는 경우
    7. OPENTS DB에 저장된 순수한 DATA에 TAG를 붙여 DATA를 분류한다.
      - EX) DEVICE_TYPE을 구분 LED, INVERTER인지
        - 여기서 매트릭을 새롭게 생성하여 데이터를 복사함
    8. OPENTS DB에는 분류된 값들이 METRIC에 저장된다
    9. 필터링된 Energy data를 graph로 출력한다
    * 참고 pptx
      * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/Process%20of%20reading%20data.pptx
