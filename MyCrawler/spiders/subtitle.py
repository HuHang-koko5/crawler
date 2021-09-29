import scrapy
from MyCrawler.items import subtitleItem
import pymongo
import re


class rtveDramaAddressSpider(scrapy.Spider):
    name = 'subtitle'

    def start_requests(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['rtve']
        col = db['Servir_y_proteger_address']
        urls = []
        for i in col.find().sort('title', pymongo.DESCENDING):
            print(i['title'])
            if 'Capítulo' in i['title']:
                urls.append(str(i['href']))
        print(len(urls))
        input("continue")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = subtitleItem()
        title = response.xpath('//*[@id="wrapper"]/div[3]/div[3]/div/h2/span/text()').get()
        y = response.xpath('//*[@id="wrapper"]')
        yy = y.xpath('//*/div[@class="textRel"]')
        yyy = yy.xpath('div[1]')
        yyyy = yyy.xpath('p')
        for part in yyyy:
            timestamp = part.xpath('@data-config').get()
            if part.xpath('*').get():
                part = part.xpath('*')
            content = part.xpath('text()').get()
            content = re.sub(r'\n', '', content)
            content = re.sub(r'\t', '', content)
            print("--------item--------")
            # print("title:", title)
            print("time:", timestamp)
            # print("content:", content)
            item['title'] = title
            item['timeline'] = timestamp
            item['content'] = content
            yield item



