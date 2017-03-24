from __future__ import print_function
import sys
from bottle import get, route, run, template
import os
import datetime

home = os.environ.get("HOME","/tmp")
csv_file = os.path.join(home, "visitcount.csv") 

import pymongo

MONGODB_URI=os.environ["MONGODB_URI"]
client = pymongo.MongoClient(MONGODB_URI)
db = client["khcc"]
collection = db["visitcount"]

header = ["_id", "created_on", "location", "address", "count"]

def sort_rows(data):
    return [[x["_id"], x["created_on"], x["location"], x["address"], x["count"]] for x in data]

def get_rows(from_date, to_date):
    data = collection.find({"created_on":{"$gte":from_date,"$lt":to_date}})
    rows = sort_rows(data)
    return rows

@get('/')
def index():
    all_dates_ = list(collection.find({},{"created_on":1}).distinct("created_on"))
    all_dates = [date(year=x.year, month=x.month, day=x.day) for x in all_dates_]
    all_dates = list(set(all_dates))
    all_dates_list = sorted([x.strftime("%Y-%m-%d") for x in all_dates])

    to_date = datetime.datetime(now.year, now.month, now.day)
    from_date = to_date - datetime.timedelta(days=1)
    rows = get_rows(from_date, to_date)

    return template('index',header=header,dates=all_dates_list,rows=rows)

now = datetime.datetime.now()
from datetime import date

@route('/table/<created_on:re:.*>')
def table(created_on):
    

    print("created_on: %s" % created_on, file=sys.stderr)

    if not created_on:
        from_date = to_date - datetime.timedelta(days=1)
        to_date = datetime.datetime(now.year, now.month, now.day)
    else:
        y,m,d = map(int,created_on.split("-"))
        from_date = datetime.datetime(y,m,d)
        to_date = from_date + datetime.timedelta(days=1)

    rows = get_rows(from_date, to_date)

    return template('table',header=header,rows=rows)


port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=True)
