# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from fiction.items import FallenarkTid, FallenarkTitle
from sqlalchemy import *
from plugins.connect_db import _conn
from plugins.get_md5 import get_md5
import logging


CONNECT_MYSQL = {
    "host": "127.0.0.1:3306",
    "user": "yong",
    "pwd": "19950105",
    "db": "wqy",
    "charset": "utf8"
}

TABLE_LIST = ['t_fallenark_title', 't_fallenark_article']


class FictionPipeline(object):
    def process_item(self, item, spider):
        if self.session and self.base:
            title = self.base.classes[TABLE_LIST[0]]
            article = self.base.classes[TABLE_LIST[1]]
            if isinstance(item, FallenarkTitle):
                logging.info('1---------------------')
                result = self.session.query(title.id).filter(title.title == item.get('title'),
                                                             title.tid == item.get('tid'))
                result_list = list(result)
                if result_list.__len__() > 0:

                    if result_list.__len__() > 1:
                        logging.warning('fallenark title 数据 {} {}  有 {} 条记录'.format(item.get('title'),
                                                                                    item.get('tid'),

                                                                                    len(result_list))
                                        )
                    else:
                        logging.info('fallenark title 数据 {} {}  有 {} 条记录'.format(item.get('title'),
                                                                                 item.get('tid'),

                                                                                 len(result_list))
                                     )
                    for id_item in result_list:
                        id = id_item[0]
                        onerecord = title(id=id,
                                          title=item.get('title'),
                                          tid=item.get('tid'),
                                          category=item.get('category'),
                                          updated=func.now())
                        try:
                            self.session.merge(onerecord)
                            self.session.commit()
                            logging.info('数据更新成功： id: {}   {}    '.format(id, item))
                        except Exception as e:
                            if 'Duplicate' in str(e):
                                logging.info(
                                    '存储数据 id：{}  {} 失败,原因是 数据库已存在该数据 '.format(id, item))
                            else:
                                logging.error('存储数据 原因：{}      {}       数据：{}'.format(e, id, item))
                            self.session.rollback()
                else:
                    onerecord = title(title=item.get('title'),
                                      tid=item.get('tid'),
                                      category=item.get('category'),
                                      updated=func.now())
                    try:
                        self.session.add(onerecord)
                        self.session.commit()
                        logging.info('数据添加成功：   {}    '.format(item))
                    except Exception as e:
                        if 'Duplicate' in str(e):
                            logging.info(
                                '存储数据    {} 失败,原因是 数据库已存在该数据 '.format(item))
                        else:
                            logging.error('存储数据 原因：{}        数据：{}'.format(e, item))
                        self.session.rollback()


                        # print(item)
            elif isinstance(item, FallenarkTid):
                t_md5 = get_md5(item.get('content'))
                logging.info('content md5 : {}'.format(t_md5))
                result = self.session.query(article.id).filter(article.uid == item.get('uid'),
                                                               article.tid == item.get('tid'),
                                                               article.t_md5 == t_md5,
                                                               article.floor == item.get('floor'))
                result_list = list(result)
                if result_list.__len__() > 0:

                    if result_list.__len__() > 1:
                        logging.warning('fallenark article 数据 {} {}  有 {} 条记录'.format(item.get('content'),
                                                                                      item.get('tid'),

                                                                                      len(result_list))
                                        )
                    else:
                        logging.info('fallenark article 数据 {} {}  有 {} 条记录'.format(item.get('content'),
                                                                                   item.get('tid'),

                                                                                   len(result_list))
                                     )
                    for id_item in result_list:
                        id = id_item[0]
                        onerecord = article(id=id,
                                            content=item.get('content'),
                                            tid=item.get('tid'),
                                            name=item.get('name'),
                                            uid=item.get('uid'),
                                            t_time=item.get('t_time'),
                                            page=item.get('page'),
                                            floor=item.get('floor'),
                                            t_md5=t_md5,
                                            updated=func.now())
                        try:
                            self.session.merge(onerecord)
                            self.session.commit()
                            logging.info('数据更新成功： id: {}   {}    '.format(id, item))
                        except Exception as e:
                            if 'Duplicate' in str(e):
                                logging.info(
                                    '存储数据 id：{}  {} 失败,原因是 数据库已存在该数据 '.format(id, item))
                            else:
                                logging.error('存储数据 原因：{}      {}       数据：{}'.format(e, id, item))
                            self.session.rollback()
                else:
                    onerecord = article(content=item.get('content'),
                                        tid=item.get('tid'),
                                        name=item.get('name'),
                                        uid=item.get('uid'),
                                        t_time=item.get('t_time'),
                                        page=item.get('page'),
                                        floor=item.get('floor'),
                                        t_md5=t_md5,
                                        updated=func.now())
                    try:
                        self.session.add(onerecord)
                        self.session.commit()
                        logging.info('数据添加成功：   {}    '.format(item))
                    except Exception as e:
                        if 'Duplicate' in str(e):
                            logging.info(
                                '存储数据    {} 失败,原因是 数据库已存在该数据 '.format(item))
                        else:
                            logging.error('存储数据 原因：{}        数据：{}'.format(e, item))
                        self.session.rollback()

                logging.info('2------------------')
                # print(item)
        return item

    def open_spider(self, spider):
        try:
            logging.info('打开管道')
            self.session, self.base = _conn(CONNECT_MYSQL, TABLE_LIST)

            logging.info('连接 MySQL  hsh_fx 成功，参数为：{}'.format(CONNECT_MYSQL))
        except Exception as e:
            logging.critical('连接 MySQL 失败')
            self.session, self.base = None, None
