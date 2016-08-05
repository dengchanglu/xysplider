import scrapy
class DemoItems(scrapy.item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()