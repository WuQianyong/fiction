#!/usr/bin/env Python3
# -*- coding: utf-8 -*-
# 
# =========================================
# launch
# -----------------------------------------
# Fatures: fiction 爬虫的启动程序
# Author : qianyong
# Time   : 2017/7/8 16:53
# =========================================
#




from scrapy.utils.project import get_project_settings
from datetime import datetime
from scrapy.crawler import CrawlerProcess

from fiction.spiders import ForumSpider,FallenarkSpider

def run():
    process = CrawlerProcess()
    process.settings = get_project_settings()
    # process.crawl(ForumSpider)  # 论坛爬虫
    process.crawl(FallenarkSpider)  # fallenark爬虫
    process.start()


if __name__ == '__main__':

    run()
    print('下载完成:%s' % datetime.now())
