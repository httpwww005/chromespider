from __future__ import print_function
import json
import sys
from bottle import get, route, run, template
import os
import datetime
from datetime import date

import logging
logger = logging.getLogger()

home = os.environ.get("HOME","/tmp")
csv_file = os.path.join(home, "visitcount.csv") 
heroku_release = os.environ.get("HEROKU_RELEASE_VERSION","unknow")

import pymongo

MONGODB_URI=os.environ["MONGODB_URI"]
client = pymongo.MongoClient(MONGODB_URI)
db = client["khcc"]
collection = db["visitcount"]

header = ["created_on", "location", "address", "count"]


def get_rows(from_date, to_date):
    data = collection.find({"created_on":{"$gte":from_date,"$lt":to_date}})
    rows = [[str(x["created_on"])[0:10], x["location"], x["address"], x["count"]] for x in data]
    return rows




@get('/')
def index():
    all_dates_ = list(collection.find({},{"created_on":1}).distinct("created_on"))
    all_dates = [date(year=x.year, month=x.month, day=x.day) for x in all_dates_]
    all_dates = list(set(all_dates))
    all_dates_list = sorted([x.strftime("%Y-%m-%d") for x in all_dates])
    print(heroku_release, file=sys.stderr)
    return template('index',header=header,dates=all_dates_list,heroku_release=heroku_release)


@route('/table/<created_on:re:\d{4}-\d{2}-\d{2}>')
def table(created_on):
    y,m,d = map(int,created_on.split("-"))
    from_date = datetime.datetime(y,m,d)
    to_date = from_date + datetime.timedelta(days=1)
    rows = get_rows(from_date, to_date)
    json_data = {"data":rows}
    return json.dumps(json_data)

port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=True)
