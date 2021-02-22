import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bankslm.items import Article


class BankSpider(scrapy.Spider):
    name = 'bank'
    start_urls = ['https://www.bankslm.ch/aktuelles-veranstaltungen/']

    def parse(self, response):
        links = response.xpath('//a[@class="card-link flood"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

        next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1//text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//div[@class="columns small-12 medium-6"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
