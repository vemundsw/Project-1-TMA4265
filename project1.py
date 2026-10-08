import numpy as np
import matplotlib.pyplot as plt
import random
import math


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
    num_days_list = np.zeros((n, 3))

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
    lower_limit = average - SD/np.sqrt(n) * t_95_29

    return lower_limit, upper_limit



# Here are the funcitons we can call:

# # Return the Markov chain
# MonteCarlo(7300)


# # Plot the Markov chain.
# plotting(7300, MonteCarlo())


# # Print the confidence interval: Lower and upper bounds for the average,
# print(confidence_interval95())



#task e
def simulate_outbreak(
    current_state = np.array([950, 50, 0]),
    N = 1000,
    n = 300,
    gamma = 0.1,
    alfa = 0.005
    ):
    current_state = current_state.copy()

    history = np.zeros((n+1, 3), dtype=int)
    history[0] = current_state

    for i in range(n):
        beta_n = 0.5*current_state[1]/N

        #S and I
        new_I = np.random.binomial(current_state[0], beta_n)
        
        #I and R
        new_R = np.random.binomial(current_state[1], gamma)

        #R and S
        new_S = np.random.binomial(current_state[2], alfa)
        
        #update
        current_state[0] -= new_I
        current_state[1] += new_I

        current_state[1] -= new_R
        current_state[2] += new_R

        current_state[2] -= new_S
        current_state[0] += new_S

        history[i+1] = current_state
    
    return history

history = simulate_outbreak()

plt.plot(range(300+1), history, label = ["S", "I", "R"])
plt.xlabel("Day")
plt.ylabel("Number of individuals")
plt.legend()
#plt.show()


#task f
def simulate_multiple_outbreaks(N_sim = 1000, function = simulate_outbreak):
    history_max_infect = np.zeros((N_sim, 2), dtype=int)

    for i in range(N_sim):
        history_i = function()
        max_day_i = np.argmax(history_i[:, 1])
        max_infected_i = history_i[:, 1][max_day_i]

        history_max_infect[i] = [max_day_i, max_infected_i]

    mean_infect_day_val = np.array([np.mean(history_max_infect[:, 0]), np.mean(history_max_infect[:, 1])])

    std = np.std(history_max_infect, axis=0, ddof=1)
    margin = 1.96*std/np.sqrt(len(history_max_infect))

    lower = mean_infect_day_val - margin
    upper = mean_infect_day_val + margin

    infect_day_CI = np.array([lower[0], upper[0]])
    infect_val_CI = np.array([lower[1], upper[1]])

    return mean_infect_day_val, infect_day_CI, infect_val_CI

mean_infect_day_val, infect_day_CI, infect_val_CI = simulate_multiple_outbreaks()

print(mean_infect_day_val)
print(infect_val_CI)
print(infect_day_CI)


#task g
fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharex=True, sharey=True)

for ax, vaccinated in zip(axes.flat, [0, 100, 600, 800]):
    history = simulate_outbreak(
        current_state=np.array([950 - vaccinated, 50, 0])
    )

    ax.plot(history, label=["S", "I", "R"])

    means, day_CI, infected_CI = simulate_multiple_outbreaks(
    function=lambda: simulate_outbreak(
        current_state=np.array([950 - vaccinated, 50, 0])
    )
    )

    ax.set_title(
        f"{vaccinated} vaccinated\n"
        f"Expected peak: {means[1]:.1f} infected\n"
        f"Expected first peak day: {means[0]:.1f}"
    )

    ax.set_xlabel("Day")
    ax.set_ylabel("Number of individuals")
    ax.legend()

plt.tight_layout()
plt.show()



### Problem 2a

### Part 1
def poisson_pdf(rate: float, time: float, x: int) -> float:
    """
    Probability density function of the Poison distribution

    rate: rate lambda of Poison distribution. Assumed constant
    time: time at which pdf is evaluated at
    x: number of occurences

    Returns a probability
    """

    return (rate * time) ** x / (math.factorial(x)) * math.exp(-rate * time)

claims = np.arange(0, 101)
rate = 1.5
days = 59

prob = 1 

# Summing up the probabilities
for i in range(100):
  prob -= poisson_pdf(rate, days, i)

print(f"The probability of more than 100 claims is {round(prob, 4)}")


### Part 2
def exp_quantile(u, rate = 1.5):
    """
    The inverse of the Cumulative Distribution Function for 
    the exponential distribution 

    u: a realization from Unif(0, 1)
    rate: the expectation of the expontential distribution

    Returns a realization of the expontential distribution
    """
    return -1 / rate * np.log(1 - u)

N = 10000
prob_b = 0


for j in range(N):

    # Drawing 100 realizations from the exponential distribution 
    # and checking whether they occur within 59 days
    time = np.sum(exp_quantile(np.random.uniform(0, 1, 100)))

    if time < 59: 
        prob_b += 1

prob_b /= N

print(f"The probability of more than 100 claims simulated by exponential distribution is {round(prob_b, 4)}")


### Part 3
N = 10
time_list = []
x_list = []

for i in range(N):

    time = 0
    x = 0

    # Simulate from the exponential distribution and count realizations
    # until until time lapsed becomes too long
    while time < 59:

        x += 1
        time += exp_quantile(np.random.uniform(0, 1, 1))
    
    x_list.append(x)
    time_list.append(time)

print(x_list)
plt.hist( x_list, bins = 10)
plt.title(fr"{N} realizations of $X(t), 0 \leq t \leq 59$")
plt.xlabel("Claims recieved")
plt.show()

    

### Problem 2b
### Part 1

N = 1000
gamma = 10
prob = 0

for i in range(N): 

    # Determining X by simulating from the Poisson distribution as earlier
    time = 0
    x = 0
    z = 0
    
    # Simulate from the exponential distribution and count realizations
    # until until time lapsed becomes too long
    while time < 59:
    
            x += 1
            time += exp_quantile(np.random.uniform(0, 1, 1))

    # Sum up the claim amounts of each claim
    for j in range(x):
        z += exp_quantile(np.random.uniform(0, 1, 1), rate = gamma)

    if z > 8:
        prob += 1
    
prob /= N

print(f"The estimated probability of the total claim amount exceeding 8 mill kr is {round(prob, 4)}")


### Part 2 
N = 10
z_list = []
for i in range(N): 

    # Determining X by simulating from the Poisson distribution as earlier
    time = 0
    x = 0
    z = 0
    
    # Simulate from the exponential distribution and count realizations
    # until until time lapsed becomes too long
    while time < 59:
    
            x += 1
            time += exp_quantile(random.uniform(0, 1))

    # Sum up the claim amounts of each claim
    for j in range(x):
        z += exp_quantile(random.uniform(0, 1), rate = gamma)

    z_list.append(z)


plt.hist(z_list, bins = 10)
plt.title(fr"{N} realizations of $X(t), 0 \leq t \leq 59$")
plt.xlabel("Total claim amount (mill kr)")
plt.show()








