from bottle import route, run

@route('/hello')
def hello():
    return "Hello World!"

run(host='localhost', debug=True)
