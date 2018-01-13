# + 개발작업중인 파일
## Metric Copy
* https://github.com/jeonghoonkang/kdatahub/tree/master/EE-data-analysis/YKPK/KHJ/MetricCopy

## Metric Copy + Tag adding
* https://github.com/jeonghoonkang/kdatahub/tree/master/EE-data-analysis/YKPK/KHJ/MetricCopy_Tag_adding

## Metric Copy + outlier deleting
* https://github.com/jeonghoonkang/kdatahub/tree/master/EE-data-analysis/YKPK/KHJ/MetricCopy_outlier_deleting

## 개발중인 코드로 TSDB에 입력한 메트릭
* https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/metrics__info.md

# + 개발목표 (보고서 내용)
```
	1.종합분석
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

## 코드별 실행방법

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
    1. 선정된 업체는 현장에 에너지 절감형 LED, 인버터 등을 새로 설치하고, 해당
       비용중 일부를 에너지공단에서 지원받음
    1. 설치시에. 전체 설치중 5% 부분에 대해 LTE 전력량계를 설치함
	1. 이 LTE 전력량계는 (옴니시스템, 누리텔레콤 등)에서 설치함. 해당 LTE 전력량계의 정보는 엑셀파일로 작성 보관함
    1. 이 LTE 전력량계는 15분 단위로 ORACLE DB에 측정 값을 저장한다
	3. ORACLE DB에 저장된 DATA를 OPENTS DB에 전송, 복사 저장한다
		- 이 DATA는 순수한 DATA이다 
        - DEVICE_TYPE에 대한 구분이 없는 모든 DATA라는 것을 뜻함
        - LTE 모뎀 전화번호만 들어있는 경우
	4. OPENTS DB에 저장된 순수한 DATA에 TAG를 붙여 DATA를 분류한다.
		- EX) DEVICE_TYPE을 구분 LED, INVERTER인지
        - 여기서 매트릭을 새롭게 생성하여 데이터를 복사함
	5. OPENTS DB에는 분류된 값들이 METRIC에 저장된다
	6. 필터링된 Energy data를 graph로 출력한다
	* 참고 pptx
		* https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/Process%20of%20reading%20data.pptx
