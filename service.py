#!/usr/bin/python2.7 -u
# coding=utf-8

from flask import Flask, jsonify, json, render_template
from fsdb import Fsdb

app = Flask(__name__, template_folder='./templates', static_folder='./static')

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/lastdays/<days>")
def lastdays(days):
    return render_template("index.html", days=days)

@app.route('/fs/api/v1.0/lastdays/<days>', methods=['GET'])
def get_tasks(days):
    db = Fsdb()
    return jsonify(db.getLastDays(days))
    #return json.dumps(db.getLastDays(days));

def get_data():
    return

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
