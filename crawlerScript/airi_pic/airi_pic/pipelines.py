# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request

class AiriPicPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['airi_image_url']:
        	yield Request(image_url)

    def item_completed(self, results, item, info):
    	image_paths = [x['path'] for ok, x in results if ok]
    	if not image_paths:
    		raise DropItem('The image has not download! %s' % image_paths)
