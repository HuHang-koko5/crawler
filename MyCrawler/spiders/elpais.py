import scrapy
from MyCrawler.items import editorialItem


class elpaisOpinionEditorialesSpider(scrapy.Spider):
    name = 'elpais'

    def start_requests(self):
        init_url = "https://elpais.com/noticias/europa/"
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        article_url = response.xpath('//*[@id="middle_section"]/div/div/article/div[2]/h2/a//@href').getall()
        article_url += response.xpath('//*[@id="bottom_section"]/div/article/h2/a//@href').getall()
        print(article_url)
        for a_url in article_url[0:4]:
            article = "https://elpais.com" + a_url
            yield scrapy.Request(url=article, callback=self.articleParser)

    def articleParser(self, response):
        item = editorialItem()
        title = response.xpath('//*[@id="article_header"]/h1/text()').get()
        author = response.xpath('//*[@id="fusion-app"]/article/header/div[3]/div[1]/span/a/text()').get()
        time = response.xpath('//*[@id="fusion-app"]/article/header/div[3]/div[2]/div/a/text()').get()
        time_zone = response.xpath('//*[@id="fusion-app"]/article/header/div[3]/div[2]/div/a/abbr/text()').get()
        print("title:", title)
        print("author :", author)
        print(time, ' ', time_zone)
        content_list = response.xpath('//*[@id="fusion-app"]/article/div[1]/div[1]/p/text()').getall()
        content = ""
        for i in content_list:
            content += i
            content += '\n'
        print("content:")
        print(content)
        item['title'] = title
        item['author'] = author
        item['time'] = time
        item['time_zone'] = time_zone
        item['content'] = content
        yield item




