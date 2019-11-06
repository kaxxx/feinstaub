#!/usr/bin/python2.7 -u
# coding=utf-8
from flask import Flask, jsonify, json
from fsdb import Fsdb

app = Flask(__name__)

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

@app.route('/fs/api/v1.0/lastdays/<days>', methods=['GET'])
def get_tasks(days):
    db = Fsdb()
    return jsonify(db.getLastDays(days))
    #return json.dumps();

def get_data():
    return

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
