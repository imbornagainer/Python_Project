# -*- coding: utf-8 -*-
# Author : jeonghoonkang , https://github.com/jeonghoonkang

import datetime
import time
import argparse
import sys
sys.path.insert(0, '../../lib')

import excel_col_to_list

def parse_args():
    story = 'Excel handling code'
    usg = '\n use python OOO.py -exl {filename} -outfile {filename} -start {B1} -end {B102} -sh {number} --help for more info'
    parser=argparse.ArgumentParser(description=story, usage=usg, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-exl",    default=None, help="input excel file name")
    parser.add_argument("-outfile",  default="out.txt", help="output filename")
    parser.add_argument("-listname",  default="list", help="list name ")
    parser.add_argument("-start",    default=None, help="start column number")
    parser.add_argument("-end",   default=None, help="end column number")
    parser.add_argument("-sh", default=None, help="sheet number of excel sheets ")
    args = parser.parse_args()
   
    if len(sys.argv) < 2:
        print usg
        exit("    please add more arguemnts like above line")

    return args.exl, args.outfile, args.listname, args.start, args.end, args.sh

if __name__ == "__main__":

    exl, outfile, listname, start, end, sh = parse_args()

    #buf, length = excel_col_to_list.get_list(u"./(EE)list_002.xlsx", 'T4', 'T539', 2)
    buf, length = excel_col_to_list.get_list(exl, start, end, sh)

    buf = excel_col_to_list.rm_None(buf)

    print buf 
    print length
   
    of = open (outfile, 'w+')
    of.write(listname +'=')
    of.write(str(buf))
    of.close()


