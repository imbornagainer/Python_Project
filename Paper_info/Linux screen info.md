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




########################################################################



1. 실행 예
[root@ns1 ~]# screen -S TodayBackup100 -t FirstList
[root@ns1 ~]# screen -S TodayBackup200 -t SecondList


2. 구동중인 세션으로 로긴 (2개 이상일 경우 세션 정보가 나타남)
[root@ns1 ~]# screen -R
There are several suitable screens on:
12171.TodayBackup100 (Detached)
13518.TodayBackup200 (Detached)
Type "screen [-d] -r [pid.]tty.host" to resume one of them.

3. 두 개 세션 중 TodayBackup200 으로 로그인
[root@ns1 ~]# screen -R 13518.TodayBackup200 또는
[root@ns1 ~]# screen -S TodayBackup200 

4. Screen 상태에서 일반 터미널로 나가기
Ctrl + a, d

==========================================================================================

screen
Multiplex a physical terminal between several processes (typically interactive shells).

Syntax:
 
   Start a screen session:

      screen [ -options ] [ cmd [args] ]

   Resume a detached screen session:

      screen -r [[pid.]tty[.host]]

      screen -r sessionowner/[[pid.]tty[.host]]

Options:

   -A -[r|R]     Adapt all windows to the new display width & height.
   -c file       Read configuration file instead of .screenrc
   -d (-r)       Detach the elsewhere running screen (and reattach here).
   -dmS name     Start as daemon: Screen session in detached mode.
   -D (-r)       Detach and logout remote (and reattach here).
   -D -RR        Do whatever is needed to Reattach a screen session.
   -d -m         Start in "detached" mode. Useful for system startup scripts.
   -D -m         Start in "detached" mode, & don't fork a new process.
   -list         List our SockDir and do nothing else (-ls) 
   -r            Reattach to a detached screen process.
   -R            Reattach if possible, otherwise start a new session.
   -t title      Set title. (window's name).
   -U            Tell screen to use UTF-8 encoding.
   -x            Attach to a not detached screen. (Multi display mode).
   -X            Execute cmd as a screen command in the specified session.
			
Interactive commands (default key bindings):

     Control-a ?    Display brief help
     Control-a "    List all windows for selection
     Control-a '    Prompt for a window name or number to switch to.
     Control-a 0    Select window 0
     Control-a 1    Select window 1
     ...            ...
     Control-a 9    Select window 9
     Control-a A    Accept a title name for the current window.
     Control-a b    Send a break to window
     Control-a c    Create new window running a shell
     Control-a C    Clear the screen
     Control-a d    Detach screen from this terminal.
     Control-a D D  Detach and logout.
     Control-a f    Toggle flow on, off or auto.
     Control-a F    Resize the window to the current region size.
     Control-a h    Write a hardcopy of the current window to file "hardcopy.n"
     Control-a H    Begin/end logging of the current window to file "screenlog.n"
     Control-a i    Show info about this window.
     Control-a k    Kill (Destroy) the current window.
     Control-a l    Fully refresh current window
     Control-a M    Monitor the current window for activity {toggle on/off}
     Control-a n    Switch to the Next window
     Control-a N    Show the Number and Title of window
     Control-a p    Switch to the Previous window
     Control-a q    Send a control-q to the current window(xon)
     Control-a Q    Delete all regions but the current one.(only)
     Control-a r    Toggle the current window's line-wrap setting(wrap)
     Control-a s    Send a control-s to the current window(xoff)
     Control-a w    Show a list of windows (windows)
     Control-a x    Lock this terminal (lockscreen)
     Control-a X    Kill the current region(remove)
     Control-a Z    Reset the virtual terminal to its "power-on" values
     Control-a Control-\    Kill all windows and terminate screen(quit)
     Control-a :    Enter command line mode(colon)
     Control-a [    Enter copy/scrollback mode(copy)
     Control-a ]    Write the contents of the paste buffer to stdin(paste)
     Control-a _    Monitor the current window for inactivity {toggle on/off}
     Control-a *    Show  a listing of all currently attached displays.
When screen is called, it creates a single window with a shell in it (or the specified command) and then gets out of your way so that you can use the program as you normally would.

Then, at any time, you can:

Create new (full-screen) windows with other programs in them (including more shells)

Kill existing windows

View a list of windows

Switch between windows - all windows run their programs completely independent of each other. Programs continue to run when their window is currently not visible and even when the whole screen session is detached from the user's terminal.

The interactive commands above assume the default key bindings. You can modify screen’s settings by creating a ~/.screenrc file in your home directory. This can change the default keystrokes, bind function keys F11, F12 or even set a load of programs/windows to run as soon as you start screen.

Attaching and Detaching

Once you have screen running, switch to any of the running windows and type Control-a d. this will detach screen from this terminal. Now, go to a different machine, open a shell, ssh to the machine running screen (the one you just detached from), and type: % screen -r

This will reattach to the session. Just like magic, your session is back up and running, just like you never left it.

Exiting screen completely

Screen will exit automatically when all of its windows have been killed.

Close whatever program is running or type `Exit ' to exit the shell, and the window that contained it will be killed by screen. (If this window was in the foreground, the display will switch to the previous window)

When none are left, screen exits.

This page is just a summary of the options available, type man screen for more.

"Growing old is mandatory, but growing up is optional" ~ Motto of the Silver Screen Saddle Pals
