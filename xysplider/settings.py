# Scrapy settings for xysplider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'xysplider'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['xysplider.spiders']
NEWSPIDER_MODULE = 'xysplider.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

