import scrapy
import pymongo
from MyCrawler.items import newsItem
from MyCrawler.settings import MONGO_HOST, MONGO_DB


class elmundoNewsSpider(scrapy.Spider):
    name = 'elmundo'
    allowed_domains = ['https://www.elmundo.es']

    def start_requests(self):
        client = pymongo.MongoClient(MONGO_HOST)
        db = client[MONGO_DB]
        col = client['News']
        for item in col.find():
            news_url = item['url']
            tag = item['label']
            request = scrapy.Request(url=news_url,
                                     callback=self.parse_article,
                                     dont_filter=True)
            request.cb_kwargs['label'] = tag
            yield request

    def parse_article(self, response, label):
        # get <article>
        item = newsItem()
        news = response.xpath("//article")
        """
            <header> include title, stand first(optional) </header>
            div: "//div[@class='ue-l-article-content']"
            title: h1/text()
            stand first(optional): p[@class='ue-c-article__standfirst']/text()
        """
        header = news.xpath("//div[@class='ue-l-article-content']")
        title = header.xpath("//h1/text()").get()
        stand_first = response.xpath("//p[@class='ue-c-article__standfirst']/text()").getall()
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

