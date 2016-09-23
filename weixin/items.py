# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html

from scrapy.item import Item,Field


class WeixinItem(Item):
    # define the fields for your item here like:
    title = Field()
    url = Field()
    content = Field()
    pub_date = Field()
    source = Field()
    html = Field()
    insert_date = Field()
    tag = Field()
