import scrapy #importing the scrapy framework
from ..items import FarfetchItem #importing the items.py

class FarfetchspiderSpider(scrapy.Spider):  # This method usually parses the response, extracting the scraped data as dicts and also finding new URLs
    name = 'farfetchspider' #Spider.
    allowed_domains = ['www.farfetch.com']

    # A List of urls where the spider will begin to crawl from.
    def start_requests(self):
        urls = [
            'https://www.farfetch.com/fr/shopping/men/shoes-2/items.aspx?page={}',
            'https://www.farfetch.com/fr/shopping/women/bags-purses-1/items.aspx?page={}']

        # Check the condition till 220 pages and increase the page_number by 1
        for url in urls:
            for i in range(1, 220):
                x = url.format(i)
                yield scrapy.Request(url=x, callback=self.parse)

    def parse(self, response, **kwargs):

        items = FarfetchItem()

        # A List of urls where the spider will begin to crawl from.
        product_name = response.css('div.css-hu5jv1-ProductCardInfoClamp.e1awqx90 > p.css-4y8w0i-Body.e1s5vycj0').css(
            '::text').extract() #text is availabe in <p class='_d85b45'> and extracting only text while inspecting
        product_brand = response.css(
            'p.e17j0z620::text').extract() #text is availabe in <h3 class='_346238'> and extracting only text while inspecting
        product_price = response.css('div.css-q58lfc-PriceBrief.erv2rus0').css(
            '::text').extract() #text is availabe in <div class='_6356bb'> and extracting only text while inspecting
        product_sale_price = response.css('css-hmsjre-Body-Price e15nyh750').css(
            '::text').extract() #text is availabe in <div class='_6356bb'> and extracting only text while inspecting
        product_image_url = response.css(
            'meta::attr(content)').extract() #Url is available in <img> and inspecting only 'content' attribute
        product_page_url = response.css(
            'a::attr(href)').extract() #Url is availabe in <a> and extracting only 'href' attribute

        # Using our items
        items['product_name'] = product_name
        items['product_brand'] = product_brand
        items['product_price'] = product_price
        items['product_sale_price'] = product_sale_price
        items['product_image_url'] = product_image_url
        items['product_page_url'] = product_page_url

        yield items #It's like return.

        #the mongodb localhost setting is edit in setting.py and pipelines.py
        #In settings.py the item pipline is configured.
        #In pipelines.py the local host, port, database name, collection name is created and a method to process_item.
        #so that the data is stored in mongodb database as gaurav(farfetch).
        #and a json file for data extracted is also created.
