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
from twisted.internet import reactor
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
    return template('index',message="csv_file is not available, click above button to fresh!")

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
    if os.path.isfile(csv_file):
        return get_csvtable()
    else:
        return "csv_file not available."

def run_spider():
    try:
        os.remove(csv_file)
    except OSError:
        pass

    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl(VisitcountSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

@route('/refresh')
def refresh():
    run_spider()
    return get_csvtable()

@route('/hello')
def hello():
    return "hello"


port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=True)
