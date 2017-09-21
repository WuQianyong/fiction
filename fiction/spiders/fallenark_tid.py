#!/usr/bin/env Python3
# -*- coding: utf-8 -*-
# 
# Name   : fallenark_tid
# Fatures:
# Author : qianyong
# Time   : 2017/9/21 16:42
# Version: V0.0.1
#

"""
fallenark 爬虫
"""

# import redis
from fiction.spiders.fallenark import new_cook, R, url_key
from  scrapy.spiders import Spider
from scrapy.http import Request
import re
# R = redis.Redis(host='127.0.0.1',port=6379,db=0,decode_responses=True)
# url_key = 'fallenark:url:dict'
# print(R.hgetall(url_key))
a = R.hgetall(url_key)['http://bbs.fallenark.com/forum.php?mod=viewthread&tid=12608&mobile=1']
print(a)


class FallnarkTidSpider(Spider):
    name = 'fallnark_til_spider'

    start_urls = [a]
    host = 'http://bbs.fallenark.com'

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies=new_cook, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        content_list = response.xpath('//div[@class="pbody"]')
        new_content_list = [x.xpath('string(.)').extract() for x in content_list ]
        print(new_content_list)
        time_list = response.xpath('//div[@class="bm_user"]/em/font/text()').extract()
        uid_list =[re.findall('uid=(.*?)&m',x)[0] for x in response.xpath('//div[@class="bm_user"]/a[1]/@href').extract()]
        name_list = response.xpath('//div[@class="bm_user"]/a[1]/text()').extract()
        max_len = min(len(time_list),len(new_content_list),len(uid_list),len(name_list))
        print(len(time_list),len(new_content_list),len(uid_list),len(name_list))
        # if len(new_content_list) == max_len:
        tid = int(re.findall('tid=(.*?)&', response.url))
        for i,x in enumerate( zip(new_content_list,time_list,name_list,uid_list)):
            page = int(re.findall('page=(\d*)&',response.url))

            print(page,i,tid)
            content, time, name, uid = x
            print(i,content,time,name,uid)
        # main_content = ''.join(new_content_list[:(-1*max_len-1)])
        # print(main_content)
        # print(new_content_list[(-1*max_len-1):])
        # print(new_content_list[(-1*max_len-1):].__len__())
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)


