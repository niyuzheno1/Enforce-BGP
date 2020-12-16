from mrtparse import *
import pandas as pd
import seaborn as sns
from collections import OrderedDict
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import networkx as nx
from collections import deque
import random
import sys
import argparse
from bgputilities.parser import parse_aggregator, getcolumns, parse_one_entry
import json


def main():
    entries = []
    s = ".20180119.1515"
    for entry in Reader("updates{}.bz2".format(s)):
        entries.append(entry.data)
    hashtable =getcolumns(entries)
    for i in range(len(entries)):
        u = parse_one_entry(entries[i])
        for key in hashtable:
            if key in u:
                hashtable[key].append(u[key])
            else:
                hashtable[key].append(None)
    dataframe = pd.DataFrame(hashtable)
    dataframe.to_csv('data{}.csv'.format(s))
    bgp_message_withdrawn_routes_length = []
    for x in dataframe.iloc:
        bgp_message_withdrawn_routes_length.append(int(x['bgp_message_withdrawn_routes_length']))
    with open('bgpwithdrawn{}.json'.format(s), 'w') as fp:
        json.dump( bgp_message_withdrawn_routes_length, fp)
    multiexit = {"timestamp" : [],"value" : []}
    for x in dataframe.iloc:
        multiexit["timestamp"].append(x["timestamp"])
        multiexit["value"].append(x["MULTI_EXIT_DISC_value"])
    with open('multiexit{}.json'.format(s), 'w') as fp:
        json.dump( multiexit, fp)
    as_sequence = []
    for x in dataframe.iloc:
        if (x['AS_PATH_AS_SEQUENCE']) is None:
            as_sequence.append(0)
        else:
            as_sequence.append(int(len(x['AS_PATH_AS_SEQUENCE'])))
    with open('as_sequence{}.json'.format(s), 'w') as fp:
        json.dump( as_sequence, fp)
graphedge = {}
for x in dataframe3['AS_PATH_AS_SEQUENCE']:
  if x is None:
    continue
  for i in range(len(x)-1):
    u = x[i]
    v = x[i+1]
    if u not in graphedge:
      graphedge[u] = {}
    if v not in graphedge:
      graphedge[v] = {}
    graphedge[u][v] = graphedge[v][u]= 1

    G = nx.Graph()
    for x in graphedge:
        G.add_node(int(x))

    for x in graphedge:
        for y in graphedge[x]:
            if x == y:
                continue
            G.add_edge(int(x),int(y))

    pos = nx.kamada_kawai_layout(G)



    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')



    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    with open('graph{}.json'.format(s), 'w') as fp:
            json.dump(graphedge, fp)
    
if __name__ == "__main__":
    main()

