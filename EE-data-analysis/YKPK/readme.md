### 17/10/11 회의내용

- 목표1. 기존 All Data Metric을 읽어서, 다른 Metric 으로 저장
  * 세부 추가기능 : Tags 추가하기
    (예) Led인지 Converter인지

- 목표2. 기존 All Data Metric을 읽어서, 다른 Metric 으로 저장할때, 복잡/다양한 Tags 추가 처리
  * python dic(딕셔너리)를 사용하여 Tag값 정렬하기
    * Tag 입력값에 key, value 값으로, 데이터를 구분할 수 있는 Tag 적용가능

- 목표3. 위의 추가된 Metric 통계값을 이용하여 보고서 작성
* 현재버전 HWP 보고서에 들어있는 기능을 추가한 Metric을 대상으로 실행 확인


### 주요 파일경로

* input_list : 실증사이트 설치된 약 600개 전력량계의 LTE 전화번호
   * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/lib/_input_list_17_0906.py

* OpenTSDB - write data API
   * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/ketiwork_20170614/tsdb_insert_device_serial_20170829.py

* OpenTSDB - read  source API
   * https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/EE-data-analysis/lib/useTSDB.py
   
* 사업 추진 엑셀 파일
   * https://github.com/jeonghoonkang/kdatahub/tree/master/EE-data-analysis/report/excel

### OpenTSDB 주소
- http://125.140.110.217:4242/#start=2016/05/01-00:00:00&end=2017/01/01-00:00:00&m=sum:rc04_simple_data_v3&o=&yrange=%5B0:%5D&wxh=1025x631&style=linespoint
- ssh otsdbusr@125.140.110.217
- passwd : stsdbusr
