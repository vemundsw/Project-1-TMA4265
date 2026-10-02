import math
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import matplotlib.pyplot as plt

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

    

