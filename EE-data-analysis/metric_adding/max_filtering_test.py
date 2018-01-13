# -*- coding: utf-8 -*-
# Author : jeonghoonkang https://github.com/jeonghoonkang

import _2016_list

if __name__ == "__main__" :

    vals = _2016_list.__list
    idxs = len(vals)
    
    maxv = max(vals)
    minv = min(vals)
    sumv = sum(vals, 0.0)
    avgv = sumv / idxs
    print maxv 
    print minv 
    print sumv 
    print avgv 

    _1000vals = []
    _50vals = []
    for ix in range(idxs):
        if vals[ix] > 1000 : _1000vals.append([ix,vals[ix]])
        elif vals[ix] > 50 : _50vals.append([ix,vals[ix]])
    print _1000vals
    print _50vals

