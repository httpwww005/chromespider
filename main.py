from bottle import route, run
import os

@route('/hello')
def hello():
    return "Hello World!"


port = os.environ['PORT']
run(host='localhost', port=port, debug=True)
