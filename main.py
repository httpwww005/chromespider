import threading

from bottle import get, route, run, template
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

import tablib
import csv
import os

import scrapy
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pydispatch import dispatcher
from twisted.internet import reactor
#from billiard import Process
from khcc.spiders.visitcount import VisitcountSpider
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner

home = os.environ.get("HOME","/tmp")                 
csv_file = os.path.join(home, "visitcount.csv") 


configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

def get_csvtable():
    dataset = tablib.Dataset()
    with open(csv_file) as f:
    	dataset.csv = f.read()

    return dataset.html



@get('/')
def index():
    return template('index', message="gg")

@get('/websocket', apply=[websocket])
def echo(ws):
    while True:
        msg = ws.receive()
        msg = get_csvtable()
        if msg is not None:
            ws.send(msg)
        else: 
	    break



@route('/view')
def view():
    return get_csvtable()


def run_spider(e):
    try:
        os.remove(csv_file)
    except OSError:
        pass

    #runner = CrawlerRunner(get_project_settings())
    #d = runner.crawl(VisitcountSpider)
    #d.addBoth(lambda _: reactor.stop())
    #reactor.run()

    process = CrawlerProcess(get_project_settings())
    process.crawl('visitcount')
    process.start(stop_after_crawl=False)


@route('/go')
def go():
    e = threading.Event()
    t = threading.Thread(target=run_spider, args=(e,))
    t.start()
    return "processing"

port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=True, server=GeventWebSocketServer)
