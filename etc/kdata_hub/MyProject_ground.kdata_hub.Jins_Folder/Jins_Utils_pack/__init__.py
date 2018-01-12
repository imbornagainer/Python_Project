class Jins_Utils_class():
    
    '''
    ## 함수 : dateInt
    문자열 date를 정수형으로 변환
    parameter1 (in_time) : 문자형 date 값
    parameter2 (mdh) : 연, 월, 일, 시간의 분류 (y, m, d, h)
    반환 (re_mdh) : 변환 된 정수
    '''
    def dateInt(self,in_time, mdh):
        # year
        if mdh == 'y': re_mdh = int(in_time[0:4])
        # month
        if mdh == 'm':
            if in_time[4] == '0': re_mdh = int(in_time[5])
            else: re_mdh = int(in_time[4:6])
        # day
        elif mdh == 'd':
            if in_time[6] == '0': re_mdh = int(in_time[7])
            else: re_mdh = int(in_time[6:8])
        # hour
        elif mdh == 'h':
            if in_time[8] == '0': re_mdh = int(in_time[9])
            else: re_mdh = int(in_time[8:10])
        return re_mdh
    
    '''
    ## 함수 : twodigitZero
    한자리 정수 에 0을 추가
    '''
    def twodigitZero(self,in_num):
        if in_num < 10: re_num = '0' + str(in_num)
        else:
            re_num = str(in_num)
        return re_num