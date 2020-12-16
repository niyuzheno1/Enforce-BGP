def convert(list): 
    return tuple(list) 
STATE_SHAPE = (10, 9, 5, 8, 9)
ACTION_SHAPE = convert([2])

def getstate(x):
  if x is None:
    return (0,0,0,0,0)
  state = [] # (10, 9, 5, 8, 9)
  u = hash(x['peer_ip']) % 10
  state.append(u)
  try:
    u = hash(x['AS_PATH_AS_SEQUENCE'][-1]) % 9
  except:
    u = 0
  state.append(u)
  try:
    u = hash(x['MULTI_EXIT_DISC_value']) % 5
  except:
    u = 0
  state.append(u)
  try:
    u = hash(x['COMMUNITY_value'][-1]) % 8
  except:
    u = 0 
  state.append(u)
  u = hash(x['subtype'][-1]) % 9
  state.append(u)
  for i in range(0, len(state)):
    state[i] = int(state[i])
  return convert(state)