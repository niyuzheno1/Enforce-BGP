from agents.simpleqlearning.util import getstate, convert, STATE_SHAPE, ACTION_SHAPE
import random
import numpy as np

def q_learning_agent(obs, x):
  #learning rate
  alpha = 0.1
  gamma = 0.6
  epsilon = 0.1
  global laststate, lastaction, q_table
  if obs.step == 0:
    lastaction = 0
    laststate = None
    return 0
  cur = laststate
  laststate = getstate(x)
  if cur != None:
    #update our q_table
    updateidx = cur + convert([lastaction])
    old_value = q_table[updateidx]
    next_max = np.max(q_table[laststate])
    new_value = (1 - alpha) * old_value + alpha * (obs.lastreward + gamma * next_max)
    q_table[updateidx] = new_value
  if random.uniform(0, 1) < epsilon:
    action = (np.random.randint(2, size=1)[0] % 2)
  else:
    action = np.argmax(q_table[laststate])
  lastaction = action
  return action

def intialize_q_table():
    global q_table 
    q_table = np.zeros(STATE_SHAPE + ACTION_SHAPE)

