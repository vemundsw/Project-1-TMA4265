
import numpy as np
import matplotlib.pyplot as plt
import random

def exp_quantile(u, rate = 1.5):
    """
    The inverse of the Cumulative Distribution Function for 
    the exponential distribution 

    u: a realization from Unif(0, 1)
    rate: the expectation of the expontential distribution

    Returns a realization of the expontential distribution
    """
    return -1 / rate * np.log(1 - u)


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