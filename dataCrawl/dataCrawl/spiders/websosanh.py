import scrapy

class Websosanh(scrapy.Spider):
    name = "websosanh"
    start_urls = [
        "https://websosanh.vn/dien-thoai-may-tinh-bang/cat-85.htm",
        "https://websosanh.vn/dien-lanh/cat-1867.htm",
        "https://websosanh.vn/thoi-trang-my-pham/cat-3.htm",
        "https://websosanh.vn/may-anh-may-quay-phim/cat-13.htm",
        "https://websosanh.vn/sach/cat-216.htm"
    ]

    def parse(self, response):
        product_links = response.css('ul.list-no-style.row li.product-item.row-col a::attr(href)').extract()
        for product_link in product_links:
            yield scrapy.Request(response.urljoin(product_link), callback=self.parse2)

        next_page = response.css('div.pagination-wrap ul.pagination li a.next::attr(href)').extract_first()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page))

    def parse2(self, response):

        store_names = response.css('div.compare-result div.compare-item span.compare-store-name::text').extract()
        prices = response.css('div.compare-result div.compare-item div.compare-product-wrap div.compare-money::text').extract()
        price_comparision = dict(zip(store_names, prices))

        data_product = {
            'product name:' : response.css('h1.page-title::text').extract_first(),
            'price comparision:' :  price_comparision
        }
        yield data_product