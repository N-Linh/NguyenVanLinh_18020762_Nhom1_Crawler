import scrapy
import json
from datetime import datetime

output_file = 'output/dantri/dantri_{}.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))

class Dantri(scrapy.Spider):
    name = "dantri"
    start_urls = [
            "https://dantri.com.vn/xa-hoi.htm",
            "https://dantri.com.vn/the-gioi.htm",
            "https://dantri.com.vn/the-thao.htm",
            "https://dantri.com.vn/van-hoa.htm",
            "https://dantri.com.vn/giai-tri.htm",
        #   "https://dantri.com.vn/giao-duc-khuyen-hoc.htm",
        #   "https://dantri.com.vn/du-lich.htm",
        #   "https://dantri.com.vn/phap-luat.htm",
        #   "https://dantri.com.vn/nhip-song-tre.htm",
        #   "https://dantri.com.vn/suc-manh-so.htm"
       ]


    def parse(self, response):
        articles = response.css('div.clearfix ul.dt-list.dt-list--lg li a.news-item__avatar::attr(href)').extract()
        for article in articles:
            if article is not None:
                yield scrapy.Request(response.urljoin(article), callback=self.parse2)

        next_page = response.xpath('//ul[@class="list-unstyled dt-category-actions"]/li/a/@href')[-1].extract()
        if next_page is not None and "101" not in str(next_page):#100 page limit each article
            yield scrapy.Request(response.urljoin(next_page))

    def parse2(self, response):
        data = {
            'Title: ': response.css('h1.dt-news__title::text').extract_first().strip(),
            'Category' : response.css('div.dt-news__header ul.dt-breadcrumb li a::text')[-1].extract(),
            'Publish time' : response.css('div.dt-news__header div.dt-news__meta span.dt-news__time::text').extract(),
            'Content' : '\n'.join(response.css('div.dt-news__body div.dt-news__content p::text').extract()),
            'Tags' : response.css('ul.dt-news__tag-list li a::text').extract()
        }
        #yield data
        with open(output_file, 'a', encoding='utf8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
            f.write('\n')



