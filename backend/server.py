from flask import Flask
from flask import jsonify, make_response
import csv
import pandas as pd
import json 
from flask_cors import CORS
from datetime import datetime
from mrtparse import *
import pandas as pd
import seaborn as sns
from collections import OrderedDict
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from helper import parse_aggregator, parse_as_path, parse_path_attributes, parse_bgp_message, parse_one_entry, getcolumns, parse_all_entries,get_graph_from_AS_path, getGraphintoPresentableScale
import json
from flask import jsonify
from bisect import bisect_left 
import random
from flask import request
import io
import csv
from flask import make_response
import pyexcel as pe

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    res = "hello"
    return res


def find(vertexID, attackervertexID):
    if attackervertexID == -1:
        attackervertexID = None
    with open('graph.json') as json_file:
        vertexlist = []
        data = json.load(json_file)
        for x in data:
            vertexlist.append(x)
        vertexlist = list(map(int, vertexlist))
        vertexlist = sorted(vertexlist)
        v = bisect_left(vertexlist, vertexID)
        
        localizedvertex = {}
        visited = {}
        
        def dfs(vertex, depth):
            maxdepths = random.randint(3,10)
            if depth > maxdepths:
                return 
            global numvertex
            if depth == 1:
                numvertex = 0
            if numvertex > 500:
                return
            x = str(vertex)
            if x in visited:
                return
            visited[x] = 1
            for u in data[x]:
                if u not in localizedvertex:
                    localizedvertex[u] = {}
                    numvertex = numvertex + 1
                if x not in localizedvertex:
                    localizedvertex[x] = {}
                    numvertex = numvertex + 1
                
                localizedvertex[u][x] = 1
                localizedvertex[x][u] = 1
                if numvertex > 500:
                    return
                dfs(u,depth+1) 
        dfs(vertexlist[v], 1)
        attacker = None
        if attackervertexID is not None:
            u = bisect_left(vertexlist, attackervertexID)
            dfs(vertexlist[u], 1)
            attacker = vertexlist[u]
        return (getGraphintoPresentableScale(localizedvertex, vertexlist[v], attacker))
        
@app.route('/graph', methods=['GET', 'POST']) 
def construct_graph():
    asn = request.args.get('asn')
    attackerasn = request.args.get('aasn')
    if asn is None:
        asn = 123
    if attackerasn is None:
        attackerasn = -1
    print(attackerasn)
    res = find(int(asn), int(attackerasn))
    return jsonify(res)

@app.route('/graph2', methods=['GET', 'POST'])
def getrequestdetail():
    asn = request.args.get('asn')
    print(asn)
    return "yes"

# def reading():
#     entries = []
#     for entry in Reader("updates.20180222.2330.bz2"):
#         entries.append(entry.data)
#     tmp = parse_path_attributes(entries[0]['bgp_message']['path_attributes'])
#     print(tmp)
#     dataframe = parse_all_entries(entries)
#     graphedges = get_graph_from_AS_path(dataframe[:20])
#     print(graphedges)
#     with open('graph.json', 'w') as fp:
#         json.dump(graphedges, fp)

@app.route('/degreedist', methods=['GET', 'POST']) 
def degreedistribution():
    degreedist = []
    with open('graph.json') as json_file:
        data = json.load(json_file)
        for x in data:
            degreedist.append(len(data[x]))
    data = [["date","close"]]
    u = max(degreedist)
    v = min(degreedist)
    mollifier = (u-v)//50
    result = { i : 0 for i in range(0,50)}
    for x in degreedist:
        for i in range(0, 50):
            if x >= i * mollifier + v and x < (i+1)*mollifier + v:
                result[i] = result[i] + 1
    for x in result:
        data.append([x, result[x]])        
    sheet = pe.Sheet(data)
    io2 = io.StringIO()
    sheet.save_to_memory("csv", io2)
    output = make_response(io2.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/withdrawndist', methods=['GET', 'POST']) 
def withdrawndistribution():
    degreedist = []
    with open('bgpwithdrawn.json') as json_file:
        data = json.load(json_file)
        for x in data:
            degreedist.append(x)
    data = [["date","close"]]
    u = 500
    v = min(degreedist)
    mollifier = (u-v)//50
    result = { i : 0 for i in range(0,50)}
    for x in degreedist:
        for i in range(0, 50):
            if x >= i * mollifier + v and x < (i+1)*mollifier + v and x > 0:
                result[i] = result[i] + 1
    for x in result:
        data.append([x, result[x]])        
    sheet = pe.Sheet(data)
    io2 = io.StringIO()
    sheet.save_to_memory("csv", io2)
    output = make_response(io2.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output   

@app.route('/asequence', methods=['GET', 'POST']) 
def asequencedistribution():
    degreedist = []
    with open('as_sequence.json') as json_file:
        data = json.load(json_file)
        for x in data:
            degreedist.append(x)
        
    data = [["date","close"]]
    
    u = max(degreedist)
    v = min(degreedist)
    mollifier = 1
    result = { i : 0 for i in range(0,10)}
    for x in degreedist:
        for i in range(0, 10):
            if x >= i * mollifier + v and x < (i+1)*mollifier + v and x > 0:
                result[i] = result[i] + 1
    for x in result:
        data.append([x, result[x]])        
    sheet = pe.Sheet(data)
    io2 = io.StringIO()
    sheet.save_to_memory("csv", io2)
    output = make_response(io2.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output     

@app.route('/aggregatemulti', methods=['GET', 'POST']) 
def aggregatemulti():
    degreedist = { "timestamp" : [], "close" : []}
    outputdata = [["date","close"]]
    resultx = {}
    with open('multiexit.json') as json_file:
        data = json.load(json_file)
        l = len(data["timestamp"])
        for i in range(0,l):
            x = (data["timestamp"][i][1]) 
            result = 0
            if str(data["value"][i]) == 'nan':
                result = 0
            else:
                result = (data["value"][i])
            if x in resultx:
                resultx[x] += result
            else:
                 resultx[x] = result
    for x in resultx:
        outputdata.append([x, resultx[x]])  
    sheet = pe.Sheet(outputdata)
    io2 = io.StringIO()
    sheet.save_to_memory("csv", io2)
    output = make_response(io2.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output    

if __name__ == "__main__":
    app.run(port=24561)