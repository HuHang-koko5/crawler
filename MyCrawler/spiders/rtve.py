import scrapy
from MyCrawler.items import dramaAddressItem


class rtveDramaAddressSpider(scrapy.Spider):
    name = 'DramaAddress'

    def start_requests(self):
        html_url = 'https://www.rtve.es/alacarta/interno/contenttable.shtml?pbq={page}&order=3&orderCriteria=ASC&modl=TOC&locale=es&pageSize=15&ctx=106710&typeFilter=39816'
        for p in range(1, 42):
            url = html_url.format(page=str(p))
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ul = response.xpath('//*/div[@class="ContentTabla"]/ul')
        lis = ul.xpath('li[@class="odd"]|li[@class="even"]')
        titles = lis.xpath('span[@class="col_tit"]/a/text()').getall()
        durations = lis.xpath('span[@class="col_dur"]/text()').getall()
        hrefs = lis.xpath('span[@class="col_tit"]/a/@href').getall()
        for title, dur, href in zip(titles, durations, hrefs):
            ep = dramaAddressItem()
            ep['title'] = title
            ep['duration'] = dur
            ep['href'] = href
            yield ep


if __name__ == '__main__':
    from scrapy import cmdline
    cmdline.execute("scrapy crawl DramaAddress".split())







