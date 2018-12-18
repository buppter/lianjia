# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy

from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline


class DownLoadImagePipeline(ImagesPipeline):
    image_store = get_project_settings().get("IMAGE_STORE")

    def get_media_requests(self, item, info):
        image_url_list = item["image_URL"]
        for image_url in image_url_list:
            yield scrapy.Request(image_url, meta={"category": item["image_CATEGORY"]})

    def file_path(self, request, response=None, info=None):
        image_path = request.meta['category']
        image_guid = request.url.split('/')[-1]
        path = '%s/%s' % (image_path, image_guid)
        return path
