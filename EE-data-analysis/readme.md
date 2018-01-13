
### TAG 구성방법 

* 업종정보,기업유형이 추가된 태그정보!


![image](https://user-images.githubusercontent.com/16898385/26900044-f97cf080-4c0b-11e7-90a3-108b925d0314.png)

* 원본데이터 Metric 이름 : "origin_data_please"

* 기간별 가공된 가동률 Data Metric Name : "daily_workingrate"

* 기간별 가공된 누적가동률 Data Metric Name : "nuzuk_workingrate"


* 태그정보는 위의 그림정보와 동일

* 원본 데이터 넣는 코드

https://github.com/jeonghoonkang/kdatahub/tree/master/EE-data-analysis/ketiwork_20170614

tsdb_insert_origin_20170614.py  검은색으로 칠해진 데이터들
tsdb_insert_origin_inverter_20170612.py	-inverter100개
tsdb_insert_origin_led_20170612.py -led400개

* 엑셀추출 및 데이터비교후 정보(기업정보,,,,)가져오기 코드

https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/ketiwork20170608/excel_shell_find.py


< 이전 태그 내용 >

 mdsid | | | | |
----|----|----|-----|-----
 Holiday| 1(주말) | 0(휴일) | | | |
 led_inverter | LED |INVERTER | heongkwangdeung (형광동) | metalhalaid (메탈라이드)
 factory_mart | factory | apt | mart | office
 fan_pump | fan | pump | compressor | blower


### 데이터 처리 방법
  - DB 접근 및 데이터 저장방안
   - https://docs.google.com/drawings/d/1cVzy25tO-5FVGi5I7qstN-YWbdPDwwSXxSt16_g5vvY/edit?usp=sharing

### cx Oracle 설치
  - cx Oracle 전반적 설치 설명
    - https://oracle.github.io/odpi/doc/installation.html
  - Windows 에서 pip 로 설치하는 예전방법 설명
    - 경로, 파일명은 다름. 이해에 참조만 할것
    - http://ba6.us/?q=cx_Oracle_easy_windows_install

#### windows10 , Cygwin 환경
  - pip 설치 방법이 있음 (Cygwin내에서 실행)
     - pip install cx_Oracle --pre
     - https://oracle.github.io/python-cx_Oracle/
   - 라이브러리 설치가 어려움 (설치참조 : https://oracle.github.io/odpi/doc/installation.html)
     1. Visual Studio redistributable 설치
        - 12.2 : VS 2013 설치
     2. Instant Client zip 설치
        - Download the "Basic" or "Basic Light" zip file from here (64-bit or 32-bit)
          - http://www.oracle.com/technetwork/topics/winx64soft-089540.html
        - Set the environment variable PATH to include the path
          - update PATH in Control Panel -> System -> Advanced System Settings -> Advanced -> Environment Variables -> System Variables -> PATH
          - 설치후 권한설정을 확인해야 함 (권한이 없으면 실행이 안됨)
      3. for Cygwin
        - I set the env Variables like below.
      <pre>
      export ORACLE_HOME=/usr/oracle/instantclient_12_2
      export PATH=$PATH:$ORACLE_HOME
      #export ORIGINAL_PATH=$ORIGINAL_PATH:/cygdrive/c/system/cygwin64/usr/oracle/instantclient_12_2
      export LD_LIBRARY_PATH=$ORACLE_HOME
      export DYLD_LIBRARY_PATH=$ORACLE_HOME
      </pre>    
     4. reboot to apply path & check path of oci.dll
        - "which oci.dll" will show path, check it is correct to you PATH
        - Be carefully if you have multiple-Oracle library (I was in trouble since Orawin92)

#### Oracle SQL 가능한 서버
  - FitPC 
  - addr:49.254.13.34  Bcast:49.254.13.39  Mask:255.255.255.248
  - kdatahub / keti4321
  - tinyos16 / keti098765
  
#### 서버에서 엑셀 다운로드 
   - http://125.141.144.150:8085/aimir-web/gadget/index.jsp
   - keti, keti1234
   


