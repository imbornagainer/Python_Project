# -*- coding: utf-8 -*-
# Author : jeonghoonkang , https://github.com/jeonghoonkang
# Author : Eungsoo Lim

import urllib

url = "http://125.140.110.217:4242/q?"
_url = url + "start=" + '2016/11/01-00:00:00' + "&end=" + '2017/04/01-00:00:00'
rqst_url = _url + '&m=sum:origin_data_please{MDS_ID=00-450083522}&o=&yrange=[0:]&wxh=1900x779&style=linespoint&png', "local-filename.jpg
urllib.urlretrieve(")
