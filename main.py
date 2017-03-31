from __future__ import print_function
import json
import sys
from bottle import get, route, run, template
import os
import datetime
from datetime import date
import pytz
from bottle import response
import gridfs

import logging
logger = logging.getLogger()

heroku_release = os.environ.get("HEROKU_RELEASE_VERSION","unknow")

import pymongo

MONGODB_URI=os.environ["MONGODB_URI"]
MONGODBCSV_URI=os.environ["MONGODBCSV_URI"]
client = pymongo.MongoClient(MONGODB_URI)
client_csv = pymongo.MongoClient(MONGODBCSV_URI)
db = client["khcc"]
db_csv = client_csv["csv"]
fs_db = gridfs.GridFS(db_csv)
collection = db["visitcount"]

header = ["created_on", "location", "address", "count"]

TZ=pytz.timezone("Asia/Taipei")

def get_rows(from_date, to_date):
    data = collection.find({"created_on":{"$gte":from_date,"$lt":to_date}})
    rows = [[str(x["created_on"])[0:10], x["location"], x["address"], x["count"]] for x in data]
    return rows


@get('/')
def index():
    all_dates = list(collection.find({},{"created_on":1}).distinct("created_on"))
    all_dates = sorted([str(x.date()) for x in all_dates])
    return template('index',header=header,dates=all_dates,heroku_release=heroku_release,re_created_on=re_created_on)

re_created_on = "\d{4}-\d{2}-\d{2}"

@route('/table/<created_on:re:%s>' % re_created_on)
def table(created_on):
    from_date = datetime.datetime.strptime(created_on,'%Y-%m-%d')
    to_date = from_date + datetime.timedelta(days=1)
    rows = get_rows(from_date, to_date)
    json_data = {"data":rows}

    return json.dumps(json_data)


@route('/csv/<created_on:re:%s>' % re_created_on)
def csv(created_on):
    filename = "%s.csv" % created_on
    fp = fs_db.get_last_version(filename)
    data = fp.read()
    response.content_type = "text/csv"
    return data


port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=False, reloader=True)
