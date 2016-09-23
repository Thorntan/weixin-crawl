# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
import datetime
from weixin.items import WeixinItem
from MySQLdb import escape_string

class WeixinSpider(Spider):
    name = "weixin"
    allowed_domains = ["sougou.com"]
    # query=keyword, sourceid=message_publish_time(inttime_day,inttime_week,inttime_month,inttime_year) 
    url2tag = {
            "http://weixin.sogou.com/weixin?type=2&ie=utf8&query=PVC&soureceid=inttime_week":"weixin"
            }
    start_urls = url2tag.keys()

    def parse(self,response):
        """
        从搜索结果的首页得到前10页的链接
        """
        url_list = [ response.url ]
        #tag = self.url2tag[response.url]
        for page in response.xpath('//*[@id="pagebar_container"]/a')[:-1]:
            page_url = "http://weixin.sogou.com/weixin"+page.xpath('./@href').extract()[0]
            url_list.append(page_url)
        for url in url_list:
            yield Request(
                    url = url,
                    callback = self.parse_page,
                    dont_filter = True
                    )
            break

    def parse_page(self,response):
        """
        从每个搜索结果页得到文章的链接
        """
        for result in response.xpath('//div[@class="results"]/div'):
            url = result.xpath('./div[2]/h4/a/@href').extract()[0]
            title = result.xpath('string(./div[2]/h4/a)').extract_first(default="").strip()
            yield Request(
                url = url,
                meta = {
                    "tag":"weixin",
                    "source":"weixin"
                },
                callback = self.parse_content,
                dont_filter = True
            )
            break

    def parse_content(self, response):
        """
        解析文章
        """
        title = response.xpath('//*[@id="activity-name"]/text()').extract()[0].encode('utf-8').strip()
        pub_date = response.xpath('//*[@id="post-date"]/text()').extract()[0]
        html = response.xpath('//*[@id="js_content"]').extract()[0]
        content = response.xpath('string(//*[@id="js_content"])').extract_first(default="").strip()
        yield WeixinItem(
            title = title,
            tag = response.meta['tag'],
            url=response.url,
            source = response.meta['source'],
            pub_date = pub_date,
            content = content,
            html = escape_string(html),
            insert_date = datetime.datetime.today().strftime('%Y-%m-%d')
        )
