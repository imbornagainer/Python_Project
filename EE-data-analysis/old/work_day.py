# -*- coding: utf-8 -*-
# Author : jeonghoonkang, https://github.com/jeonghoonkang
#!/usr/bin/python

import time, datetime

now = time.localtime()
week = ( 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun' )

# Today type
print '오늘 요일: %s' % ( week[now.tm_wday] )

# input a certain day, and return the type of day, which weekday
print week[datetime.date(2017, 05, 24).weekday()]

