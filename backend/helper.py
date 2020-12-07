import pandas as pd
def parse_aggregator(aggregator):
  ret = {}
  for key in aggregator:
    ret["aggregator" + "_" + key] = aggregator[key]
  return ret
def parse_as_path(as_path):
  ret = {}
  for x in as_path:
    types = x['type']
    ret['AS_PATH_' + types[1]] = x['value']
  return ret

def parse_path_attributes(path_attributes):
  ret = {}
  for pa in path_attributes:
    x = pa['type'][1]
    ret[x + '_flag'] = pa['flag']
    if x == 'AGGREGATOR':
      ret1 = parse_aggregator(pa['value'])
      for key in ret1:
        ret[key] = ret1[key]
    elif x == 'AS_PATH':
      ret1 = parse_as_path(pa['value'])
      for key in ret1:
        ret[key] = ret1[key]
    else:
      ret[x + '_value'] = pa['value']
  return ret

def parse_bgp_message(entry):
  ret = {}
  for x in entry['bgp_message']:
    if x == 'type':
      ret['bgp_message_type'] = entry['bgp_message'][x][1]
    elif x == 'path_attributes':
      ret1 = parse_path_attributes(entry['bgp_message'][x])
      for x in ret1:
        ret[x] = ret1[x]
    elif x == 'nlri':
      for z in entry['bgp_message'][x]:
        for y in z:
          ret['bgp_message_nlri_' + y] = z[y]
    else:
      ret['bgp_message_{}'.format(x)] = entry['bgp_message'][x]
  return ret

def parse_one_entry(entry):
  ret = {}
  tmp = entry
  for x in tmp:
    if x == 'bgp_message':
      ret1 = parse_bgp_message(tmp)
      for y in ret1:
        ret[y] = ret1[y]
    else:
      ret[x] = tmp[x]
  return ret

def getcolumns(entries):
  columns = {}
  for i in range(0,7000):
    u = parse_one_entry(entries[i])
    for k in u:
      columns[k] = []
  return columns

def parse_all_entries(entries):
    hashtable =getcolumns(entries)
    for i in range(len(entries)):
        u = parse_one_entry(entries[i])
        for key in hashtable:
            if key in u:
                hashtable[key].append(u[key])
            else:
                hashtable[key].append(None)
    dataframe = pd.DataFrame(hashtable)
    return dataframe
def get_graph_from_AS_path(dataframe):
    graphedge = {}
    for x in dataframe['AS_PATH_AS_SEQUENCE']:
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
    return graphedge

def getalledges(edges):
  ret = {}
  for u in edges:
    for v in edges[u]:
      if (u,v) in ret or (v,u) in ret:
        continue
      ret[(u,v)] = 1
  return ret

def newnode(x, y, z):
  ret = {"id" : "node_"+x }
  ret["group"] = 2 if str(x) == str(y) else 1 
  ret["group"] = 3 if str(x) == str(z) else ret["group"]
  return ret

def newedge(x, y):
  return {"source" : "node_"+x, "target": "node_"+y}

def getalledges(edges):
  ret = {}
  for u in edges:
    for v in edges[u]:
      if (u,v) in ret or (v,u) in ret:
        continue
      ret[(u,v)] = 1
  return ret

def getGraphintoPresentableScale(graphedge, y, z):
    edges =getalledges(graphedge)
    tmp = {
        "nodes" : [newnode(u, y, z) for u in graphedge],
        "links" : [newedge(x,y) for x, y in edges]
    }
    return tmp   
# parse_bgp_message, parse_one_entry, getcolumns, parse_all_entries,get_graph_from_AS_path, getGraphintoPresentableScale
