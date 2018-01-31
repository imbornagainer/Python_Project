#OpenTSDB 설치과정#

1. 설치를 진행하기 전에 설치되어 있어야할 것들:
 -java 1.7이상
  1- sudo add-apt-repository ppa:webupd8team/java 
  2- sudo apt-get update
  3- sudo apt-get install oracle-java8-installer (apt-cache search keyword로 검색가능)
  4- 일반적으로 /usr/lib/jvm/ 에 설치되어 있다
  5- JAVA_HOME 설정 ( /etc/profile )
   - JAVA_HOME=/usr/lib/jvm/java-8-oracle
     PATH=$PATH:$JAVA_HOME
     export JAVA_HOME
     export PATH
   -source /etc/profile
  - (추가적으로) hbase 가 설치되면, hbase/hbase-env.conf에 JAVA_HOME을 설정    해주어야 한다 (설정하지 않을 경우, “JAVA_HOME is not set” 에러 발생)


 -hbase 0.92 이상
  1- http://www.apache.org/dyn/closer.cgi/hbase/에서 미러페이지 접속 
  2- 특정 버전에 대한 다운로드 링크 복사
  3- wget 다운로드링크 (wget명령어로 웹에 있는 파일을 다운로드 가능)
  4- 해당 파일 압축해제 ( tar xfz 압출파일명.tar.gz )
  5- 압축 해제된 폴더로 이동 ( cd hbase-version)
  6- hbase/conf/hbase-site.xml 파일 수정:
   <configuration> <property>           <name>hbase.rootdir</name>          <value>file:///DIRECTORY/hbase</value> 
   </property> 
   <property>
     <name>hbase.zookeeper.property.dataDir</name>       <value>/DIRECTORY/zookeeper</value>
    </property>
   </configuration>
  (DIRECTORY 에는 hbase를 구동할 디렉토리명을 넣는다)
   
 -gnuplot 4.2 이상
 -telnet (telnet을 무조건 설치해야한다. 설치하지 않을 경우, 추후 단계에서 에러 발생)
  -telnet? 원격 접속용 프로그램 
  -rf ) abt_telnet,ssh.doc
 
 rf. 하둡은 설치되어있을 필요 x
  

2. hbase/bin/ $ ./start-hbase.sh
 
3. zookeeper 연결 확인
telnet localhost 2181
stats
    Zookeeper version: 3.4.3-cdh4.0.1--1, built on 06/28/2012 23:59 GMT
    Clients:

    Latency min/avg/max: 0/0/677
    Received: 4684478
    Sent: 4687034
    Outstanding: 0l
    Zxid: 0xb00187dd0
    Mode: leader
    Node count: 127182
    Connection closed by foreign host.
4. OpenTSDB 설치
cd /usr/local
git clone git://github.com/OpenTSDB/opentsdb.git


5. cd opentsdb
sudo ./build.sh
(telnet이 설치되어 있지 않으면 이 과정에서 에러 발생 : “zookeeper ~~~”)
(autoreconf: not found 에러 발생 시 dh-autoreconf 설치)

5.5. sh build.sh debian 
       ./build/opentsdb-version/opentsdb-versin.deb 파일 설치
       ( dpkg -i opentsdb-version_all.deb )
       
위 내용을 실행하면 다음과 같은 디렉토리가 생성된다:
/tmp/opentsdb - Temporary cache files
/etc/opentsdb - Configuration files
/usr/share/opentsdb - Application files
/usr/share/opentsdb/bin - The "tsdb" startup script that launches a TSD or command line tools
/usr/share/opentsdb/lib - Java JAR library files
/usr/share/opentsdb/plugins - Location for plugin files and dependencies
/usr/share/opentsdb/static - Static files for the GUI
/usr/share/opentsdb/tools - Scripts and other tools
/var/log/opentsdb - Logs




6. /usr/share/opentsdb/tools/ $ sudo env COMPRESSION=NONE HBASE_HOME=/hbase/설치/폴더 ./src/create_table.sh
→ 명령어 env : run a program in a modified environment
env [OPTION] … [ -  ] [NAME=VALUE]…… [COMMAND] : NAME변수값을 VALUE로 설정한 후 명령어(./src/create_table.sh) 수행


7. 다음을 통해 서버에 db생성
opentsdb/build $ sudo./tsdb tsd --port=44242 --staticroot=./staticroot --cachedir=/usr/local/data --auto-metric
(포트번호 44242는 서버에서 포트포워딩한 것으로 변경되었을 수 있음)

*opentsdb/build-aux/rpm/opentsdb.conf 파일에 default configuration이 설정되어 있다. 실행 시 바인딩될 네트워크 주소 지정이 가능하다* 

*바인드된 네트워크 주소에(125.140.110.217:44242) 웹으로 접속

*tsd 명령은 opentsdb daemon을 foreground로 실행하여 tcp,http를 통해 연결을 수락한다
오류 :
1. HBaseClient: The znode for the -ROOT- region doesn't exist
→ opentsdb.conf 파일에서 zk_basedir = 주키퍼 설치위치
→ hbase와 opentsdb는 동일한 주키퍼 설정을 갖고 있어야함
→ hbase/conf/hbase-site.xml, opentsdb/src/opentsdb.conf 내용 확인

2. duplicate timestamp for a key ~~
→ 특정 타임스탬프에 동일한 타입에 대한 값이 존재하면 발생함
→ 실행 프로그램에서 임의의 타임스탬프에 대해 동일한 tag하의 value값을 넣는지 확인
→ 위에 해당이 안된다면, opentsdb 설정파일에 duplicate timestamp to a key value에 대한 작동 방식 지정
 → opentsdb/src/opentsdb.conf 에서 tsd.storage.fix_duplicates = true 내용 추가 후  /etc/opentsdb/ 에 파일 복사
