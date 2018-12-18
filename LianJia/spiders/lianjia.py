# -*- coding: utf-8 -*-
import json

from scrapy.http import Request
from urllib import parse
import scrapy

from LianJia.items import DownloadImageItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'

    api_url = 'https://app.api.lianjia.com/Rentplat/v1/house/list?city_id={city_id}&limit=100&offset={offset}'

    def start_requests(self):
        yield Request(self.api_url.format(city_id=110000, offset=100), callback=self.parse, dont_filter=True)

    def parse(self, response):

        resp_data = json.loads(response.body)['data']
        total = resp_data['total']

        for i in range(1, int(total/100)):
            yield Request(url=self.api_url.format(city_id=110000, offset=i*100), callback=self.parse_list,
                          dont_filter=True)

    def parse_list(self, response):
        resp_data = json.loads(response.body)['data']
        house_list = resp_data['list']

        if house_list:
            for house in house_list:
                house_code = house['house_code']
                yield Request(url=parse.urljoin(response.url, "detail?house_code=%s" % house_code),
                              callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):

        image_url_items = DownloadImageItem()

        resp_data = json.loads(response.body)['data']
        house_picrures = resp_data['house_picture']

        for house_picrure in house_picrures:
            image_url = house_picrure.get('house_picture_url')
            image_name = house_picrure.get('picture_name')

            image_url_items['image_URL'] = [image_url + ".780x439.jpg"]
            image_url_items['image_CATEGORY'] = image_name

            yield image_url_items

