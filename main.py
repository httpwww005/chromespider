from bottle import route, run
import os

@route('/hello')
def hello():
    return "Hello World!"


port = os.environ['PORT']
run(host='0.0.0.0', port=port, debug=True)
