import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model, load_model
import numpy as np
from collections import deque
import random
def make_model():
    model = Sequential()
    model.add(Dense(32))
    model.add(Dense(32))
    model.add(Dense(32))
    model.add(Dense(2, activation='linear'))  
    model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])
    return model

class DQNAgent:
    def __init__(self, ob, traindataframe):
        self.env = ob(traindataframe)
        self.dataframe = traindataframe
        # by default, CartPole-v1 has max episode steps = 500
        self.state_size = 9
        self.action_size = 2
        self.EPISODES = 50
        self.memory = deque(maxlen=2000)
        
        self.gamma = 0.6    # discount rate
        self.epsilon = 0.1  # exploration rate
        self.epsilon_min = 0.001
        self.epsilon_decay = 0.999
        self.batch_size = 64
        self.train_start = 1000

        # create main model
        self.model = make_model()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        if len(self.memory) > self.train_start:
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

    def act(self, state):
        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            return np.argmax(self.model.predict(state))

    def replay(self):
        if len(self.memory) < self.train_start:
            return
        # Randomly sample minibatch from the memory
        minibatch = random.sample(self.memory, min(len(self.memory), self.batch_size))

        state = np.zeros((self.batch_size, self.state_size))
        next_state = np.zeros((self.batch_size, self.state_size))
        action, reward, done = [], [], []

        # do this before prediction
        # for speedup, this could be done on the tensor level
        # but easier to understand using a loop
        for i in range(self.batch_size):
            state[i] = minibatch[i][0]
            action.append(minibatch[i][1])
            reward.append(minibatch[i][2])
            next_state[i] = minibatch[i][3]
            done.append(minibatch[i][4])

        # do batch prediction to save speed
        target = self.model.predict(state)
        target_next = self.model.predict(next_state)

        for i in range(self.batch_size):
            # correction on the Q value for the action used
            if done[i]:
                target[i][action[i]] = reward[i]
            else:
                # Standard - DQN
                # DQN chooses the max Q value among next actions
                # selection and evaluation of action is on the target Q Network
                # Q_max = max_a' Q_target(s', a')
                target[i][action[i]] = reward[i] + self.gamma * (np.amax(target_next[i]))

        # Train the Neural Network with batches
        self.model.fit(state, target, batch_size=self.batch_size, verbose=0)


    def load(self, name):
        self.model = load_model(name)

    def save(self, name):
        self.model.save(name)
    
    def getstate(self, state):
        u = np.asarray(int(state['type'][0]))
        u = np.append(u, int(state['subtype'][0]))
        u = np.append(u, int(state['length']))
        u = np.append(u, int(state['peer_as']))
        u = np.append(u, int(state['local_as']))
        try:
          u = np.append(u, int(hash(state['peer_ip'])))
        except:
          u = np.append(u, 0)
        try:
          u = np.append(u, int(state['AS_PATH_AS_SEQUENCE'][-1]))
        except:
          u = np.append(u, 0)
        try:
          u = np.append(u, int(state['bgp_message_nlri_prefix_length']))
        except:
          u = np.append(u, 0)
        u = np.append(u, int(hash(state['bgp_message_nlri_prefix'])))
        u = u.astype(float)
        return u.reshape(self.state_size, )

    def run(self):
        for e in range(self.EPISODES):
            self.env.reset(self.dataframe)
            state = self.getstate(self.env.inc(0))
            state = np.reshape(state, [1, self.state_size])
            done = False
            i = 0
            reward = 0
            creward = 0
            while not done:
                action = self.act(state)
                next_state = self.getstate(self.env.inc(action))
                reward = self.env.lastreward
                creward += reward
                done = self.env.isdone()
                next_state = np.reshape(next_state, [1, self.state_size])
                if not done:
                    reward = reward
                else:
                    reward = -100
                self.remember(state, action, reward, next_state, done)
                state = next_state
                i += 1
                if done:                   
                    print("episode: {}/{}, score: {}, e: {:.2}".format(e, self.EPISODES, creward, self.epsilon))
                    if i == 500:
                        self.save("dqn-agent.h5")
                        return
                self.replay()

    def test(self):
        self.load("dqn-agent.h5")
        for e in range(self.EPISODES):
            state = self.env.reset()
            state = np.reshape(state, [1, self.state_size])
            done = False
            i = 0
            while not done:
                action = np.argmax(self.model.predict(state))
                next_state = self.getstate(self.env.inc(action))
                reward = self.env.lastreward
                done = self.env.isdone()
                next_state = np.reshape(next_state, [1, self.state_size])
                state = np.reshape(next_state, [1, self.state_size])
                i += 1
                if done:
                    print("episode: {}/{}, score: {}".format(e, self.EPISODES, i))
                    break