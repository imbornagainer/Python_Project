#### 일정

| 목차            | 내용                                | 일정    |
| ------------- | --------------------------------- | ----- |
| 전력량계 갯수 통계 수치 | 전체                                |       |
|               | (1-1) LED                         | 11/23 |
|               | (1-2) 인버터                         | 11/24 |
|               | (1-3) 냉난방기                        | 11/27 |
| 전력량계 분류별 통계   | (2-1) LED 가동율 (건물종류 / 업종별 / 월별)   | 11/24 |
|               | (2-2) 인버터 부하율 (건물종류 / 업종별 / 월별)   | 11/24 |
|               | (2-3) 냉난방기 부하율                    | 11/27 |
| 전력량계 특징 그래프   | (3-1) LED 주요 패턴 (2-1) 관련 항목별 그래프  | 11/24 |
|               | (3-2) 인버터 주요 패턴 (2-2) 관련 항목별 그래프  | 11/24 |
|               | (3-3) 냉난방기 주요 패턴 (2-3) 관련 항목별 그래프 | 11/27 |

11/24일 오전버전 보고서요약 파일
https://cmail.daum.net/v2/mails/000000000000Ewu/attachments/MjoxLjI6Mjg3NDY6NTQyMjg4OmFwcGxpY2F0aW9uL3gtaHdwOmJhc2U2NDpTWk9BUk5lakNCSThNUGFWbG9abkpB/download/EE_%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D_%EA%B8%B0%EB%8A%A5_%EA%B5%AC%ED%98%84%EC%A4%91_1124_009.hwp

#### Grafana에서 보고서에 사용해야할 board들
|          | 가동율                          | 사용율                          | 주중/주말                             | 1일평균                                   | 동절기                                |                                      |
| -------- | ---------------------------- | ---------------------------- | --------------------------------- | -------------------------------------- | ---------------------------------- | ------------------------------------ |
| LED      | ***01EE_LED_가동율(2017/12/06)  | ***02EE_LED 사용율 (171128) ine | ***03EE_LED _주중_주말_(2017/11/27)   | ***04EE_LED_1일_평균_(2017/11/29)         |                                    |                                      |
|          |                              |                              |                                   |                                        |                                    |                                      |
| Inverter | ***11EE_인버터 가동율 (2017/12/07) | ***12EE_인버터 부하율 (171207) ine | ***13EE 171207 인버터 가동율 (주중/주말) HJ | ***04EE_LED_1일_평균_(2017/11/29) 에 일부 있음 |                                    |                                      |
|          |                              |                              | ***13EE tag 171207 인버터 부하율(주중/주말) |                                        | (참고)***20_171206 / 하절기. 동절기. 일간 평균 | (참고)***20_171206 동/하절기 (가동율/사용율)-ine |

![grafana_table](https://raw.githubusercontent.com/jeonghoonkang/kdatahub/master/EE-data-analysis/report/grafa_graph.PNG?token=AOjWa8bQFdfmISJwR0Riklygmrv0aeMHks5aMxnjwA%3D%3D)



#### 해야될 것

* 17/12/08
* 새로운 태그의 list와 dict 추가
  - 추가된 tag
    - detail - 자동차부품, 기계설비, 반도체, 전자전기, 의료
      ![tag_info](https://raw.githubusercontent.com/jeonghoonkang/kdatahub/master/EE-data-analysis/report/tag_info.PNG?token=AOjWa3C0MD0SDM4fOO5ow6nYacqY1a8cks5aM4T2wA%3D%3D)
  - in_list 파일위치
    - kdatahub\EE-data-analysis\lib\in_list.py

- 가동율 구하기
  - test결과 정상
    - 하지만 opentsdb가 계속사용중임 그래서 put시 timeout되는중 작업자 작업 끝나면 실행해야 될 듯 (17/12/08 17:04)
  1. rc05_operation_rate_v6(가동수)를 get하여 tag 추가 및 수정하기
    * 이용할 source : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Copy\Copy_Adjust.py
  2. 위에서 구한 metric을 get하여 가동율 구하기
    * 이용할 source : kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_operationRate.py

- 사용율 구하기 - 사용율 구하는 것은 고민을 해보아야함.
  - modem_num이 살아있는 metric 확인하여 실행해야함
  - 가동율 같은 경우에는 가동수부터 진행하여서 modem이 살아있지만 사용율은 사용수가 아닌 사용율부터 진행됨

- 이후에는 위에것들의 1일 평균을 구해야함.
  - 사용해야 할 source
    - kdatahub\EE-data-analysis\YKPK\KHJ\Main_Program\Calc\Calc_daily_Operation.py

- 그리고 이 새로운 tag들의 grafana의 graph를 그려야 함.(주중/주말, 1일평균, 년별 등등)
- Grafana에서 사용할 board는 위의 표에서 사용할 metric의 정보는 https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/YKPK/KHJ/metrics__info.md

#### 완료

| LED (tag={building : 태그값}) | DICT                         | Value           | 기준총갯수 |
| -------------------------- | ---------------------------- | --------------- | -----  |
| 일반건물                       | {building: office}           | office        | 91    |
| 공장                         | {building : factory}         | factory         | 221   |
| 공동주택                       | {building : apt}             | apt           | 37    |
| 기타                         | {building : etc}             | etc             | 2     |
| 물류센터                       | {building : none}            | none          | 10    |
| 합계                         |                              |                 | 361   |

| LED (tag={detail : 태그값}) | DICT                       | Value           | 갯수   |
| ------------------------ | -------------------------- | --------------- | ---- |
| 건물기타                     | {detail : building_etc}    | building_etc    | 40   |
| 기타                         | {building : etc}             | etc             | 2     |
| 마트                         | {building : mart}            | mart            | 2     |
| 물류센터                       | {building : none}            | none            | 10    |
| 백화점                      | {detail : departmentStore} | departmentStore | 25   |
| 병원                       | {detail: hospital}         | hospital        | 1    |
| 전자대리점                      | {building : electricmart}    | electricmart    | 20    |
| 학교                       | {detail : school}          | school          | 5    | |
| 합계                       |                            |                 | 105  |

| LED (tag={building : 태그값}) | DICT                         | Value           | 기준총갯수 |
| -------------------------- | ---------------------------- | --------------- | ----- |
| 일반건물                       | {building: office}           | office          | 91    |
| 공장                         | {building : factory}         | factory         | 221   |
| 마트                         | {building : mart}            | mart            | 2     |
| 전자대리점                      | {building : electricmart}    | electricmart    | 20    |
| 공동주택                       | {building : apt}             | apt             | 37    |
| 백화점                        | {building : departmentStore} | departmentStore | 3     |
| 기타                         | {building : etc}             | etc             | 2     |
| 병원                         | {building : hospital}        | hospital        | 2     |
| 물류센터                       | {building : none}            | none            | 10    |
| 학교                         | {building : school}          | school          | 5     |
| 합계                         |                              |                 | 393   |


| LED (tag={detail : 태그값}) | DICT                       | Value           | 갯수   |
| ------------------------ | -------------------------- | --------------- | ---- |
| 병원                       | {detail: hospital}         | hospital        | 1    |
| 금속                       | {detail: metal}            | metal           | 28   |
| 제지목재                     | {detail : wood}            | wood            | 15   |
| 요업                       | {detail : ceramic}         | ceramic         | 9    |
| 백화점                      | {detail : departmentStore} | departmentStore | 25   |
| 섬유                       | {detail : fiber}           | fiber           | 22   |
| 학교                       | {detail : school}          | school          | 5    |
| 식품                       | {detail : food}            | food            | 12   |
| 상용                       | {detail : sangyong}        | sangyong        | 72   |
| 산업기타                     | {detail : industryEtc}     | industryEtc     | 122  |
| 건물기타                     | {detail : building_etc}    | building_etc    | 40   |
| 화공                       | {detail : fceramic}        | fceramic        | 8    |
| 합계                       |                            |                 | 359  |

| INVERTER Load (tag={load : 태그값}) | DICT               | Value      | 갯수   |
| -------------------------------- | ------------------ | ---------- | ---- |
| 블로워                              | {load: blower}     | blower     | 3    |
| 컴프레셔                             | {load: compressor} | compressor | 5    |
| 펌프                               | {load : pump}      | pump       | 8    |
| 팬                                | {load : fan }      | fan        | 28   |
| Blank                            | {load : none }     | none       | 6    |
| 합계                               |                    |            | 52   |

| INVERTER (tag={detail : 태그값}) | DICT                       | Value           | 갯수   |
| ----------------------------- | -------------------------- | --------------- | ---- |
| 병원                            | {detail: hospital}         | hospital        | 0    |
| 금속                            | {detail: metal}            | metal           | 3    |
| 제지목재                          | {detail : wood}            | wood            | 1    |
| 요업                            | {detail : ceramic}         | ceramic         | 0    |
| 백화점                           | {detail : departmentStore} | departmentStore | 26   |
| 섬유                            | {detail : fiber}           | fiber           | 1    |
| 학교                            | {detail : school}          | school          | 0    |
| 식품                            | {detail : food}            | food            | 2    |
| 상용                            | {detail : sangyong}        | sangyong        | 4    |
| 산업기타                          | {detail : industryEtc}     | industryEtc     | 13   |
| 건기타                           | {detail : building_etc}    | building_etc    | 0    |
| 화공                            | {detail : fceramic}        | fceramic        | 2    |
| 합계                            |                            |                 | 52   |


