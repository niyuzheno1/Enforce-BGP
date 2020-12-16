from agents.tabiagent.util import EmulatedRIB, process_message
# tabi benchmark agent:
def tabi_agent(obs, x):
  #learning rate
  
  global rib
  if obs.step == 0:
    rib = EmulatedRIB()
    return 0
  u = process_message(rib, None, x, None)
  if len(u[2]) > 0:
    return 1
  else:
    return 0