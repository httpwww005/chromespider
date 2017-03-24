from bottle import get, route, run, template
import os

home = os.environ.get("HOME","/tmp")
csv_file = os.path.join(home, "visitcount.csv") 

import pymongo

MONGODB_URI=os.environ["MONGODB_URI"]
client = pymongo.MongoClient(MONGODB_URI)
db = client["khcc"]
collection = db["visitcount"]


@get('/')
def index():
    return template('index')


@route('/table')
def table():
    data = list(collection.find())
    header = list(data[0].viewkeys())
    rows = [list(x.viewvalues()) for x in data]
    return template('table',header=header,rows=rows)


port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=True)
