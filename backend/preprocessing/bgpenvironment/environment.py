import numpy as np

class Observe:
  def __init__(self, dataframe):
    self.step = 0
    self.lastreward = 0
    self.action = -1
    self.data = dataframe
    self.prefixpool = dataframe["bgp_message_nlri_prefix"].unique()
    self.size = dataframe.count()['timestamp']
    self.truepositive = 0
    self.totalpositve = 0
    self.falsepositive = 0
    self.falsenegative = 0
    self.truenegative, self.falsenegative = (0.0,0.0)
  def reset(self,dataframe):
    self.step = 0
    self.lastreward = 0
    self.action = -1
    self.data = dataframe
    self.prefixpool = dataframe["bgp_message_nlri_prefix"].unique()
    self.size = dataframe.count()['timestamp']
  def inc(self, action):
    if self.step != 0:
      if action == 1:
        self.totalpositve += 1
      if self.action == action:
        self.lastreward = 50
        if self.action == 1:
          self.truepositive = self.truepositive + 1
        else:
          self.falsepositive = self.falsepositive + 1
      else:
        if self.action == 1:
          self.falsenegative += 1
        else: 
          self.truenegative += 1
        self.lastreward = -100
    ret = None
    if np.random.randint(3, size = 1)[0] < 1:
      self.action = 0
      ret = self.data.iloc[self.step]
    else:
      self.action = 1 # ip hijacking/ misconfiguration
      ret = self.data.iloc[self.step].copy()
      pix = np.random.randint(len(self.prefixpool) ,size= 1)[0]
      ret['bgp_message_nlri_prefix'] = self.prefixpool[pix]
    self.step = self.step + 1
    return ret    
  def isdone(self):
    return self.step + 1 >= self.size-20

class Environment:
  def __init__(self, msteps, dataframe):
     self.obs = Observe(dataframe)
     self.maxsteps = msteps
     self.cumulaterewards = 0
     
  def train(self,agent):
    testing = 0
    lastaction = None
    agent(self.obs, None)
    while testing < self.maxsteps and (not self.obs.isdone()):
      testing = testing + 1
      newobs = self.obs.inc(lastaction)
      lastaction = agent(self.obs, newobs)
      self.cumulaterewards += self.obs.lastreward
    return self.cumulaterewards
  def getpercision(self):
    return self.obs.truepositive/self.obs.totalpositve
  def getrecall(self):
    return self.obs.truepositive/(self.obs.falsenegative+self.obs.truepositive)
  def getsensitivity(self):
    return self.obs.truepositive/(self.obs.falsenegative+self.obs.truepositive)
  def getspecificity(self):
    return self.obs.truenegative/(self.obs.truenegative + self.obs.falsepositive)
  def getfalsepositive(self):
    return 1.0-self.getspecificity()