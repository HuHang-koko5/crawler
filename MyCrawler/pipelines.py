# -*- coding: utf-8 -*-
import pymongo
import logging
import certifi
from pymongo.errors import DuplicateKeyError
from MyCrawler.items import editorialItem, dramaAddressItem, subtitleItem, newsItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

ca = certifi.where()


class MycrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self, mongo_host, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # pull in information from settings.py
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def process_item(self, item, spider):
        if isinstance(item, editorialItem):
            table_name = "EDITORIAL"
        if isinstance(item, dramaAddressItem):
            table_name = 'Servir_y_proteger_address'
        if isinstance(item, subtitleItem):
            table_name = item['title']
        if isinstance(item, newsItem):
            table_name = 'News'
        col = self.db[table_name]
        logging.debug("Post added to MongoDB")
        self.insert_item(col, item)
        return item


    def open_spider(self, spider):
        # initializing spider
        # opening db connection
        self.client = pymongo.MongoClient(self.mongo_host, tlsCAFile=ca)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # clean up when spider is closed
        self.client.close()

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            pass
