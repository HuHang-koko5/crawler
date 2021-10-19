import scrapy
import json
from MyCrawler.items import newsItem
from MyCrawler.settings import MONGO_HOST,MONGO_DB
import pymongo
import certifi


CA = certifi.where()
FEEDER = "https://www.elmundo.es/ue-nydus/nydus-feeder.php?option=direct&content="
urls = [
        'https://www.elmundo.es/economia.html',
        #'https://www.elmundo.es/internacional.html',
        'https://www.elmundo.es/deportes.html',
        'https://www.elmundo.es/cultura.html',
        'https://www.elmundo.es/television.html',
        'https://www.elmundo.es/ciencia-y-salud.html',
        'https://www.elmundo.es/tecnologia.html',
        ]
labels = [
    'economia',
    #'internacional',
    'deportes',
    'cultura',
    'television',
    'ciencia-y-salud',
    'tecnologia',
]


class elmundoCategorySpider(scrapy.Spider):
    name = "elcate"
    # allowed_domains = ['elmundo.es']
    client = pymongo.MongoClient(MONGO_HOST, tlsCAFile=CA)
    db = client[MONGO_DB]
    col = db['elmundo_News']

    def start_requests(self):
        for url, label in zip(urls, labels):
            request = scrapy.Request(url=url,
                                     callback=self.parse_index,
                                     dont_filter=False)
            request.cb_kwargs['label'] = label
            yield request

    def parse_index(self, response, label):
        blocks = response.xpath('//article')
        hrefs = blocks.xpath('//header/a/@href').getall()
        titles = blocks.xpath("//header/a/h2/text()").getall()
        for href, title in zip(hrefs, titles):
            """
                if label in href:
                item = newsItem()
                item['category'] = label
                item['title'] = title
                item['url'] = href
                yield item
            """
            if self.col.find_one({'title':title}) is None:
                # print("new url!")
                feeder_url = FEEDER + href[href.find(".es/")+4:].rstrip(".html")
                feeder_request = scrapy.Request(feeder_url,
                                                callback=self.feeder_check,
                                                dont_filter=False)
                feeder_request.cb_kwargs['label'] = label
                yield feeder_request

    def feeder_check(self, response, label):
        js = json.loads(response.text)
        content = js['content']
        for feed in content:
            if self.col.find_one({'title': feed['titulo']}) is None:
                print("url:{} \n title:{}".format(feed['url'], feed['titulo']))
                item = newsItem()
                item['category'] = label
                item['title'] = feed['titulo']
                item['url'] = feed['url']
                yield item
                feeder_url = FEEDER + feed['url'][feed['url'].find(".es/")+4:].rstrip(".html")
                feeder_request = scrapy.Request(feeder_url,
                                                callback=self.feeder_check,
                                                dont_filter=False)
                feeder_request.cb_kwargs['label'] = label
                yield feeder_request


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl elcate".split())