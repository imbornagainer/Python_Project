# 데이터 읽어오기.

#### (1) 전체데이터가 들어가 있는 메트릭 : rc04_simple_data_v3

(1)에서 읽어오는 방법:
* useTSDB.py 를 이용하여 read
  * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/EE-data-analysis/lib/useTSDB.py
* read시에 tag 로 모뎀시리얼을 주면 전체데이터에서 하나의 전력량계만 읽을 수 있음
  * 모뎀시리얼은 아래 파일에 있음
    * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/lib/_input_list_17_0906.py

(2) 읽어온 데이터에 추가 tag를 붙여서 write 해야함
* 추가 tag를 붙이는 방법은 추후 아래 (???) 에서 설명
* write를 위해 일단 (1)에서 데이터를 읽어 오고, 데이터는 1 point 씩 읽어옴
  * (데이터 저장 시간 단위) 여기서 1 point 는 (1)에 원본데이터를 저장해서, 데이터가 존재하는 시간인데. 한 전력량계의 원본 데이터를 2016년 7월 1일 0시 15분에 저장했으면, 이 시간에 데이터가 1 포인트 존재함
  * (원본 데이터 결측 존재) 이 리포에서 다루고 있는 모든 데이터는 원래는 2016 7 1 부터 2017 7 1 까지 모두 15분 단위로 데이터가 존재해야 하는데, 전력량계를 현장에 설치한 날짜, 현재 운영 상태에 따라서 데이터가 비어 있다
    * 즉, 모뎀시리얼을 기준으로 데이터를 조회해 보면 데이터 쭉 들어있다가 없기도 하고. 아예 없는 경우도 있다
* write 방법은 두가지가 있음
  * HTTP post 하는 방법으로 저장할 수 있음
    * (예제파일)  https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/ketiwork_20170614/tsdb_insert_device_serial_20170829.py
* Socket 으로 접속하여 String 을 write 하면 입렫됨 "put 메트릭이름 태그키:태그내용 시간 값"
  * (예제파일) https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/YKR/otsdb_put.py

(3) tag를 붙여야 하는 이유
* (다양한 분석) 미터기 전체 통계도 중요하지만. LED 만 통계를 낸다던지. LED중 마트 만 평균을 낸다던지. 다양한 통계 그래프를 만들고. 그 중에 의미있는것을 뽑아내는 작업을 하기 위해 다양한 분석이 가능해야함 
* (OpenTSDB 태그 필요 이유) 데이터 전체값이 db에 있지만. 하나하나 불러서 평균 내는것도 전체 데이터에대한 for loop를 실행해야 하기 때문에. 이런 기능이 이미 들어가 있는 OpenTSdB의 aggregation 기능을 사용하는것이 속도면에서 많은 개선이 가능하다
* 통계 분석 보고서 예제
  * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/2017_0825_%EC%9E%91%EC%84%B1%EC%A4%91.hwp


(4) tag 분이는 방법
* 태그 내용 준비 (예)
  * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/Tag_add_0710/information_list.py
* LED 태그 붙이는 (예)
  * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/Tag_add_0710/led_tag_data.py
* 인버터 태그 붙이는 (예)
  * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/Tag_add_0710/inverter_tag_data.py

