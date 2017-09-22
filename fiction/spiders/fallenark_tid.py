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
import os
from fiction.items import FallenarkTitle, FallenarkTid
import logging
# from
# R = redis.Redis(host='127.0.0.1',port=6379,db=0,decode_responses=True)
# url_key = 'fallenark:url:dict'
# print(R.hgetall(url_key))
# a = R.hgetall(url_key)['http://bbs.fallenark.com/forum.php?mod=viewthread&tid=12608&mobile=1']
# print(a)
# import re
# for x in a.items():
#     if '/forum.php' not in x[1]:
#         print(x[0], x[1])
#         new_url_list = x[1].split('_dsign')
#         if len(new_url_list) >1:
#             new_url =''.join([x[0],'&_dsign',new_url_list[-1]])
#             R.hset(url_key,x[0],new_url)
#             # print(x[0],''.join([x[0],'&_dsign',new_url_list[-1]])

# 所有队列
all_key = 'fallenark:url:all'

# 准备队列
prepare_key = 'fallenark:url:prepare'

# 成功队列
success_key = 'fallenark:url:success'
# 失败队列
fail_key = 'fallenark:url:fail'


class FallnarkTidSpider(Spider):
    name = 'fallnark_til_spider'

    # start_urls = [a]
    host = 'http://bbs.fallenark.com'

    def start_requests(self):
        flag = True
        while flag:
            try:
                url = R.spop(prepare_key)
                if url:
                    tid = re.findall('tid=(.*?)&', url)[0]
                    js_dir = os.path.join(os.path.abspath('.'), 'html', tid)
                    if (not os.path.exists(js_dir)) or len(os.listdir(js_dir)) == 0:

                        yield Request(url, cookies=new_cook, callback=self.parse)
                    else:
                        print('{}  已抓取文件'.format(url))
                else:
                    flag =False

                logging.info('------start')
                a = R.sadd(success_key, url)
                logging.info('添加到成功 {} {}'.format(url, a))

            except Exception as e:
                logging.warning(e)
                logging.info('------start')
                a = R.sadd(fail_key, url)
                logging.info('添加到失败 {} {}'.format(url, a))


        # for url in self.start_urls:
        #     tid = re.findall('tid=(.*?)&', url)[0]
        #     js_dir = os.path.join(os.path.abspath('.'), 'html', tid)
        #     if (not os.path.exists(js_dir)) or  len(os.listdir(js_dir))==0:
        #
        #
        #         yield Request(url, cookies=new_cook, callback=self.parse)
        #     else:
        #         print('{}  已抓取文件'.format(url))

    def parse(self, response):
        try:
            fall_title = FallenarkTitle()
            fall_tid = FallenarkTid()

            # print(response.text)
            # from scrapy.shell import inspect_response
            # inspect_response(response, self)
            content_list = response.xpath('//div[@class="pbody"]')
            new_content_list = [x.xpath('string(.)').extract() for x in content_list]
            # print(new_content_list)
            time_list = response.xpath('//div[@class="bm_user"]/em/font/text()').extract()
            uid_list = [re.findall('uid=(.*?)&m', x)[0] for x in
                        response.xpath('//div[@class="bm_user"]/a[1]/@href').extract()]
            name_list = response.xpath('//div[@class="bm_user"]/a[1]/text()').extract()
            # max_len = min(len(time_list), len(new_content_list), len(uid_list), len(name_list))
            print(len(time_list), len(new_content_list), len(uid_list), len(name_list))
            # if len(new_content_list) == max_len:
            tid = re.findall('tid=(.*?)&', response.url)[0]
            print(re.findall('page=(.*?)&', response.url))
            page_list = re.findall('page=(.*?)&', response.url)
            if page_list:
                page = int(page_list[0])
            else:
                page = 1

            category_list = response.xpath('//*/div[@class="bm_h"]/a[1]/text()').extract()
            if category_list:
                category = category_list[0]
            else:
                category = ''

            title = response.xpath('//*[@id="thread_subject"]/text()').extract()[0]

            js_dir = os.path.join(os.path.abspath('.'), 'html', tid)
            if not os.path.exists(js_dir):
                os.makedirs(js_dir)
            filename = ''.join([str(page).zfill(3), '.html'])
            filepath = os.path.join(js_dir, filename)
            print(filepath)
            with open(filepath, 'wb') as f:
                f.write(response.body)
                f.close()
            fall_title['tid'] = tid
            fall_title['title'] = title
            fall_title['category'] = category
            yield fall_title

            # 设置文本
            txt_dir = os.path.join(os.path.abspath('.'), 'text')
            if not os.path.exists(txt_dir):
                os.makedirs(txt_dir)

            format_title = title.replace(r'\'','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','')
            txt_name = ''.join([format_title, '.txt'])
            txtpath = os.path.join(txt_dir, txt_name)
            print(txtpath)



            for i, x in enumerate(zip(new_content_list, time_list, name_list, uid_list)):
                # print(page, i, tid)
                content, time, name, uid = x
                # print(i, content, time, name, uid)
                floor = (page - 1) * 20 + i + 1
                if isinstance(content,list):
                    content=''.join(content)

                fall_tid['tid'] = tid
                fall_tid['page'] = page
                fall_tid['t_time'] = time
                fall_tid['uid'] = uid
                fall_tid['content'] = content.strip()
                fall_tid['name'] = name
                fall_tid['floor'] = floor

                txt_content = '{} {} {} \n{}\n'.format(floor,name,time,content).encode()
                with open(txtpath, 'ab') as f:
                    f.write(txt_content)
                    f.close()
                logging.info('写入内容成功')
                yield fall_tid
            if '_dsign' in response.url:
                a = R.sadd(success_key, response.url)
                logging.info('添加到成功 {} {}'.format(response.url,a))

            # 下一页

            next_url_list = response.xpath('//*/a[@class="nxt"]/@href').extract()
            if next_url_list:
                for next_url_tail in list(set(next_url_list)):
                    next_url = ''.join([self.host, '/', next_url_tail])
                    logging.info('请求下一页  :  {}'.format(next_url))
                    # (next_url)
                    yield Request(next_url, cookies=new_cook, callback=self.parse)
        except Exception as e:
            logging.warning(e)
            if '_dsign' in response.url:
                a = R.sadd(fail_key, response.url)
                logging.info('添加到失败 {} {}'.format(response.url,a))

            # b = R.sadd(all_key,response)


