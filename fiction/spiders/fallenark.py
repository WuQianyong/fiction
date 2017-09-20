#!/usr/bin/env Python3
# -*- coding: utf-8 -*-
# 
# Name   : fallenark
# Fatures:
# Author : qianyong
# Time   : 2017/9/20 11:38
# Version: V0.0.1
#
import chardet
import datetime, time, os
from scrapy.http import Request
from scrapy.spiders import Spider

cookies = '__cfduid=d2f5d480c64e637b0bbf8451a146394ab1497344110; __utma=105352400.1222396991.1499842390.1499842390.1499842390.1; __utmz=105352400.1499842390.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); l7y0_2132_onlineindex=1; l7y0_2132_saltkey=BpzE0zg4; l7y0_2132_lastvisit=1504589238; l7y0_2132_auth=eaccgu2V3hf6EmDnwEm56dLpTlBtowpdBGQCxX%2F22MBiCALuZRjFzVH%2FlHmXuGvbsXx4QUk8vD983f%2FmUFTPg3l9jg; l7y0_2132_lastcheckfeed=13898%7C1504592866; l7y0_2132_smile=1D1; l7y0_2132_forum_lastvisit=D_95_1505368065D_4_1505368075; l7y0_2132_ulastactivity=c96ekmj%2F16VutB0Gqtf7r11DeHHMDUVB7U0rLFQcJOOxwq%2FeM6e8; l7y0_2132_lip=66.112.216.105%2C1505876606; l7y0_2132_onlineusernum=98; _gat=1; l7y0_2132_lastact=1505878292%09forum.php%09; l7y0_2132_sid=m0A9U9; _ga=GA1.2.1222396991.1499842390; _gid=GA1.2.709143668.1505876608'


def get_new_cookie(cookies):
    items = cookies.split(';')
    new_cookies = {}
    for item in items:
        the = item.split('=')
        new_cookies[the[0]] = the[1]
    return new_cookies


new_cook = get_new_cookie(cookies)


class FallenarkSpider(Spider):
    name = 'fallenark_spider'

    start_urls = ['http://bbs.fallenark.com/forum.php?mod=forumdisplay&fid=4&page=1&mobile=1']
    host = 'http://bbs.fallenark.com/'

    def start_requests(self):


        for url in self.start_urls:
            yield Request(url, cookies=new_cook, callback=self.parse)

    def parse(self, response):
        print(response.text[:200])

        # 获取 帖子 连接
        post_url_list = response.xpath('//*/div[contains(@class,"bm_c")]/a/@href').extract()

        print(post_url_list)
        for post_url_tail in post_url_list:
            if 'mod=forumdisplay' in post_url_tail:
                pass
            elif 'mod=viewthread' in post_url_tail:
                post_url = ''.join([self.host, post_url_tail])
                print(post_url)
                print('请求帖子内容')
                yield Request(post_url, cookies=new_cook, callback=self.parse_post)

                # # 下一页链接
                # next_url_list = response.xpath('//*/a[@class="nxt"]/@href').extract()
                # if next_url_list:
                #     for next_url_tail in list(set(next_url_list)):
                #         next_url = ''.join([self.host, next_url_tail])
                #         print('请求下一页')
                #         yield Request(next_url, cookies=self.new_cook, callback=self.parse)

    def parse_post(self, response):

        print(response.url)
        print(response.text)
        from scrapy.shell import inspect_response
        inspect_response(response, self)
