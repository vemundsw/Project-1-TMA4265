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

def calculate_days_per_year(chain):
    # Calculates the average number of days per year spent in a state

    # Input:
    #   chain

    # Output
    # Calculates the average number of days per year spent in a state, as a list. 

    years = len(chain)/365    #Number of years in N days.
    days_per_year = [sum(chain == 0)/years, sum(chain == 1)/years, sum(chain == 2)/years]
    return days_per_year




def plotting(N, chain, states =["S", "I", "R"]):
    # A helping tool, to visualise the transitions.

    chain_states = [states[i] for i in chain]

    prob_S = np.mean(chain[3650:] == 0)
    prob_I = np.mean(chain[3650:] == 1)
    prob_R = np.mean(chain[3650:] == 2)


    print(f"Probability of being in S: {prob_S}")
    print(f"Probability of being in I: {prob_I}")
    print(f"Probability of being in R: {prob_R}")


    plt.step(range(N), chain_states)
    plt.ylabel("States")
    plt.yticks([0,1,2], states)
    plt.xlabel("timesteps")
    plt.show()


def confidence_interval95():
    # Calculates the 95% confidence interval for the mean number of days per year spent in each states.
    # We always use 30 simulations, as the student t-quantile depends on degrees of freedom.

    # Input:
    
    # Output:
    #   95% confidence interval for the expected value.

    n = 30     # Number of simulations
    num_days_list = np.zeros(n)

    for i in range(n):
        chain =  MonteCarlo()
        days_per_year = calculate_days_per_year(chain)
        num_days_list[i] = days_per_year

    average = sum(num_days_list)/len(num_days_list)
    SD = 0

    for simulation in num_days_list:
        SD += (simulation - average)**2

    SD = np.sqrt(1/( n-1 ) * SD)     # Standard deviation

    #Critical value for the student t-distribution. 
    # 29 degrees of freedom
    # 95 % confidence interval: alfa = 0.025  (Blir dette riktig måte å skrive det på. To forskjellige alfaer?)
    t_95_29 = 2.045    

    upper_limit = average + SD/np.sqrt(n) * t_95_29
    lower_limiit = average - SD/np.sqrt(n) * t_95_29

    return upper_limit, lower_limiit

print(confidence_interval95())


        

        




# a = MonteCarlo(7300)

# print(calculate_average(a))

# plotting(N, MonteCarlo())






