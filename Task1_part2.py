import numpy as np
import matplotlib.pyplot as plt

current_state = np.array([950, 50, 0])
N = 1000
n = 300
gamma = 0.1
alfa = 0.005

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

plt.plot(range(n+1), history, label = ["S", "I", "R"])
plt.xlabel("Day")
plt.ylabel("Number of individuals")
plt.legend()
plt.show()

print(current_state)