'''
Author: Logic
Date: 2022-04-27 11:12:58
LastEditTime: 2022-04-28 13:17:43
FilePath: \pyFuncs\web_run.py
Description: 
'''

from testGraph import graph
from graph.beans import Graph, Node, Edge, Info
import json
from flask import Flask, g, request
from flask_cors import CORS
import myFunc.basic.signFunc
app = Flask(__name__)

CORS(app, supports_credentials=True)


@app.route('/graph', methods=['GET', 'POST'])
def graphShow():
    return json.dumps(graph.toDict(), ensure_ascii=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1235)
