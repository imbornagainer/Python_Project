###파일 찾기 (파일명 검색)
```
현재 디렉토리에서, pl 확장자를 가진 모든 파일 찾기
find -name '*.pl'

(현재 디렉토리 밑의 하위 디렉토리까지 다 찾습니다.)
```

```
루트에서부터, 즉 전체 하드에서, pl 확장자를 가진 모든 파일 찾기
find / -name '*.pl'
```
```
전체 하드 디스크에서, 파일명이 ab 로 시작하는 모든 파일 찾기
find / -name 'ab*'
```
```
전체 하드 디스크에서, 파일명이 .bash 로 시작하는 모든 파일 찾기
find / -name '.bash*'
```
```
전체 하드 디스크에서, 파일명이 .bash 로 시작하는 모든 파일 찾기
+ ls 명령 형식으로 출력
find / -name '.bash*' -ls

뒤에 -ls 라는 옵션을 붙이면 됩니다.
```


### 디렉토리명 찾기
```
전체 하드 디스크에서, 디렉토리 이름이 et 로 시작하는 모든 디렉토리 찾기
find / -name 'et*' -type d


주의! 옵션 순서를 바꾸면 에러가 납니다.
```