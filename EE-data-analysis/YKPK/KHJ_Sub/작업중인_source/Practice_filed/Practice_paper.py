# -*- coding: utf-8 -*-

# float의 0과 int의 0이 같은지 확인하는 함수
def ZeroValueTest():
    if 0.00000000000 != 0:
        print 'a'
    else:
        print 'b'

if __name__ == '__main__':
    dp = [0,100]
    
    #ZeroValueTest()
    outlier_if = dp[0] != 0 and dp[1] <= 100.0
    
    print dp[0]
    print dp[1]
    print outlier_if