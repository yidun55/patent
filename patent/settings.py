# -*- coding: utf-8 -*-

# Scrapy settings for patent project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'patent1'

SPIDER_MODULES = ['patent.spiders']
NEWSPIDER_MODULE = 'patent.spiders'

DEFAULT_ITEM_CLASS = 'patent.items.PatentItem'
ITEM_PIPELINES=['patent.pipelines.PatentPipeline']
COOKIES_ENABLES=False
DNSCACHE_ENABLED = True
CONCURRENT_REQUESTS = 50
DOWNLOAD_TIMEOUT = 300
LOG_FILE = "/home/dyh/data/testScrapyd/log"

# Retry many times since proxies often fail
RETRY_TIMES = 10
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 405, 408]

#测试user_agent池
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 200,
        'patent.rotate_useragent.RotateUserAgentMiddleware' :400
    }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'patent (+http://www.yourdomain.com)'
