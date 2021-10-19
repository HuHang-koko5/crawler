import scrapy
import pymongo
from MyCrawler.items import newsContentItem
from MyCrawler.settings import MONGO_HOST, MONGO_DB
import certifi
ca = certifi.where()

class elmundoNewsSpider(scrapy.Spider):
    name = 'elmundo'
    allowed_domains = ['www.elmundo.es']

    def start_requests(self):
        client = pymongo.MongoClient(MONGO_HOST, tlsCAFile=ca)
        db = client[MONGO_DB]
        col = db['elmundo_News']
        for item in col.find():
            news_url = item['url']
            tag = item['category']
            print('url:{}\ntag:{}'.format(news_url, tag))
            request = scrapy.Request(url=news_url,
                                     callback=self.parse_article,
                                     dont_filter=True)
            request.cb_kwargs['label'] = tag
            yield request

    def parse_article(self, response, label):
        # get <article>
        item = newsContentItem()
        news = response.xpath("//article")
        """
            <header> include title, stand first(optional) </header>
            div: "//div[@class='ue-l-article__header-content']"
            title: h1/text()
            stand first(optional): p[@class='ue-c-article__standfirst']/text()
        """
        header = news.xpath("//div[@class='ue-l-article__header-content']")
        title = header.xpath("//h1/text()").get()
        stand_first = response.xpath("//p[@class='ue-c-article__standfirst']/text()").getall()
        stand_first = "".join(stand_first)
        """
            content, need to exclude premium script
            div: div[@class='ue-l-article__body ue-c-article__body']
            paragraph(s): p[1]//text()
                for free articles:
                    extract first paragraph
                for premium articles:
                    extract snapshot(incomplete fist paragraph)
        """
        content = news.xpath("div[@class='ue-l-article__body ue-c-article__body']")
        content = content.xpath("p[1]//text()").getall()
        content = "".join(content)
        item['category'] = label
        item['title'] = title
        item['stand_first'] = stand_first
        item['content'] = content
        yield item

