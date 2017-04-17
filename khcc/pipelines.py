# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#from scrapy.pipelines.images import ImagesPipeline
import os
from imgurpython import ImgurClient
import time
import scrapy
import logging

logger = logging.getLogger(__name__)


class ImgurPipeline(object):
    def __init__(self):
        imgur_id = os.environ.get('IMGUR_ID', "")
        imgur_secret = os.environ.get('IMGUR_SECRET', "")
        imgur_refresh_token = os.environ.get('IMGUR_REFRESH_TOKEN', "")
        #mashape_key = os.environ.get('IMGUR_MASHAPE_KEY', "")
        self.imgur_delay = 70 # upload limit, 1 hour 50 images, 60/50=1.2
        self.imgur_client = ImgurClient(
                imgur_id, 
                imgur_secret, 
                refresh_token=imgur_refresh_token)
                #mashape_key=mashape_key)


    def open_spider(self, spider):
        self.imgur_album = spider.imgur_album
        logger.debug('imgur_album: %s' % self.imgur_album)


    def process_item(self, item, spider):
        imgur_urls = []
        for i in range(0, len(item['image_urls'])):
            url = item['image_urls'][i]
	    config = {
		'album': self.imgur_album,
		'name':  "%s.%d" % (item['address'], i),
		'title': "%s %s" % (item['location'], item['address']),
		'description': url
	    }

            image = self.imgur_client.upload_from_url(url=url, config=config, anon=False)
            if(image):
                logger.debug('image: %s' % image)
                imgur_urls.append(image["link"])
                logger.debug('sleep for %d secodes..' % self.imgur_delay)
                try:
                    time.sleep(self.imgur_delay)
                except:
                    spider.close_down = True # not work

        item["imgur_urls"] = imgur_urls

        return item
