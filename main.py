from bottle import route, run
import os

@route('/')
def hello():
    return "Hello World!"


port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=True)
