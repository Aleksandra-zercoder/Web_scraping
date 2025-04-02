import scrapy


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        products = response.css('div[data-testid="product-card"]')

        for product in products:
            name = product.css('div.lsooF span[itemprop="name"]::text').get()
            price = product.css('div.pY3d2 span[data-testid="price"]::text').get()
            url = product.css('div.lsooF a::attr(href)').get()

            yield {
                "name": name.strip() if name else None,
                "price": price.strip() if price else None,
                "url": response.urljoin(url) if url else None
            }

