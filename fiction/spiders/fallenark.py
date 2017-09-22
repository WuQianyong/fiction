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
from selenium import webdriver

import re
import  redis
cookies = '__cfduid=d2f5d480c64e637b0bbf8451a146394ab1497344110; __utma=105352400.1222396991.1499842390.1499842390.1499842390.1; __utmz=105352400.1499842390.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); l7y0_2132_onlineindex=1; l7y0_2132_saltkey=BpzE0zg4; l7y0_2132_lastvisit=1504589238; l7y0_2132_auth=eaccgu2V3hf6EmDnwEm56dLpTlBtowpdBGQCxX%2F22MBiCALuZRjFzVH%2FlHmXuGvbsXx4QUk8vD983f%2FmUFTPg3l9jg; l7y0_2132_lastcheckfeed=13898%7C1504592866; l7y0_2132_smile=1D1; l7y0_2132_forum_lastvisit=D_95_1505368065D_4_1505368075; l7y0_2132_ulastactivity=c96ekmj%2F16VutB0Gqtf7r11DeHHMDUVB7U0rLFQcJOOxwq%2FeM6e8; l7y0_2132_lip=66.112.216.105%2C1505876606; l7y0_2132_onlineusernum=98; _gat=1; l7y0_2132_lastact=1505878292%09forum.php%09; l7y0_2132_sid=m0A9U9; _ga=GA1.2.1222396991.1499842390; _gid=GA1.2.709143668.1505876608'


def get_new_cookie(cookies):
    items = cookies.split(';')
    new_cookies = {}
    for item in items:
        the = item.split('=')
        new_cookies[the[0]] = the[1]
    return new_cookies


new_cook = get_new_cookie(cookies)


R = redis.Redis(host='localhost',port=6379,decode_responses=True)
url_key = 'fallenark:url:dict'


class FallenarkSpider(Spider):
    name = 'fallenark_spider'

    start_urls = ['http://bbs.fallenark.com/forum.php?mod=forumdisplay&fid=54&mobile=1',
                  'http://bbs.fallenark.com/forum.php?mod=forumdisplay&fid=138&mobile=1',
                  'http://bbs.fallenark.com/forum.php?mod=forumdisplay&fid=139&mobile=1',
                  'http://bbs.fallenark.com/forum.php?mod=forumdisplay&fid=134&mobile=1',
                  'http://bbs.fallenark.com/forum.php?mod=forumdisplay&fid=95&mobile=1',
                  'http://bbs.fallenark.com/forum.php?mod=forumdisplay&fid=135&mobile=1',
                  'http://bbs.fallenark.com/forum.php?mod=forumdisplay&fid=148&mobile=1']
    host = 'http://bbs.fallenark.com'

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
                post_url = ''.join([self.host, '/', post_url_tail])

                print('请求帖子内容')
                print(post_url)
                yield Request(post_url, cookies=new_cook, callback=self.parse_script)

        # 下一页链接
        next_url_list = response.xpath('//*/a[@class="nxt"]/@href').extract()
        if next_url_list:
            for next_url_tail in list(set(next_url_list)):
                next_url = ''.join([self.host, '/',next_url_tail])
                print('请求下一页')
                print(next_url)
                yield Request(next_url, cookies=new_cook, callback=self.parse)

    def parse_script(self, response):

        # print(response.url)
        # print(response.text)
        web_content = response.text
        a = re.findall('<script type="text/javascript">(.*?)</script>', web_content)
        flag = False
        # 开始重构 js 脚本
        if len(a) == 1:

            script = a[0]
            tail_compile_list = ['location=(.*?);_', 'location\..*?=(.*?);_', 'location\..*?(\(.*?);_',
                                 'location\[.*?\]([=\(].*?);_',
                                 ';location\..*?(\(.*?)\);_',
                                 ';location(.*?);_', ]
            head_compile_list = ['(.*?)location=.*?;_', '(.*?)location\..*?;_', '(.*?)location\..*?\(.*?;_',
                                 '(.*?)location\[.*?\].*?;_',
                                 '(.*?;)location.*?;_',
                                 '(.*?;)location.*?;_']
            for tail_compile_str, head_compile_str in zip(tail_compile_list, head_compile_list):
                tail_compile = re.compile(tail_compile_str)
                head_compile = re.compile(head_compile_str)
                console_script_list = re.findall(tail_compile, script)
                new_script_head = re.findall(head_compile, script)
                try:
                    if len(console_script_list) == 1 and len(new_script_head) == 1:

                        console_script = console_script_list[0]

                        new_script_list = [''.join([new_script_head[0], 'console.log(', console_script, ');']),
                                           ''.join([new_script_head[0], 'console.log(', console_script[1:], ';']),
                                           ''.join([new_script_head[0], 'console.log(', console_script, ';']),
                                           ''.join([new_script_head[0], 'console.log(', console_script[1:], ');']),
                                           ]
                        browser = webdriver.PhantomJS()
                        for new_script in new_script_list:
                            try:
                                browser.execute_script(new_script)
                                log_list = browser.get_log('browser')
                                for log in log_list:
                                    if log:
                                        url_tail = log['message'].replace('(:)', '').strip()
                                        print(url_tail)
                                        post_url = ''.join([self.host, url_tail])
                                        print(post_url)
                                        R.hset(url_key,response.url,post_url)
                                        flag = True
                                        break
                                        # yield Request(post_url, cookies=new_cook, callback=self.parse_post)

                                    else:
                                        print('re3')
                            except:
                                pass
                        browser.close()

                        # if console_script.startswith('.replace'):
                        #     console_script = console_script.replace('.replace', '')
                        #     new_script = ''.join([new_script_head[0], 'console.log(', console_script, ');'])
                        # elif console_script.startswith('='):
                        #     new_script = ''.join([new_script_head[0], 'console.log(', console_script[1:], ';'])
                        #
                        # else:
                        #     new_script = ''.join([new_script_head[0], 'console.log(', console_script, ');'])


                        # bs = browser.get_log('browser')


                        break
                except:
                    # print(web_content)
                    pass

        else:
            # console_script_list = re.findall(';location(.*?);_', script)
            # new_script_head = re.findall('(.*?;)location.*?;_', script)

            print('re2')

        if not flag:
            print(web_content)
            js_dir = os.path.join(os.path.abspath('.'), 'tmp_html')

            if not os.path.exists(js_dir):
                os.makedirs(js_dir)
            url = response.url
            filename = ''.join([re.findall('tid=(.*?)&', url)[0], '.html'])
            # if re.findall('tid=(.*?)&', url)[0]
            filepath = os.path.join(js_dir, filename)
            print(filepath)
            with open(filepath, 'w') as f:
                f.write(web_content)
                f.close()

            # if new_script:
            #
            #     browser = webdriver.PhantomJS()
            #     browser.execute_script(new_script)
            #     log_list = browser.get_log('browser')
            #     browser.close()
            #     for log in log_list:
            #         if log:
            #             url_tail = log['message'].replace('(:)', '').strip()
            #             print(url_tail)
            #             post_url = ''.join([self.host, url_tail])
            #             print(post_url)
            #             # yield Request(post_url, cookies=new_cook, callback=self.parse_post)
            #
            #         else:
            #             print('re3')
            # yield Request(post_url, cookies=new_cook, callback=self.parse_post)

