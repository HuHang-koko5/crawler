import scrapy

urls = ['https://www.elmundo.es/espana.html',
        'https://www.elmundo.es/opinion.html',
        'https://www.elmundo.es/economia.html',
        'https://www.elmundo.es/internacional.html',
        'https://www.elmundo.es/deportes.html',
        'https://www.elmundo.es/cultura.html',
        'https://www.elmundo.es/television.html',
        'https://www.elmundo.es/ciencia-y-salud.html',
        'https://www.elmundo.es/tecnologia.html',
        'https://www.elmundo.es/loc.html']

class elmundoCategorySpider(scrapy.Spider):
    name = "el_cate"

    def start_requests(self):
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        pass
