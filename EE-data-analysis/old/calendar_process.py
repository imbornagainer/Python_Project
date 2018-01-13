
# -*- coding: utf-8 -*-
# Author : jeonghoonkang, https://github.com/jeonghoonkang

import calendar

def dateInt(in_time, mdh):
    # year
    if mdh == 'y':
       re_mdh = int(in_time[0:4])

	# month
    if mdh == 'm':
        if in_time[4] == '0':
            re_mdh = int(in_time[5])
        else:
            re_mdh = int(in_time[4:6])
	# day
    elif mdh == 'd':
        if in_time[6] == '0':
            re_mdh = int(in_time[7])
        else:
            re_mdh = int(in_time[6:8])
	# hour
    elif mdh == 'h':
        if in_time[8] == '0':
            re_mdh = int(in_time[9])
        else:
            re_mdh = int(in_time[8:10])

    return re_mdh


def twodigitZero(in_num):
	if in_num < 10:
		re_num = '0' + str(in_num)
	else:
		re_num = str(in_num)

	return re_num


def nextDate(in_time, in_mdh):
    # next year
    if in_mdh == 'y':
        int_year = dateInt(in_time, 'y')
        next_year = int_year + 1

        re_mdh = str(next_year) + '010000' # next year/01/01/00

    # next month
    if in_mdh == 'm':
        int_month = dateInt(in_time, 'm')
        next_month = twodigitZero(int_month + 1)

        re_mdh = in_time[0:4] + next_month + '00' + in_time[8:10] # next month/01/01
    # next day
    elif in_mdh == 'd':
        int_day = dateInt(in_time, 'd')
        next_day = twodigitZero(int_day + 1)
        re_mdh = in_time[0:6] + next_day + in_time[8:10]

    return re_mdh


def calDate(sttime, ettime):
	w_sttime = sttime
	w_ettime = ettime
	tmp_w_sttime = w_sttime[0:8]

	first_loop = 0

    return "2011"
#    re_datelist = []

#    print "loop"
#    sleep(0.1)

#	print "DEBUG: sttime: %s, ettime: %s" %(sttime, ettime)



# main function
if __name__ == "__main__":

	# differnet year
	sttime = "2017052300"
	entime = "2017052400"

	datelist = []

	datelist = calDate(sttime, entime)
	print "datelist=%s" %datelist
	print "length of datelist: %s" %len(datelist)




'''
	while 1:
        if (first_loop > 0) :
            if w_ettime == ettime :
                print "while loop finished ..."
                break # finish while True
            w_sttime = nextDate(w_sttime, 'd')
            tmp_w_sttime = w_sttime[0:8] #ymd

            # make last day time to 23 hour : 11 PM
            w_ettime = tmp_w_sttime + '23'
            if w_ettime == ettime:

			first_loop = 1
			re_datelist.append([w_sttime, w_ettime])
			break

		else: # start time != end time
			if dateInt(ettime, 'y') == dateInt(w_sttime, 'y'): # same year
				if dateInt(ettime, 'm') > dateInt(w_sttime, 'm'): # different month

				# check the last day of start month
					w_st_calr = calendar.monthrange(int(w_sttime[0:4]), dateInt(w_sttime, 'm'))

					if dateInt(w_sttime, 'd') == w_st_calr[1]: # current day == the last day of stday
						# next month
						re_datelist.append([w_sttime, tmp_w_sttime+'23'])
						w_sttime = nextDate(w_sttime, 'm')
						first_loop = 1
						continue

			else: # different year

				tmp_w_sttime = w_sttime[0:4] # year

				w_st_calr = calendar.monthrange(int(w_sttime[0:4]), dateInt(w_sttime, 'm'))

				if dateInt(w_sttime, 'd') == w_st_calr[1]: # current day == the last day of stday
					re_datelist.append([w_sttime, w_ettime])

					if dateInt(w_sttime, 'm') == 12: # 12 month
						# next year
						w_sttime = nextDate(w_sttime, 'y')
						tmp_w_sttime = w_sttime[0:8]
						first_loop = 1
						continue

					else:
                        # next month
                        w_sttime = nextDate(w_sttime, 'm')
                        tmp_w_sttime = w_sttime[0:8]
                        first_loop = 1
                        continue

                	first_loop = 1

		re_datelist.append([w_sttime, w_ettime])

	return re_datelist
'''
