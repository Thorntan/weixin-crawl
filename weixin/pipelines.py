# -*- coding: utf-8 -*-
from scrapy import signals, log
from datetime import datetime
import MySQLdb
import MySQLdb.cursors
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeixinPipeline(object):

    def __init__(self,dbargs):
        self.conn = MySQLdb.connect(**dbargs)
        self.cursor = self.conn.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        """
        从settings.py读取MySQL的配置
        """
        dbargs = dict(
            host=crawler.settings['MYSQL_HOST'],
            port=crawler.settings['MYSQL_PORT'],
            db=crawler.settings['MYSQL_DB'],
            user=crawler.settings['MYSQL_USER'],
            passwd=crawler.settings['MYSQL_PWD'],
            charset='utf8',
            use_unicode= True,
        )
        return cls(dbargs)

    def process_item(self, item, spider):
        '''
        Insert item into MYSQL
        '''
        '''
        tb_name = 'metal_news'
        keys = ['pub_date', 'title', 'url', 'content', 'html', 'source', 'insert_date', 'tag']
        insert_temp = u'INSERT INTO %s (%s) VALUES (%s)' %(tb_name, ','.join(keys), ','.join(['"{%s}"' %k for k in keys]))
        #print MySQLdb.escape_string( item['html'] )
        #sql = insert_temp.format( item['pub_date'],item['title'], item['url'], MySQLdb.escape_string(item['content']), MySQLdb.escape_string(item['html']), item['source'], item['insert_date'], item['tag'] )
        sql = insert_temp.format(**item)
        try:
            self.cursor.execute(sql)
            # 得到这条news的id
            news_id = self.cursor.lastrowid

            # 查询tag是否存在
            tag = item['tag']
            sql = "select id from metal_tags where tag = '%s'"%tag
            self.cursor.execute(sql)
            temp_data = self.cursor.fetchall()
            # 取tag对应的id, 如果不存在这个tag,则新插入一个tag
            if len(temp_data) == 0:
                sql = "insert into metal_tags(tag) VALUE ('%s')"%tag
                self.cursor.execute(sql)
                tag_id = self.cursor.lastrowid
            else:
                tag_id = temp_data[0][0]

            # 将news和tag的关系写入表
            sql = "insert into metal_tag_news(metal_news_id, metal_tag_id) VALUE (%s, %s)"%(news_id, tag_id)
            self.cursor.execute(sql)

            self.conn.commit()
        except MySQLdb.IntegrityError, e:
            log.msg(e, level=log.WARNING)
        except Exception,e:
            log.msg(e, level=log.ERROR)
            log.msg(sql, level=log.ERROR)
        '''
        return item

    def __del__(self):
        self.cursor.close()
        self.conn.close()
