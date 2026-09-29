import numpy as np
import matplotlib.pyplot as plt
import random


alfa = 0.005
beta = 0.01
gamma = 0.10

states = ["S", "I", "R"]

N= 7300

def MonteCarlo():
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

    return chain




def plotting(N, chain, states =["S", "I", "R"]):

    chain_states = [states[i] for i in chain]

    prob_S = np.mean(chain[3650:] == 0)
    prob_I = np.mean(chain[3650:] == 1)
    prob_R = np.mean(chain[3650:] == 2)


    print(f"Probability of being in S: {prob_S}")
    print(f"Probability of being in I: {prob_I}")
    print(f"Probability of being in R: {prob_R}")

    print(f"Probability of being in S: {prob_S}")
    print(f"Probability of being in I: {prob_I}")
    print(f"Probability of being in R: {prob_R}")
    plt.step(range(N), chain_states)

    plt.ylabel("States")
    plt.yticks([0,1,2], states)
    plt.xlabel("timesteps")
    plt.show()


def AverageMontecarlo(n = 30):

    distribution_list = []

    for i in range(n):
        chain =  MonteCarlo()
        limiting_distribution = [np.mean(chain[3650:] == 0), np.mean(chain[3650:] == 1), np.mean(chain[3650:] == 2)]
        distribution_list.append(limiting_distribution)

    print(distribution_list)

AverageMontecarlo()






