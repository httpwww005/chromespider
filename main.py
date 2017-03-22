from bottle import route, run
import os

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


@route('/run')
def hello():
    process = CrawlerProcess(get_project_settings())
    process.crawl('visitcount')
    process.start() # the script will block here until the crawling is finished
    return "running"


port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=True)
