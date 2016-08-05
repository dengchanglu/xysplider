# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class XyspliderItem(Item):
    url = Field()
    title = Field()
    size = Field()
    referer = Field()
    newcookies = Field()
    body = Field()

