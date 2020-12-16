from  preprocessing.bgpenvironment.environment import Environment
import pandas as pd
def bgp_environment_train(epochs, traindataframe,agent):
    rewards = []
    p = r = 0
    pclist = []
    print("precision, recall, false positive, specificity")
    for epoch in range(0,epochs):
        testbed = Environment(100,traindataframe)
        rewards.append(testbed.train(agent))
        if epoch % 10 == 0:
            p = testbed.getpercision()
            r = testbed.getrecall()
            s = testbed.getspecificity()
            fp = testbed.getfalsepositive()
            print("{},{}, {}, {}".format(p, r, fp, s))
            pclist.append((p,r))
    crewards = pd.DataFrame({ "r" : rewards})
    return crewards, p , r