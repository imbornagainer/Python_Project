# -*- coding: utf-8 -*-
#Author : jeonghoonkang https://github.com/jeonghoonkang

import sys
sys.path.append("../")
import _mds_id_170825 as _mds_id


def nodata_over_day(days):
    _in_list = _mds_id.no_data_day_list
    _day = days
    _cnt = 0
    for k in _in_list :
        if k[1] > _day:
            #print k[0], k[1]
            _cnt = _cnt + 1
    return _cnt


if __name__ == '__main__' :

    #print "len of %s =" %'mds_id_list', len(_mds_id_170825.mds_id_list)
    print ( " mds_id_list     %d" %len(_mds_id.mds_id_list))
    print ( " led_list        %d" %len(_mds_id.led_list))
    print ( " inv_list        %d" %len(_mds_id.inv_list))
    print ( " good_list       %d" %len(_mds_id.good_list))
    print ( " bad_list        %d" %len(_mds_id.bad_list))
    print ( " nuri_list       %d" %len(_mds_id.nuri_list))
    print ( " db_list         %d" %len(_mds_id.db_list))
    print ( " unique_list     %d" %len(_mds_id.unique_list))
    print ( " non_unique_list %d" %len(_mds_id.non_unique_list))
    print ( " no_data_list    %d" %len(_mds_id.no_data_day_list))
    print ( " 365_no_data     %d" %len(_mds_id.no_365_list))
   

    tmp = nodata_over_day(30)
    print ( " 30_no_data      %d" %tmp )
    tmp = nodata_over_day(60)
    print ( " 60_no_data      %d" %tmp )
    tmp = nodata_over_day(100)
    print ( " 100_no_data      %d" %tmp )
    tmp = nodata_over_day(150)
    print ( " 150_no_data      %d" %tmp )
    tmp = nodata_over_day(200)
    print ( " 200_no_data      %d" %tmp )

