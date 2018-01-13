### Screen이란?
* Screen이란 Linux에서 물리적인 터미널을 여러 개의 가상 터미널로 다중화해주는 도구입니다. 각 가상 터미널은 독립적으로 동작하며 사용자 세션이 분리되어도 동작합니다. 간단히 말하면 이 도구는 백그라운드로 동작하는 다중 터미널을 만들어 줍니다. 이걸 이용해서 백그라운드 작업을 간단히 수행할 수도 있고 회사에서 작업하던 터미널 화면을 집에 가서도 같은 터미널 화면을 보며 작업을 이어 할 수도 있습니다.

* Install
  * screen 이라는 명령어를 실행했을때 명령어가 없다고 나오면 아래와 같이 설치를 해줍니다.

* cygwin
  * apt-cyg install screen

* RedHat계열 (RedHat, CentOS, Fedora 등...)
  * yum install screen
  * Debian 계열(Ubuntu 등..)
  * apt-get install screen

* 사용법 - 참고 url
  * http://dreamlog.tistory.com/470

* 추가 환경 설정
  * 아래와 같이 설정 파일을 추가해주면 Screen 사용 시 좀 더 편해집니다. 적용하시는 것을 추천합니다. 각 가상 터미널의 창 구분도 되고 시계도 표시되는 등 더 보기 편해집니다.
  
* vi ~/.screenrc

```
defscrollback 5000
termcapinfo xterm* ti@:te@
startup_message off
hardstatus on
hardstatus alwayslastline
hardstatus string "%{.bW}%-w%{.rW}%n*%t%{-}%+w %= %c ${USER}@%H"
bindkey -k k1 select 0
bindkey -k k2 select 1
bindkey -k k3 select 2
왼쪽이 추가 환경 설정이 적용된 모습이며 오른쪽이 아무 설정도 하지 않고 screen을 실행했을 시 모습입니다. 추가 환경 설정을 하여 Screen을 사용하고 있는지, 어느 가상 터미널에 있는지 확인할 수 있습니다.
```

### Screen 명렁어
```
1. 쉘모드 명령어
(1) screen

- screen 을 시작 하는 기본 명령입니다.
- 기본 세션명으로 시작합니다.

(2) screen -S 세션명
-S 다음에 주는 세션명으로 시작합니다.
- screen -list
: -list 옵션을 주고 실행하면 이전에 작업했었던 screen 리스트가 있으면 세션명과 함께 리스트를 보여줍니다.

(3) screen -R 세션명

: 이전에 세션이 있을 경우 -R 다음에 오는 세션명으로 이전 작업을 불러옵니다.
: -R 다음에 세션명을 주지 않았을 경우에는 이전 세션이 한개만 있을 경우 그 작업을 불러옵니다.
: 이전 작업이 여러개 있을 경우에는 이전 작업 리스트를 보여줍니다.
: 세션명을 가진 세션이 없다면 새로운 세션을 만들어서 보여줌. (안만들려면 소문자 -r을 사용할 것)

(3) screen -D -r 세션명

: 이전 세션이 Attach 된 상태라면 Detach하고 세션을 복원해 줌.

2. screen 실행후 명령어

screen 실행후의 명령어는 Ctrl-a로 시작합니다:
Ctrl-a, c : (create) 새로운 쉘이 생기면서 그 쉘로 이동
Ctrl-a, a : 바로 전 창으로 이동
Ctrl-a, n : (next) 다음 창으로 이동
Ctrl-a, p : (previous) 이전 창으로 이동
Ctrl-a, 숫자 : 숫자에 해당하는 창으로 이동
Ctrl-a, ' : 창번호 또는 창이름으로 이동 ( ' => 싱글 쿼테이션 )
Ctrl-a, " : 창번호를 보여준다. ( " => 더블 쿼테이션 )
Ctrl-a, A : 현재 창의 title을 수정
Ctrl-a, w : 창 리스트 보여주기
Ctrl-a, esc : Copy 모드로 전환. Copy 모드에서는 vi의 이동키로 이동을 할 수 있다.
Crtl-a, [ 커서 이동을 할 수 있고 특정 블럭을 복사하는 기능으로 사용한다.
먼저 시작 위치에서 space 바를 누르고 끝 위치에서 space 바를 누르면 해당 부분이 buffer로 복사된다.
Ctrl-a, ] : buffer의 내용을 stdin으로 쏟아 넣는다.
이 기능은 vi의 입력모드에서 사용하면 유용하다.
Ctrl-a, :(콜론) : 명령행 모드로 전환
Ctrl-a, d : (detach) 현재 작업을 유지하면서 screen 세션에서 빠져나옴
세션이 종료 되지 않습니다.
Ctrl-a, x : lock screen
아래 부분은 창을 나눠서 사용하는 명령입니다.
Ctrl-a, S : (split) 창을 나눔 (region)
Ctrl-a, Tab : 다른 region으로 이동
Ctrl-a, Q : 현재 region을 제외한 나머지 숨기기

그리고 마지막 명령으로 세션을 완전히 빠져 나오는 명령입니다.
exit : screen 의 쉘상에서 exit 를 치고 엔터를 하면 세션이 완전히 종료 됩니다.
