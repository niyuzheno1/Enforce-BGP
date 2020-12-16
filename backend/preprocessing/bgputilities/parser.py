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