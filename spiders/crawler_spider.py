from scrapy import Spider
from scrapy.selector import Selector
from crawler.items import CrawlerItem
import re


class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["https://stackoverflow.com"]
    start_urls = [
        "https://stackoverflow.com/questions/tagged/python",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@id="questions"]/div')
        print(questions)

        def stringformat(str):

            str = re.sub("\\r\\n\s+", "", str)

            str = re.sub("\\n", "", str)

            str = re.sub("\"", "\"", str)

            return str
        for question in questions:
            item = CrawlerItem()
            item['id'] = question.attrib['id'][17:]
            item['title'] = question.xpath(
                'div[@class="s-post-summary--content"]/h3[@class="s-post-summary--content-title"]/a/text()').extract_first()
            item['content'] = stringformat(question.xpath(
                'div[@class="s-post-summary--content"]/div[@class="s-post-summary--content-excerpt"]/text()').extract_first())
            item['vote'] = question.xpath(
                'div[@class="s-post-summary--stats js-post-summary-stats"]/div[@class="s-post-summary--stats-item s-post-summary--stats-item__emphasized"]/span/text()').extract_first()
            item['answer'] = question.xpath(
                'div[@class="s-post-summary--stats js-post-summary-stats"]/div[2]/span/text()').extract_first()
            item['view'] = question.xpath(
                'div[@class="s-post-summary--stats js-post-summary-stats"]/div[3]/span/text()').extract_first()

            yield item
