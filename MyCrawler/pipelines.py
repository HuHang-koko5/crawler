# -*- coding: utf-8 -*-
import pymongo
from pymongo.errors import DuplicateKeyError
from MyCrawler.items import editorialItem, dramaAddressItem, subtitleItem
from MyCrawler.settings import DB_NAME, LOCAL_MONGO_HOST, LOCAL_MONGO_PORT
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MycrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.db = client[DB_NAME]

    def process_item(self, item, spider):
        if isinstance(item, editorialItem):
            table_name = "EDITORIAL"
        if isinstance(item, dramaAddressItem):
            table_name = 'Servir_y_proteger_address'
        if isinstance(item, subtitleItem):
            table_name = item['title']
        col = self.db[table_name]
        self.insert_item(col, item)


    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            pass
