import scrapy
import re

class PetlebiSpider(scrapy.Spider):
    name = 'petlebi'
    allowed_domains = ['petlebi.com']

    def start_requests(self):
        categories = [
            'kedi-petshop-urunleri',
            'kopek-petshop-urunleri',
            'kus-petshop-urunleri',
            'kemirgen-petshop-urunleri'
        ]

        for category in categories:
            url = f'https://www.petlebi.com/{category}?page=1'  # Start from page 1
            yield scrapy.Request(url, callback=self.parse, meta={'category': category, 'page': 1})
            
    # Parse page
    def parse(self, response):
        category = response.meta.get('category')
        page = response.meta.get('page')

        # Parse product links from the current page
        product_links = response.css('div.card a.p-link::attr(href)').extract()
        for link in product_links:
            yield scrapy.Request(url=link, callback=self.parse_product, meta={'category': category})

        # Check for next page and send request if available
        next_page_link = response.css('ul.pagination li.page-item a.page-link[rel="next"]::attr(href)').get()
        if next_page_link:
            next_page_number = int(re.search(r'page=(\d+)', next_page_link).group(1))
            yield scrapy.Request(url=next_page_link, callback=self.parse, meta={'category': category, 'page': next_page_number})

    # Parse product
    def parse_product(self, response):
        category = response.meta.get('category')
        # Add all product
        product = {
            'product_url': response.url,
            'product_name': response.css('h1.product-h1::text').get().strip() if response.css('h1.product-h1::text').get() else None,
            'product_barcode': response.xpath('//div[contains(text(), "BARKOD")]/following-sibling::div/text()').get().strip() if response.xpath('//div[contains(text(), "BARKOD")]/following-sibling::div/text()').get() else None,
            'product_price': (response.css('p.mb-0 span.price::text').get() or '').strip() or (response.css('p.mb-0 span.commerce-discounts::text').get() or '').strip(),
            'product_stock': response.xpath('//script[contains(text(), "isInStock")]/text()').re_first(r'"isInStock":"(\w+)"'),
            'product_images': response.css('div.MagicScroll a.thumb-link::attr(href)').extract(),
            'description': response.xpath('//meta[@name="description"]/@content').get().strip(),
            'product_id': int(re.search(r'"productID":(\d+)', response.xpath('//script[contains(text(), "window.dataLayer")]/text()').get()).group(1)),
            'brand': re.search(r'"productBrand":"([^"]+)"', response.xpath('//script[contains(text(), "window.dataLayer")]/text()').get()).group(1),
            'category': re.search(r'"productCategory":"([^"]+)"', response.xpath('//script[contains(text(), "window.dataLayer")]/text()').get()).group(1),
            'sku': response.xpath('//div[contains(text(), "BARKOD")]/following-sibling::div/text()').get().strip() if response.xpath('//div[contains(text(), "BARKOD")]/following-sibling::div/text()').get() else None  # Assuming SKU is the same as barcode
        }

        yield product
