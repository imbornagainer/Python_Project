#!/usr/bin/python
#-*- coding: utf-8 -*-
# title    ProgressBar class
# file     progressBar.py
# date     2016.04.05
# refer    http://www.whatisthis.top/questions/11048/text-progress-bar-in-the-console
import sys
class ProgressBar():
    PROGRESS_BAR_LENGTH = float(50) # 콘솔창에서 보여질 bar의 길이
    def __init__(self, end, start=0): # 처음 객체생성할때 파라메터를 1개만 준다. 
                                    # 변수 end에 할당이됨. 
                                    # 만약 start(처음 시작 퍼센트)를 정하고싶으면 파라메터를 2개주면됨
        self.start = start
        self.end = end
        self.bar_length = self.PROGRESS_BAR_LENGTH
        self.setLevel(self.start) # 처음 객체가 생성될때 level은 0
        self.plotted = False
    def setLevel(self, level, initial=False): # setProgress로부터 level을 넘겨받아 
                                            # 현재의 진행상황을 percentage형태로 설정한다
        self.level = level
        if level < self.start:
            self.level = self.start
        if level > self.end:
            self.level = self.end
        self.ratio = float(self.level - self.start) / \
            float(self.end - self.start)
        self.level_string = int(self.ratio * self.bar_length)
    def drawProgress(self): # level이 설정된 만큼 그림을 그리는 함수
        sys.stdout.write("\r  %3i%% [%s%s]" % (
            int(self.ratio * 100.0),
            '#' * int(self.level_string),
            '-' * int(self.bar_length - self.level_string),
        ))
        sys.stdout.flush()
        self.plotted = True
    def setProgress(self, level): # 파라메터를 입력받음
        oldChars = self.level_string
        self.setLevel(level) # level 설정 함수 호출
        if (not self.plotted) or (oldChars != self.level_string):
            self.drawProgress() # 그리기 함수 호출
    def __del__(self): # 객체 소멸자
        sys.stdout.write("\n")