from bottle import route, run

@route('/hello')
def hello():
    return "Hello World!"

run(host='localhost', port=80, debug=True)
