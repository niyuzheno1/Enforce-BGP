import pandas as pd 
from  preprocessing.bgpenvironment.training import bgp_environment_train
from agents.simpleqlearning.agent import intialize_q_table, q_learning_agent
from agents.tabiagent.agent import tabi_agent
#from agents.deepqlearning.agent import deepq_agent
intialize_q_table()
dataframe = pd.read_csv("data.csv")

print(bgp_environment_train(100, dataframe, q_learning_agent))