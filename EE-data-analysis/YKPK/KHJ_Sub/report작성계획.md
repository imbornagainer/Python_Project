# 보고서용 메트릭 

* 메트릭생성. 
  * 아웃라이어 메트릭에서 0값을 모두 제외한 메트릭 복사 생성. 
  * 가동여부는 카운트로 호출하면 될것 같음. 
    * 입력된 메트릭에서 각 LTE ID 측정값을 읽어와서.. 모두 1로 변경 (바이너리
      변환)
  * 추후. 기준값이 0값이 아닌 0.5등의 값으로 변경할 수 있도록 고려해서 코드 작성

| 이름 | 메트릭명 | 내용 | 실행코드 파일이름|
|:-------------:|:-------------:| :-----:| :-----:|
| 원본 데이터 | rc04_simple_data_v3 | 오라클DB에서 복사한 데이터 | |
| outlier제거 데이터 | rc05_operation_tag_v1 | 일정크기 이상은 제외 | |
| Tag 추가 데이터 | rc05_operation_tag_v1 | 태그 추가, 그러나 업종은 아직 추가 안함 | |
| Tag 추가 데이터 | rc05_operation_tag_v2 | 태그 추가, 업종추가 그러나 세부사항은 아직 추가 안함 | |
| Tag 추가 데이터 | rc05_operation_tag_v3 | 태그 추가 세부사항 존재(금속 등등) | |

# 분석 대상 LTE 모뎀번호 리스트 정리
| 이름 | 유형 | 갯수 | 참고 |
|:-------------:| :-------------:|:-------------:| :-----:|
| 총 LTE 모뎀 갯수|  | 455 | 엑셀 갯수 |
| LED 갯수 | 데이터 존재 |  |
| LED 갯수 | 데이터 없는것 |  |
| LED 갯수 | 일반건물 | 28 |
| Inverter 갯수 | 데이터 존재 |  |
| Inverter 갯수 | 데이터 없는것 |  |
| Inverter 갯수 | 일반건물 | 0 |


# 작성 목차

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

