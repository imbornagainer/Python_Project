#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import cx_Oracle
import os
import sys
import requests
import json
from types import *
import csv

url = "http://49.254.13.34:4242/api/put"
response ={}


def timeTOunixtime (rlt):
        #YYYY [0:4], MM [4:6], DD [6:8], HH [8:10], m[10:12]
        stime = "%s/%s/%s" %(rlt[6:8], rlt[4:6], rlt[0:4])
        h = rlt[8:10]

	if len(rlt) == 10: # without minutes
		m = '00'
	else:
        	m = rlt[10:12]

        #unixtime need to have 1 sec unit scale
        dechour = int(h)*60*60
        dechour += int(m)*60
        unixday = time.mktime(datetime.datetime.strptime(stime, "%d/%m/%Y").timetuple())
        unixtime = unixday + dechour

        return int(unixtime)


# update temperature
def updateWtemp(in_loc_code, in_row):

        print "YYYYMMDDHH: "+ in_row[1] + ", " + in_loc_code[0] + "... ing"

        uxtime = timeTOunixtime(in_row[1])

        data = {
                "metric" : "rc002.EE.WEATHER_" + in_loc_code[2] + "_LOC_" + in_loc_code[0] + '_' + in_loc_code[1],
                "timestamp" : uxtime,
                "value" : in_row[2],
                "tags" : {
                        "Location" : in_loc_code[0],
                        "Date" : in_row [1],
                        "Factor" : in_loc_code[2]
                }
        }

        ret = requests.post(url, data=json.dumps(data))



# update humidity
def updateWhumi(in_loc_code, in_row):

	print "YYYYMMDDHH: "+ in_row[1] + ", " + in_loc_code[0] + "... ing"

        uxtime = timeTOunixtime(in_row[1])

        data = {
        	"metric" : "rc002.EE.WEATHER_" + in_loc_code[2] + "_LOC_" + in_loc_code[0] + '_' + in_loc_code[1],
                "timestamp" : uxtime,
                "value" : in_row[6],
                "tags" : {
                	"Location" : in_loc_code[0],
                        "Date" : in_row [1],
                        "Factor" : in_loc_code[2]
                }
	}

       	ret = requests.post(url, data=json.dumps(data))


# update temperature
def updateWtemp_graph(in_loc_code, in_row):

        print "YYYYMMDDHH: "+ in_row[1] + ", " + in_loc_code[0] + "... ing"

        uxtime = timeTOunixtime(in_row[1])

	temp = float(in_row[2])/10.0

        data = {
                "metric" : "rc002.EE.WEATHER_" + in_loc_code[2] + "_LOC_" + in_loc_code[0] + '_' + in_loc_code[1] + '_graph',
                "timestamp" : uxtime,
                "value" : temp,
                "tags" : {
                        "Location" : in_loc_code[0],
                        "Date" : in_row [1],
                        "Factor" : in_loc_code[2]
                }
        }

        ret = requests.post(url, data=json.dumps(data))


# update humidity graph
def updateWhumi_graph(in_loc_code, in_row):

        print "YYYYMMDDHH: "+ in_row[1] + ", " + in_loc_code[0] + "... ing"

        uxtime = timeTOunixtime(in_row[1])

	humi = int(in_row[6])/10

        data = {
                "metric" : "rc002.EE.WEATHER_" + in_loc_code[2] + "_LOC_" + in_loc_code[0] + '_' + in_loc_code[1] + '_graph',
                "timestamp" : uxtime,
                "value" : humi,
                "tags" : {
                        "Location" : in_loc_code[0],
                        "Date" : in_row [1],
                        "Factor" : in_loc_code[2]
                }
        }

        ret = requests.post(url, data=json.dumps(data))



# update precipitation
def updateWprec(in_loc_code, in_row):

        print "YYYYMMDDHH: "+ in_row[1] + ", " + in_loc_code[0] + "... ing"

        uxtime = timeTOunixtime(in_row[1])

        data = {
                "metric" : "rc002.EE.WEATHER_" + in_loc_code[2] + "_LOC_" + in_loc_code[0] + '_' + in_loc_code[1],
                "timestamp" : uxtime,
                "value" : in_row[3],
                "tags" : {
                        "Location" : in_loc_code[0],
                        "Date" : in_row [1],
                        "Factor" : in_loc_code[2]
                }
        }

        ret = requests.post(url, data=json.dumps(data))

# update wind
def updateWwind(in_loc_code, in_row):

        print "YYYYMMDDHH: "+ in_row[1] + ", " + in_loc_code[0] + "... ing"

        uxtime = timeTOunixtime(in_row[1])

        data = {
                "metric" : "rc002.EE.WEATHER_" + in_loc_code[2] + "_LOC_" + in_loc_code[0] + '_' + in_loc_code[1],
                "timestamp" : uxtime,
                "value" : in_row[4],
                "tags" : {
                        "Location" : in_loc_code[0],
                        "Date" : in_row [1],
                        "Factor" : in_loc_code[2]
                }
        }

        ret = requests.post(url, data=json.dumps(data))


# update wind graph
def updateWwind_graph(in_loc_code, in_row):

        print "YYYYMMDDHH: "+ in_row[1] + ", " + in_loc_code[0] + "... ing"

        uxtime = timeTOunixtime(in_row[1])

        wind = float(in_row[4])*10

        data = {
                "metric" : "rc002.EE.WEATHER_" + in_loc_code[2] + "_LOC_" + in_loc_code[0] + '_' + in_loc_code[1] + '_graph',
                "timestamp" : uxtime,
                "value" : wind,
                "tags" : {
                        "Location" : in_loc_code[0],
                        "Date" : in_row [1],
                        "Factor" : in_loc_code[2]
                }
        }

        ret = requests.post(url, data=json.dumps(data))

# update wind direction
def updateWwindd(in_loc_code, in_row):

        print "YYYYMMDDHH: "+ in_row[1] + ", " + in_loc_code[0] + "... ing"

        uxtime = timeTOunixtime(in_row[1])

        data = {
                "metric" : "rc002.EE.WEATHER_" + in_loc_code[2] + "_LOC_" + in_loc_code[0] + '_' + in_loc_code[1],
                "timestamp" : uxtime,
                "value" : in_row[5],
                "tags" : {
                        "Location" : in_loc_code[0],
                        "Date" : in_row [1],
                        "Factor" : in_loc_code[2]
                }
        }

        ret = requests.post(url, data=json.dumps(data))


# update sunshine
def updateWsuns(in_loc_code, in_row):

        print "YYYYMMDDHH: "+ in_row[1] + ", " + in_loc_code[0] + "... ing"

        uxtime = timeTOunixtime(in_row[1])

        data = {
                "metric" : "rc002.EE.WEATHER_" + in_loc_code[2] + "_LOC_" + in_loc_code[0] + '_' + in_loc_code[1],
                "timestamp" : uxtime,
                "value" : in_row[11],
                "tags" : {
                        "Location" : in_loc_code[0],
                        "Date" : in_row [1],
                        "Factor" : in_loc_code[2]
                }
        }

        ret = requests.post(url, data=json.dumps(data))


# update sunshine
def updateWsuns_graph(in_loc_code, in_row):

        print "YYYYMMDDHH: "+ in_row[1] + ", " + in_loc_code[0] + "... ing"

        uxtime = timeTOunixtime(in_row[1])

       	if in_row[11]=='':
        	fillzero = 0
       	else:
        	fillzero = in_row[11]

	suns = float(fillzero) * 10

        data = {
                "metric" : "rc002.EE.WEATHER_" + in_loc_code[2] + "_LOC_" + in_loc_code[0] + '_' + in_loc_code[1] + '_graph',
                "timestamp" : uxtime,
                "value" : suns,
                "tags" : {
                        "Location" : in_loc_code[0],
                        "Date" : in_row [1],
                        "Factor" : in_loc_code[2]
                }
        }

        ret = requests.post(url, data=json.dumps(data))



def readCSV():

        sttime = '2017022000'
        ettime = '2017022023'


        factor = ['TEMPERATURE', 'HUMIDITY', 'PRECIPITATION', 'WIND', 'WINDdirection', 'SUNSHINE']

        w_info = [['seoul', '108'], ['incheon', '112'], ['suwon', '119']]

        fname = './data/weather/' + sttime + '-' + ettime + '_db.csv'

        f = open(fname, 'r')
        csvReader = csv.reader(f)

        for row in csvReader:
                for ix in range(len(w_info)):
                        if row[0] == w_info[ix][1]:
                                loc_code_temp = [w_info[ix][0], w_info[ix][1], factor[0]] # temperature, city name, city code, factor
                                loc_code_humi = [w_info[ix][0], w_info[ix][1], factor[1]] # humidity, city name, city code, factor
                                loc_code_prec = [w_info[ix][0], w_info[ix][1], factor[2]] # precipitation, city name, city code, factor
				loc_code_wind = [w_info[ix][0], w_info[ix][1], factor[3]] # wind, city name, city code, factor
                                loc_code_windd = [w_info[ix][0], w_info[ix][1], factor[4]] # wind direction, city name, city code, factor
                                loc_code_suns = [w_info[ix][0], w_info[ix][1], factor[5]] # sunshine, city name, city code, factor


          	updateWtemp(loc_code_temp, row)
		updateWhumi(loc_code_humi, row)
                updateWprec(loc_code_prec, row)
                updateWwind(loc_code_wind, row)
                updateWwindd(loc_code_windd, row)
                updateWsuns(loc_code_suns, row)

		# graph
		updateWtemp_graph(loc_code_temp, row)
                updateWhumi_graph(loc_code_humi, row)
		updateWwind_graph(loc_code_wind, row)
		updateWsuns_graph(loc_code_suns, row)


	f.close()


def re_dayarr(in_year, in_month):

	if in_month == '01' or in_month == '03' or in_month == '05' or in_month == '07' or in_month == '08' or in_month == '10' or in_month == '12':
#		lc = len(day_arr) # 31
        	day_arr = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                   	   '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                           '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                   	   '31']

	elif in_month == '04' or in_month == '06' or in_month == '09' or in_month == '11':
#		lc = len(day_arr) - 1 #30
                day_arr = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                           '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                           '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']

	elif in_month == '02':
		if in_year == '2016':
#			lc = len(day_arr) - 2 # 29
                	day_arr = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                                   '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                   '21', '22', '23', '24', '25', '26', '27', '28', '29']
		else:
#			lc = len(day_arr) - 3 # 28
                        day_arr = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                                   '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                   '21', '22', '23', '24', '25', '26', '27', '28']


#	print day_arr

	return day_arr


def readCSV_month(in_year, in_month):

	day_arr = re_dayarr(in_year, in_month)

	for lc in day_arr:
		sttime = in_year + in_month + lc + '00'
		ettime = in_year + in_month + lc + '23'
#		print sttime

        	factor = ['TEMPERATURE', 'HUMIDITY', 'PRECIPITATION', 'WIND', 'WINDdirection', 'SUNSHINE']

        	w_info = [['seoul', '108'], ['incheon', '112'], ['suwon', '119']]

        	fname = './data/weather/' + sttime + '-' + ettime + '_db.csv'

        	f = open(fname, 'r')
        	csvReader = csv.reader(f)

        	for row in csvReader:
                	for ix in range(len(w_info)):
                        	if row[0] == w_info[ix][1]:
                                	loc_code_temp = [w_info[ix][0], w_info[ix][1], factor[0]] # temperature, city name, city code, factor
#	                               	loc_code_humi = [w_info[ix][0], w_info[ix][1], factor[1]] # humidity, city name, city code, factor
#                                	loc_code_prec = [w_info[ix][0], w_info[ix][1], factor[2]] # precipitation, city name, city code, factor
#                               		loc_code_wind = [w_info[ix][0], w_info[ix][1], factor[3]] # wind, city name, city code, factor
#                                	loc_code_windd = [w_info[ix][0], w_info[ix][1], factor[4]] # wind direction, city name, city code, factor
#                                	loc_code_suns = [w_info[ix][0], w_info[ix][1], factor[5]] # sunshine, city name, city code, factor


#               		updateWtemp(loc_code_temp, row)
#               		updateWhumi(loc_code_humi, row)
#                	updateWprec(loc_code_prec, row)
#                	updateWwind(loc_code_wind, row)
#                	updateWwindd(loc_code_windd, row)
#                	updateWsuns(loc_code_suns, row)

                	# graph
                	updateWtemp_graph(loc_code_temp, row)
#                	updateWhumi_graph(loc_code_humi, row)
#               		updateWwind_graph(loc_code_wind, row)
#               		updateWsuns_graph(loc_code_suns, row)


        f.close()

# main function
if __name__ == "__main__":

	readCSV()
#	readCSV_month('2016', '08')
