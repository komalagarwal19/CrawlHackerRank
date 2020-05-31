# -*- coding: utf-8 -*-
from scrapy.selector import Selector
import scrapy


class HackernewsSpider(scrapy.Spider):
    name = 'hackernews'
    allowed_domains = ['news.ycombinator.com']
    start_urls = ['https://news.ycombinator.com/news?p=1']

    def parse(self, response):
        """
        Parses the hackernews to extract
        title, url, points and user for each posts
        """
        selector = Selector(response)
        items = selector.xpath('//tr[@class="athing"]')
        details = selector.xpath('//tr/td[@class="subtext"]')
        for item, detail in zip(items, details):
            title = item.xpath('td[@class="title"]/a/text()').extract()[0]
            url = item.xpath('td[@class="title"]/a/@href').extract()[0]
            try:
                points = detail.xpath(
                    'span[@class="score"]/text()').extract()[0]
                user = detail.xpath('a[@class="hnuser"]/text()').extract()[0]
            except:
                points = user = None
            yield {
                "title": title,
                "url": url,
                "points": points,
                "user": user
            }
        next_link = selector.xpath('//a[@class="morelink"]/@href').extract()
        if len(next_link) != 0:
            next_link = next_link[0]
            idx = next_link.split("=")[-1]
            print("Crawling page id : ", idx)
            if(int(idx) < 10):
                next_link = response.urljoin(next_link)
                yield scrapy.Request(next_link, callback=self.parse)
