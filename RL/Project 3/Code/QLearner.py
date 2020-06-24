from env import *

epsilon = .5 
gamma = .99 
alpha = .5 

num_iterations = 10000  
timeout = 25  

epsilon_decay = (epsilon-.001)/num_iterations
alpha_decayrate = (alpha-.001)/num_iterations


Q_1 = np.random.rand(len(S), len(actions))
Q_2 = np.random.rand(len(S), len(actions))

s0 = 71

err = [] 

forstepin range(num_iterations):
    s = s0  
    q_sa = Q_1[s0, 4]

    forstepin range(timeout):
        
        choice = np.random.rand()
        if choice <= e:
            a1 = actions[np.random.randint(5)]
            a2 = actions[np.random.randint(5)]
        else:

            a1 = actions[np.argmax(Q_1[s])] 
            a2 = actions[np.argmax(Q_2[s])]

        a = [a1, a2] 
        s_prime = transition(s, a) 
        
        r1 = R[s_prime, 0]
        r2 = R[s_prime, 1]
        
        Q_1[s, a1] = Q_1[s, a1] + alpha * (r1 + gamma * Q_1[s_prime, :].max() - Q_1[s, a1])
        Q_2[s, a2] = Q_2[s, a2] + alpha * (r2 + gamma * Q_2[s_prime, :].max() - Q_2[s, a2])
        
        s = s_prime
        
        if r1 != 0 or r2 != 0: break
    
    epsilon = epsilon - epsilon_decay
       
    if alpha > .001:
        alpha = alpha - alpha_decayrate
    err.append(np.abs(Q_1[s0, 4] - q_sa))
    print(step)

print(Q_1)

plt.plot(err)
plt.ylim([0,.5])
plt.show()