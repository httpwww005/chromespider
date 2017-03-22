from bottle import route, run
import os


from selenium import webdriver
webdriver.ChromeOptions.binary_location = "/app/.apt/usr/bin/google-chrome-stable"
driver = webdriver.Chrome()



@route('/')
def hello():
    driver.get("http://140.117.11.2")
    source = driver.page_source
    return source 


port = int(os.environ.get('PORT',5000))
run(host='0.0.0.0', port=port, debug=True)
