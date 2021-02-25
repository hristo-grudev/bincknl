import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import BincknlItem
from itemloaders.processors import TakeFirst


class BincknlSpider(scrapy.Spider):
	name = 'bincknl'
	start_urls = ['https://www.binck.nl/kennis/blog']

	def parse(self, response):
		post_links = response.xpath('//div[@class="blog-li-wrapper"]/li/a[1]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="sf_pagerNumeric"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1//div[@class="sfTxtContent"]/text()').get()
		description = response.xpath('//div[@class="mc-article-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="mc-article-meta"]/p/text()').get()
		if date:
			date = date.split(',')
			date = [d.strip() for d in date[1:]]
			date = ' '.join(date).strip()
		print(date)

		item = ItemLoader(item=BincknlItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
