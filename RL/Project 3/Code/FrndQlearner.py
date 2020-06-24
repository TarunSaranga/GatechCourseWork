from env import *

epsilon = .5 
gamma = .99 
alpha = .3

test_state = 71 
test_state = 21 

num_iterations = 1000 
timeout = 25 

epsilon_decay = (epsilon-.001)/num_iterations
alpha_decay = (alpha-.001)/num_iterations


Q_1 = np.random.rand(len(S), len(A))
Q_2 = np.random.rand(len(S), len(A))


s0 = 71 

err = [] 

for T in range(num_iterations):
    s = s0  
    q_sa = Q_1[test_state, test_state]

    for t in range(timeout):
        
        choice = np.random.rand()
        if choice <= epsilon: 
            a1 = A[np.random.randint(25)][0]
            a2 = A[np.random.randint(25)][1]
        else:  
            a1 = A[np.argmax(Q_1[s])][0]
            a2 = A[np.argmax(Q_2[s])][1]

        a = [a1, a2]
        s_prime = transition(s, a) 

       
        r1 = R[s_prime, 0]
        r2 = R[s_prime, 1]

        np_a = np.array(a)
        for i in range(A.shape[0]):
            if np.array_equal(A[i], np_a):
                updateA = i
                break

        Q_1[s, updateA] = Q_1[s, updateA] + alpha * (r1 + gamma * Q_1[s_prime, :].max() - Q_1[s, updateA])
        Q_2[s, updateA] = Q_2[s, updateA] + alpha * (r2 + gamma * Q_2[s_prime, :].max() - Q_2[s, updateA])
       
        s = s_prime
  
        epsilon = epsilon - epsilon_decay
        
        if alpha > .001:
            alpha = alpha - alpha_decay
        
        if r1 != 0 or r2 != 0: break
   
    err.append(np.abs(Q_1[test_state, test_state] - q_sa))
    
    print(T)

print(Q_1)

plt.plot(err)
plt.ylim([0,.5])
plt.show()