from __future__ import print_function
from bottle import get, route, run, template

import logging

import tablib
import csv
import os

import scrapy
from scrapy import signals
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from khcc.spiders.visitcount import VisitcountSpider
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import Crawler

from pydispatch import dispatcher

import threading


home = os.environ.get("HOME","/tmp")
csv_file = os.path.join(home, "visitcount.csv") 

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


logger = logging.getLogger()

def get_csvtable():
    if os.path.isfile(csv_file):
        dataset = tablib.Dataset()
        with open(csv_file) as f:
            dataset.csv = f.read()

        return dataset.html
    else:
        return "csv_file not available, click above to refresh."


@get('/')
def index():
    return template('index')


@route('/view')
def view():
    return get_csvtable()


#crawler.signals.connect(reactor.stop, signal=signals.spider_closed)

def run_spider():
    #is_refreshing = True

    try:
        os.remove(csv_file)
    except OSError:
        pass

    #runner = CrawlerRunner(get_project_settings())
    #runner.crawl(VisitcountSpider)
    #d.addBoth(lambda _: reactor.stop())
    #reactor.run(installSignalHandlers=True)
    #dispatcher.connect(reactor.stop, signals.spider_closed)
    #process = CrawlerProcess(get_project_settings())
    #process.crawl('visitcount')
    #process.start(stop_after_crawl=True)
    #is_refreshing = False


    #    spider = VisitcountSpider()
    #    crawler = Crawler(spider, get_project_settings())
    #    dispatcher.connect(reactor.stop, signals.spider_closed)
    #
    #    crawler.crawl()
    #    reactor.run()
    #	

def spider_stop():
    logger.debug("spider_stop")
    reactor.callFromThread(reactor.stop)

@route('/stop')
def stop():
    #reactor.stop()
    reactor.run()
    
#d = crawler.crawl()
#d.addBoth(lambda _: reactor.callFromThread(reactor.stop))

@route('/refresh')
def refresh():
    try:
        os.remove(csv_file)
    except OSError:
        pass
	
    crawler = Crawler(VisitcountSpider)
    crawler.crawl()


#d.addBoth(lambda _: reactor.callFromThread(reactor.stop))
    #crawler.start()
    #process = CrawlerProcess(get_project_settings())
    #process.crawl('visitcount')
    #process.start(stop_after_crawl=True)
    #e = threading.Event()
    #t = threading.Thread(target=run_spider)
    #t.start()
    #return "refreshing..."
    #return get_csvtable()
    return ""


@route('/hello')
def hello():
    return "hello"


port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=True)
