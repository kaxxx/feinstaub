#!/usr/bin/python2.7 -u
# coding=utf-8

from flask import Flask, jsonify, json, render_template
from fsdb import Fsdb
from datetime import datetime, timedelta
from gevent.pywsgi import WSGIServer

app = Flask(__name__, template_folder='./templates', static_folder='./static')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aqi.json")
def aqidata():
    try:
        out = json.load(open('aqi.json'))
    except IOError as error:
        out = error

    return jsonify(out)

@app.route("/aqi.html")
def api():
    return render_template("aqi.html")

@app.route("/plotly/<days>")
def plotly(days):
    return render_template("plotly.html", days=days)

@app.route("/plotly/range/<sfrom>/<sto>")
def rangePl(sfrom, sto):
    return render_template("plotly.html", sfrom=sfrom, sto=sto)

@app.route("/plotly/range/<sfrom>")
def rangePlfrom(sfrom):
    return render_template("plotly.html", sfrom=sfrom)


@app.route("/lastdays/<days>")
def lastdays(days):
    return render_template("index.html", days=days)

@app.route("/range/<sfrom>/<sto>")
def range(sfrom, sto):
    return render_template("range.html", sfrom=sfrom, sto=sto)

@app.route('/fs/api/v1.0/aqi/data/last/days/<days>', methods=['GET'])
def get_aqi24(days):
    dfrom = datetime.now() - timedelta(days=int(days))
    dto = datetime.now()
    db = Fsdb()
    return jsonify(db.getRange(dfrom,dto))


@app.route('/fs/api/v1.0/range/<sfrom>/<sto>', methods=['GET'])
def get_range(sfrom, sto):
    dfrom = datetime.strptime(sfrom, "%Y-%m-%d %H:%M:%S")
    dto = datetime.strptime(sto, "%Y-%m-%d %H:%M:%S")
    db = Fsdb()
    return jsonify(db.getRange(dfrom,dto))

@app.route('/fs/api/v1.0/pl/range/<sfrom>/<sto>', methods=['GET'])
def get_rangePl(sfrom, sto):
    dfrom = datetime.strptime(sfrom, "%Y-%m-%d %H:%M:%S")
    dto = datetime.strptime(sto, "%Y-%m-%d %H:%M:%S")
    db = Fsdb()
    return jsonify(db.getRangePL(dfrom,dto))

@app.route('/fs/api/v1.0/pl/range/<sfrom>', methods=['GET'])
def get_rangeFromPl(sfrom):
    dfrom = datetime.strptime(sfrom, "%Y-%m-%d %H:%M:%S")
    dto = sto = datetime.now() #datetime.strptime(sto, "%Y-%m-%d %H:%M:%S")
    db = Fsdb()
    return jsonify(db.getRangePL(dfrom,dto))

@app.route('/fs/api/v1.0/lastdays/<days>', methods=['GET'])
def get_lastdays(days):
    db = Fsdb()
    return jsonify(db.getLastDays(days))

@app.route('/fs/api/v1.0/pl/lastdays/<days>', methods=['GET'])
def get_lastdaysPl(days):
    db = Fsdb()
    return jsonify(db.getLastDaysPl(days))

def get_data():
    return

if __name__ == '__main__':
    #app.run(debug=True, threaded=True, host= '0.0.0.0')
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()

