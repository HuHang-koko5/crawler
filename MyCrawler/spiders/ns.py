import scrapy

class kensetuSpider(scrapy.Spider):
    name = 'kensetu'

    def start_requests(self):
        init_url = 'https://etsuran.mlit.go.jp/TAKKEN/kensetuKensaku.do'
        yield scrapy.Request(url=init_url,callback=self.parse)

    def parse(self, response, **kwargs):
        print(response)