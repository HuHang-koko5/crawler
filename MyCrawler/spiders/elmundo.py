import scrapy
from MyCrawler.items import newsItem
urls = [
        'https://www.elmundo.es/economia.html',
        'https://www.elmundo.es/internacional.html',
        'https://www.elmundo.es/deportes.html',
        'https://www.elmundo.es/cultura.html',
        'https://www.elmundo.es/television.html',
        'https://www.elmundo.es/ciencia-y-salud.html',
        'https://www.elmundo.es/tecnologia.html',
        ]
labels = [
    'economia',
    'internacional',
    'deportes',
    'cultura',
    'television',
    'ciencia-y-salud',
    'tecnologia',
]


class elmundoCategorySpider(scrapy.Spider):
    name = "elcate"
    allowed_domains = ['https://www.elmundo.es']

    def start_requests(self):
        for url, label in zip(urls,labels):
            request = scrapy.Request(url=url,
                                     callback=self.parse_index,
                                     dont_filter=True)
            request.cb_kwargs['label'] = label
            yield request

    def parse_index(self, response, label):
        blocks = response.xpath('//article')
        hrefs = blocks.xpath('//header/a/@href').getall()
        titles = blocks.xpath("//header/a/h2/text()").getall()
        print("collected: href:{} titles:{}".format(len(hrefs), len(titles)))
        count = 0
        for href, title in zip(hrefs, titles):
            if label in href:
                item = newsItem()
                item['category'] = label
                item['title'] = title
                item['url'] = href
                count += 1
                print(item)
                yield item
        print("{} - {} crawled".format(label, count))


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl elcate".split())