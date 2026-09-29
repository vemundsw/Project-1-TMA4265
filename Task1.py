import numpy as np
import matplotlib.pyplot as plt
import random


alfa = 0.005
beta = 0.01
gamma = 0.10

states = ["S", "I", "R"]

N= 7300

P = np.array([
    [1-beta, beta,        0],
    [0,      1-gamma, gamma],
    [alfa,   0,      1-alfa]
                            ])


chain = np.zeros(N, dtype= int)

chain[0] = 0

for i in range(1,N):
    current_state = chain[i-1]

    p=P[current_state]

    chain[i] = np.random.choice(3, p=P[current_state]
    )

chain_states = [states[i] for i in chain]

print(chain_states[:40])


