from bottle import get, route, run, template

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
    #d = runner.crawl(VisitcountSpider)
    #d.addBoth(lambda _: reactor.stop())
    #reactor.run(installSignalHandlers=False)
    
    #dispatcher.connect(reactor.stop, signals.spider_closed)
    #process = CrawlerProcess(get_project_settings())
    #process.crawl('visitcount')
    #process.start(stop_after_crawl=False)
    #is_refreshing = False


    spider = VisitcountSpider()
    crawler = Crawler(spider, get_project_settings())
    dispatcher.connect(reactor.stop, signals.spider_closed)

    crawler.start()
    reactor.run()
	

@route('/refresh')
def refresh():
    e = threading.Event()
    t = threading.Thread(target=run_spider)
    t.start()

    return "refreshing..."
    #return get_csvtable()


@route('/hello')
def hello():
    return "hello"


port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=True)
