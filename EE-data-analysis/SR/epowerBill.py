# -*- coding: utf-8 -*-
# Author : jeonghoonkang , https://github.com/jeonghoonkang

import useTSDB

def ptest(__url, __st, __et, __m):
    tsdbclass = u_ee_tsdb(__url, __st, __et)
    tag = __m
    if (tag == None) : return
    tsdbclass.set_metric(tag)
    print tsdbclass.readTSD()

def rtest(__url, __m, __tag):
    tsdbclass = u_ee_tsdb(__url, None, None, True)
    tsdbclass.set_metric(__m)
    tag = __tag
    if (tag == None) : return
    print tsdbclass.readTSDrecent(tag, 'sum')

def point(__url, __m, __time, __tag):
    tsdbclass = u_ee_tsdb(__url, __time)
    tsdbclass.set_metric(__m)
    tag = __tag
    if (tag == None) : return
    print tsdbclass.readOnePoint(__time, tag, 'sum')


# main function
# python useTSDB.py -url 125.140.110.217 -port 4242 -start 20161101 -end 2016110207 -m origin_data_please
# python useTSDB.py -url tinyos.iptime.org -port 4242 -m rc01.temp.degree -recent True
if __name__ == "__main__":
#    u, p, stime, etime, recent, metric = parse_args()
    u = "tinyos.iptime.org"
    metric = "t_power.WH"
    tag = {'id':'911'}
    ch_day = 26
   
    #currentPrice()
    #todayPrice()

    #yesterdayPrice()
    #lastmonthPrice()

    #graphshowDay()
    #graphshowMonth()
    #graphshowlastMonth()



   # if recent == 'True' :
   #     rt = rtest(u, metric, tag)
   # elif (etime == None) and (stime != None)  :
   #     rt = point(u, metric, stime, tag)

    #def __init__(self, __url, __st = None, __et = None, __r = None) :
    #para1 = 'gyu_RC1_co2.ppm'
    #para2 = {'id':'924'}
    #print get_last_value('125.7.128.53:4242', str(para1), para2)
    #python useTSDB.py -url tinyos.iptime.org -port 4242 -recent True -m rc01.t_power.WH
    #http://tinyos.iptime.org:4242/api/query?start=2017/06/23-00:00:00&end=2017/06/23-00:01:00&m=sum:rc01.t_power.WH{id=911} 

