from flask import Flask, render_template, redirect, url_for, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time

app = Flask(__name__)

option = Options()
option.headless = False
driver = webdriver.chrome(option=option)
driver.implicitly_wait(5)
url = ''
driver.get(url)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        url = request.form['search']
        driver.get(url)

    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
