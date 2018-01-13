1. no_zero_value_copy_daily_onelist_khj_ver0.2.py - 메트릭 수정, 복사, value가 0인 data 제거 소스 실행방법
	* 이 함수는 metric의 data를 기간의 시작부터 끝까지 하루씩 get하고 put한다.
		* get하는 data가 너무 많아 Max retries exceeded를 방지하기 위한 소스
		* data 중에서 value가 0이 data만 제거하기 위한 소스
	1. if __name__ == '__main__':의 설정값을 입력하는 부분에서 각 변수에 입력을 한다.
		```
		# 1. 설정값 입력 - 시작
		host  = '125.140.110.217'                                       # get할 url
		port  = 4242                                                    # get할 port 번호
		query = 'http://{0!s}:{1!r}/api/query'.format(host, port)       # opentsdb에서 get할 url 주소
		put   = 'http://{0!s}:{1!r}/api/put?summary'.format(host, port) # opentsdb에서 put할 url 주소
		first = '2016/07/01-00:00:00'                                   # get 시작일
		last  = '2016/08/01-00:00:00'                                   # get 종료일
		metric_in  = 'none:rc04_simple_data_v3'                         # get할 metric명
		metric_out = 'rc05_no_zero_modem_test_v2'                       # put할 metric명
		outlier_txt_name = 'zero_lists_171110_modem_test_v2.txt'        # outlier log를 저장할 txt명
		# 설정 - 끝
		```

	2. 입력하고 싶은 modem list를 작성한다.
		* modem_list= [['01222799986'], ['01220800574']] - 예를 표시한 것

	3. 밑의 함수의 dp['value']의 outlier 범위를 조정한다.
		1. def tsdb_put_telnet(host, port, metric, dps, tags, file='False', outlier_txt_name='outlier.txt'): 함수에서 
		2. if (dp['value'] != 0):의 조건을 조정한다.
