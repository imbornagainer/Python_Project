### openTSDB을 위한 Folder

* 시간계 DB - data를 받아서 graph로 출력해줌
* 참고할만한 site가 없다. 밑의 documents를 보며 참고하는 것 외에는...
    * http://opentsdb.net/docs/build/html/user_guide/
    * opentsdb.net/docs/build/html/user_guide/query/examples.html

### Grafana 
* http://125.140.110.217:3000
* admin / admin
* snapshop capture : https://github.com/jeonghoonkang/kdatahub/blob/master/EE-data-analysis/report/howto/grafana.png

### OpenTSDB
* 접속 ssh opentsdb@125.140.110.217
```
opentsdb@PaaS:~$ screen -list
  There are screens on:
     * 4027.tcollector (2017년 10월 24일 13시 10분 29초)       (Detached)
     * 3753.opentsdb   (2017년 10월 24일 13시 10분 13초)       (Detached)
     * 2 Sockets in /var/run/screen/S-opentsdb.
opentsdb@PaaS:~$ screen -r opentsdb

CTRL + C - (openTSDB restart)
↑ 키 눌러서  02_~~~~ 쉘스크립트 실행

Ctrl A + D (화면만 나옴 - 입력된 명령어는 실행중)
```
