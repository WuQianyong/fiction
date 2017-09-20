#!/usr/bin/env Python3
# -*- coding: utf-8 -*-
# 
# =========================================
# forum
# -----------------------------------------
# Fatures: Sexinsex 爬虫
# Author : qianyong
# Time   : 2017/7/8 16:57
# =========================================
#

import chardet
import datetime,time,os

from scrapy.spiders import Spider

class ForumSpider(Spider):
    name = 'forum_spider'

    start_urls = ['http://www.sexinsex.net/forum/index.php?gid=398']
    host = 'Hwww.sexinsex.net'
    def parse(self, response):
        print(response.body)

