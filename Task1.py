import numpy as np
import matplotlib.pyplot as plt
import random


# Our transition probabilites

alfa = 0.005
beta = 0.01
gamma = 0.10


# S =Susceptible, I = infected, R = recovered/immune
states = ["S", "I", "R"]


# Number of days we run the simulation
N= 7300

def MonteCarlo(N = N, alfa = alfa, beta = beta, gamma = gamma):
    # Takes in:
    # Number of days we run the simulation
    # Transition probabilities

    # Returns:
    #   An array of numbers that corresponds to the three different states: 0 = S, 1 = I, 2 = R

    P = np.array([
        [1-beta, beta,        0],
        [0,      1-gamma, gamma],
        [alfa,   0,      1-alfa]
                                ])

    # Which state we are in a given day. The index in the array corresponds to the day.
    chain = np.zeros(N, dtype= int)

    chain[0] = 0

    for i in range(1,N):
        current_state = chain[i-1]

        p=P[current_state]

        # Takes the transistion probabilities from the transition matrix, and uses it to deterine the state in the next state.
        # 3 choices, and probabilities given by p. 
        chain[i] = np.random.choice(3, p=P[current_state]
        )

    return chain

def calculate_average(chain):
    # Calculates the average number of days per year spent in a state

    # Input:
    #   chain

    # Output
    # Calculates the average number of days per year spent in a state, as a list. 

    years = len(chain)/365    #Number of years in N days.
    average_spent = [sum(chain == 0)/years, sum(chain == 1)/years, sum(chain == 2)/years]
    return average_spent



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


# def AverageMontecarlo(n = 30):

#     state_dict = {}
#     state_dict["S"] = []
#     state_dict["I"] = []
#     state_dict["R"] = []


#     for i in range(n):
#         chain =  MonteCarlo()
#         limiting_distribution = [np.mean(chain[3650:] == 0), np.mean(chain[3650:] == 1), np.mean(chain[3650:] == 2)]
#         distribution_list.append(limiting_distribution)

#     print(distribution_list)

# AverageMontecarlo()

a = MonteCarlo(7300)

print(calculate_average(a))







