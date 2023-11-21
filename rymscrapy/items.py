# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RymChart(scrapy.Item):
    title = scrapy.Field()
    artists = scrapy.Field()
    year = scrapy.Field()
    genres = scrapy.Field()
    average_rating = scrapy.Field()
    pass
