### 파일 쓰기 (writing to file)

* 파이썬에서 파일 쓰기 작업은 아래 예제처럼 간단하게 처리할 수 있다.
    1. f = open('hello.txt', 'w')
    2. f.write('안녕하세요\n')
    3. f.write('你好吗\n')
    4. f.close()

* 파일 작업에서 중요한 것은 파일을 열었다면(open)반드시 닫아줘야(close) 한다는 것이다. 닫는 작업이 번거롭다면 아래처럼 with문을 사용하여 자동으로 닫게 할 수 있다.
    1. with open('hello.txt', 'w') as f:
    2. f.write('안녕하세요\n')
    3. f.write('你好吗\n')

### 파일 내용 추가 (appending to file)

* 기존 파일 내용의 뒷 부분에 새로운 내용을 추가하려면 아래와 같이 하면 된다. (‘w’를 사용할 때 이미 파일이 있는 경우 덮어쓰기 때문에 주의하자.)
    1. with open('hello.txt', 'a') as f:
    2. f.write('こんにちは\n')

### 파일 읽기 (reading to file)

* 이제 파일 내용을 읽어보자. 모든 라인을 읽어오려면 readlines를 사용하자.
    1. with open('hello.txt', 'r') as f:
    2. for line in f.readlines():
    3. print(line)
        
* 한 라인씩 읽기 위해서는 readline을 사용하자. (readline의 경우 대용량 파일을 읽어올 경우 굉장히 유용하다.)
    1. with open('hello.txt', 'r') as f:
    2. print(f.readline()) # '안녕하세요\n'
    3. print(f.readline()) # '你好吗\n'
    
* 전체 내용을 가져오려면 read를 사용하면 된다.
    1. with open('hello.txt', 'r') as f:
    2. content = f.read()
    3. print(content)
