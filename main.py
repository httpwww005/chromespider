from __future__ import print_function
import json
import sys
from bottle import get, route, run, template
import re
import datetime
from datetime import date
from bottle import response

import logging
logger = logging.getLogger()

import os
import pymongo
import gridfs
import pytz
from bson.codec_options import CodecOptions

TZ=pytz.timezone("Asia/Taipei")

MONGODB_URI=os.environ["MONGODB_URI"]
MONGODBCSV_URI=os.environ["MONGODBCSV_URI"]
client = pymongo.MongoClient(MONGODB_URI)
client_csv = pymongo.MongoClient(MONGODBCSV_URI)
db_csv = client_csv["csv"]
fs_db = gridfs.GridFS(db_csv)
collection_visitcount = client["khcc"]["visitcount"].with_options(codec_options=CodecOptions(tz_aware=True,tzinfo=TZ))

heroku_release = os.environ.get("HEROKU_RELEASE_VERSION","unknow")

header = ["created_on", "location", "address", "count", "images"]


def get_rows(from_date, to_date):
    pipeline = [
            {
                "$match":
                {
                    "created_on":
                    {
                        "$gte":from_date,
                        "$lt":to_date
                    }
                }
            },
            {
                "$group":
                {
                    "_id":"$address",
                    "address":{"$first":"$address"},
                    "count":{"$max":"$count"},
                    "location":{"$first":"$location"},
                    "created_on":{"$first":"$created_on"}
                }
            },
            {
                "$project":
                {
                    "_id":0,
                    "address":1,
                    "count":1,
                    "location":1,
                    "created_on":1
                }
            }]

    rows = []
    data = collection_visitcount.aggregate(pipeline)
    for d in data:
        address = re.match(r"^[^\d]+([\d-]*).*$",d["address"]).group(1) 
        img_url = "<a href=\"/images/%s\">%s</a>" % (address, address)
        rows.append([str(d["created_on"].date()), d["location"], d["address"], d["count"], img_url])

    return rows


@get('/')
def index():
    all_dates = list(collection_visitcount.distinct("created_on"))
    all_dates = sorted(set([str(x.date()) for x in all_dates]))
    return template('index',header=header,dates=all_dates,heroku_release=heroku_release,re_created_on=re_created_on)

re_created_on = "\d{4}-\d{2}-\d{2}"

@route('/table/<created_on:re:%s>' % re_created_on)
def table(created_on):
    from_date = datetime.datetime.strptime(created_on,'%Y-%m-%d').replace(tzinfo=TZ)
    #print(from_date, file=sys.stderr)
    to_date = from_date + datetime.timedelta(days=1)
    #print(to_date, file=sys.stderr)
    rows = get_rows(from_date, to_date)
    json_data = {"data":rows}

    return json.dumps(json_data)


@route('/csv/<created_on:re:%s>' % re_created_on)
def csv(created_on):
    filename = "%s.csv" % created_on
    fp = fs_db.get_last_version(filename)
    data = fp.read()
    response['Content-Type'] = "text/csv"
    response['Content-Disposition'] = 'inline; filename="%s"' % filename
    return data


@route('/images/<house_id:re:[\d-]+>')
def images(house_id):
    collection = client["khcc"]["imgur"]
    images = list(collection.find({"address":house_id}))[0]["images"]

    return template('images', images = images)

port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=False, reloader=True)
