import numpy as np
import matplotlib.pyplot as plt

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
def simulate_multiple_outbreaks(N_sim = 1000):
    history_max_infect = np.zeros((N_sim, 2), dtype=int)

    for i in range(N_sim):
        history_i = simulate_outbreak()
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
