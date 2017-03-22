from bottle import route, run
import tablib
import os

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

dataset = tablib.Dataset()

@route('/run')
def go():
    import os
    home = os.environ.get("HOME","/tmp")                 
    csv = os.path.join(home, "visitcount.csv") 

    try:
        os.remove(csv)
    except OSError:
	pass

    process = CrawlerProcess(get_project_settings())
    process.crawl('visitcount')

    process.start(stop_after_crawl=False) # the script will block here until the crawling is finished
    
    # process csv

    with open(csv) as f:
	dataset.csv = f.read()

    return dataset.html

@route('/view')
def view():
    return dataset.html

port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=True)
