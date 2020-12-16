# tabi benchmark agent:
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import numpy as np
from tensorflow.keras.models import load_model
 
def deepq_agent(obs, x):
  #learning rate
  def getstate( state):
        type = eval(str(state['type']))
        stype = eval(str(state['subtype']))
        u = np.asarray(int(type[0]))
        u = np.append(u, int(stype[0]))
        u = np.append(u, int(state['length']))
        u = np.append(u, int(state['peer_as']))
        u = np.append(u, int(state['local_as']))
        try:
          u = np.append(u, int(hash(state['peer_ip'])))
        except:
          u = np.append(u, 0)
        try:
          aspathseq = eval(str(state['AS_PATH_AS_SEQUENCE']))
          u = np.append(u, int(aspathseq[-1]))
        except:
          u = np.append(u, 0)
        try:
          u = np.append(u, int(state['bgp_message_nlri_prefix_length']))
        except:
          u = np.append(u, 0)
        u = np.append(u, int(hash(state['bgp_message_nlri_prefix'])))
        u = u.astype(float)
        return u.reshape(9, )
  global model
  if obs.step == 0:
    model = load_model("agents\\deepqlearning\\dqn-agent.h5")
    return 0
  state = getstate(x)
  state = np.reshape(state, [1, 9])
  action = np.argmax(model.predict(state))
  return 1-action