#!/usr/bin/env Python3
# -*- coding: utf-8 -*-
# 
# Name   : demo
# Fatures:
# Author : qianyong
# Time   : 2017/9/21 15:22
# Version: V0.0.1
#

import sys, os
import re
import redis
if __name__ == '__main__':
    # js_dir = os.path.join(os.path.abspath('.'),'js')
    # if not os.path.exists(js_dir):
    #     os.makedirs(js_dir)
    # url = 'http://bbs.fallenark.com/forum.php?mod=viewthread&tid=40088&mobile=1'
    # filename = ''.join([re.findall('tid=(.*?)&',url)[0],'.js'])
    # filepath = os.path.join(js_dir,filename)
    # with open(filepath,'w') as f:
    #     f.write(url)
        # f.close()

    import pymysql
    from pandas import DataFrame
    import pandas as pd

    connect = pymysql.connect(host="localhost", user="root", port=3306, db="world", password='microsoft1995')
    cur = connect.cursor()
    sql = "select * from city"
    a = pd.read_sql(sql, connect)

    print(a)

