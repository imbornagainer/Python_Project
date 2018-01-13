1. 개요
   1. 없음
2. 기능
   1. 없음
3. 사용법
   1. list2json.py
      1. 모뎀넘버 리스트를 json 으로 변환
      2. 예제
         1. `python list2json.py -i in_list -l led_list -o led_list.json`
            1. in_list.py 에서 led_list(리스트 이름)를 led_list.json에 json 형태로 출력한다.
         2. `python list2json.py -i in_list -l led_list -r ref_list.xlsx -s 2 -o led_list.json`
            1. in_list.py 에서 led_list(리스트 이름)의 모뎀넘버를 ref_list.xlsx의 3번째 시트에서 검색 후 찾으면 해당 태그를 포함해서 새 리스트에 추가하고 led_list.json에 json 형태로 출력한다.
         3. `ex_json2list.p`
            1. input list가 들어 있는 json 파일로부터 input_list를 추출해서 사용하는 예제가 들어 있다.


