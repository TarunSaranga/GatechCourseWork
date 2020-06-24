from env import *
from cvxopt import matrix, solvers

np.random.seed(50)

gamma = .9 
alpha = .1 
epsilon = .2

test_state = 71 
test_action = 21 

num_iterations = 1000  
timeout = 25  

pi_1 = np.ones((112,5))/5
pi_2 = np.ones((112,5))/5

epsilon_decay = e/(10*num_iterations)
alpha_decay = alpha/num_iterations


Q_1 = np.random.rand(112, 5, 5)
Q_2 = np.random.rand(112, 5, 5)


rewards = []

s0 = 71 
err = [] 
prob = .2 

def findMinQ_2(Q_1):

    c = matrix([0.,0.,0.,0.,0.,1.0])

    G = matrix(np.array(
        [
    [-1.0, 0., 0., 0., 0., 0.],
    [ 0., -1.0, 0., 0., 0., 0.],
    [ 0., 0., -1.0, 0., 0., 0.],
    [ 0., 0., 0., -1.0, 0., 0.],
    [ 0., 0., 0., 0., -1.0, 0.],
    [ 0., 0., 0., 0., 0., -1.0],
    [Q_1[0, 0], Q_1[0, 1], Q_1[0, 2], Q_1[0, 3], Q_1[0, 4], -1.],
    [Q_1[1, 0], Q_1[1, 1], Q_1[1, 2], Q_1[1, 3], Q_1[1, 4], -1.],
    [Q_1[2, 0], Q_1[2, 1], Q_1[2, 2], Q_1[2, 3], Q_1[2, 4], -1.],
    [Q_1[3, 0], Q_1[3, 1], Q_1[3, 2], Q_1[3, 3], Q_1[3, 4], -1.],
    [Q_1[4, 0], Q_1[4, 1], Q_1[4, 2], Q_1[4, 3], Q_1[4, 4], -1.]
    ])
    )
    h = matrix([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    A = matrix([
        [1.],[1.],[1.],[1.],[1.],[0.]
    ])

    b = matrix([1.])

    solvers.options['show_progress'] = False
    sol = solvers.lp(c, G, h, A, b)

    primeDist = [sol['x'][0],sol['x'][1],sol['x'][2],sol['x'][3],sol['x'][4]]
    return primeDist

def findMinQ(Qmin):

    c = matrix([
        
        Qmin[0, 0] + Qmin[0, 1] + Qmin[0, 2] + Qmin[0, 3] + Qmin[0, 4],
        Qmin[1, 0] + Qmin[1, 1] + Qmin[1, 2] + Qmin[1, 3] + Qmin[1, 4],
        Qmin[2, 0] + Qmin[2, 1] + Qmin[2, 2] + Qmin[2, 3] + Qmin[2, 4],
        Qmin[3, 0] + Qmin[3, 1] + Qmin[3, 2] + Qmin[3, 3] + Qmin[3, 4],
        Qmin[4, 0] + Qmin[4, 1] + Qmin[4, 2] + Qmin[4, 3] + Qmin[4, 4]
    ])

    G = matrix([
    [-1.0, 0., 0., 0., 0.],
    [ 0., -1.0, 0., 0., 0.],
    [ 0., 0., -1.0, 0., 0.],
    [ 0., 0., 0., -1.0, 0.],
    [ 0., 0., 0., 0., -1.0]
    ])
    h = matrix([ 0.0, 0.0, 0.0, 0.0, 0.0])

    A = matrix([
        [1.],[1.],[1.],[1.],[1.]
    ])

    b = matrix([1.])
    solvers.options['show_progress'] = False
    sol = solvers.lp(c, G, h, A, b)

    primeDist = [sol['x'][0],sol['x'][1],sol['x'][2],sol['x'][3],sol['x'][4]]
    return primeDist

for T in range(num_iterations):
    s = s0  
    q_sa = Q_1[test_state, 4, 0]

    for t in range(timeout):
        choice = np.random.rand()

        if choice <= e:
            a1 = actions[np.random.randint(5)]
            a2 = actions[np.random.randint(5)]
        else:
            pi_1[s] = np.array(findMinQ(Q_1[s])) 
            pi_2[s]= np.array(findMinQ(Q_2[s]))
            
            a1 = np.argmax(pi_1[s])
            a2 = np.argmax(pi_2[s])

        a = [a1, a2]
        
        s_prime = transition(s, a) 

        r1 = R[s_prime, 0]
        r2 = R[s_prime, 1]

        v1 = pi_1[s_prime]* Q_1[s_prime]
        v2 = pi_2[s_prime]* Q_2[s_prime]
        Q_1[s, a1, a2] = (1. - alpha) * Q_1[s, a1, a2] + alpha * (r1 + gamma * v1.max())
        Q_2[s, a2, a1] = (1. - alpha) * Q_2[s, a2, a1] + alpha * (r2 + gamma * v2.max())


        s = s_prime
        if e > .001:
            e = e - epsilon_decay


        if r1 != 0 or r2 != 0:
            rewards.append([r1, r2])
            break

    if alpha > .001:
        alpha = alpha - alpha_decay

    err.append(np.abs(Q_1[test_state, 4, 0] - q_sa))
    # print Q_1[0]
    print(T)


# print Q_1

plt.plot(err)
plt.ylim([0,.5])
plt.show()from env import *
from cvxopt import matrix, solvers

np.random.seed(50)

gamma = .9 
alpha = .1 
e = .2

test_state = 71 
test_action = 21 

num_iterations = 1000  
timeout = 25  

pi_1 = np.ones((112,5))/5
pi_2 = np.ones((112,5))/5

epsilon_decay = e/(10*num_iterations)
alpha_decay = alpha/num_iterations


Q_1 = np.random.rand(112, 5, 5)
Q_2 = np.random.rand(112, 5, 5)


rewards = []

s0 = 71 
err = [] 
prob = .2 

def findMinQ_2(Q_1):

    c = matrix([0.,0.,0.,0.,0.,1.0])

    G = matrix(np.array(
        [
    [-1.0, 0., 0., 0., 0., 0.],
    [ 0., -1.0, 0., 0., 0., 0.],
    [ 0., 0., -1.0, 0., 0., 0.],
    [ 0., 0., 0., -1.0, 0., 0.],
    [ 0., 0., 0., 0., -1.0, 0.],
    [ 0., 0., 0., 0., 0., -1.0],
    [Q_1[0, 0], Q_1[0, 1], Q_1[0, 2], Q_1[0, 3], Q_1[0, 4], -1.],
    [Q_1[1, 0], Q_1[1, 1], Q_1[1, 2], Q_1[1, 3], Q_1[1, 4], -1.],
    [Q_1[2, 0], Q_1[2, 1], Q_1[2, 2], Q_1[2, 3], Q_1[2, 4], -1.],
    [Q_1[3, 0], Q_1[3, 1], Q_1[3, 2], Q_1[3, 3], Q_1[3, 4], -1.],
    [Q_1[4, 0], Q_1[4, 1], Q_1[4, 2], Q_1[4, 3], Q_1[4, 4], -1.]
    ])
    )
    h = matrix([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

    A = matrix([
        [1.],[1.],[1.],[1.],[1.],[0.]
    ])

    b = matrix([1.])

    solvers.options['show_progress'] = False
    sol = solvers.lp(c, G, h, A, b)

    primeDist = [sol['x'][0],sol['x'][1],sol['x'][2],sol['x'][3],sol['x'][4]]
    return primeDist

def findMinQ(Qmin):

    c = matrix([
        
        Qmin[0, 0] + Qmin[0, 1] + Qmin[0, 2] + Qmin[0, 3] + Qmin[0, 4],
        Qmin[1, 0] + Qmin[1, 1] + Qmin[1, 2] + Qmin[1, 3] + Qmin[1, 4],
        Qmin[2, 0] + Qmin[2, 1] + Qmin[2, 2] + Qmin[2, 3] + Qmin[2, 4],
        Qmin[3, 0] + Qmin[3, 1] + Qmin[3, 2] + Qmin[3, 3] + Qmin[3, 4],
        Qmin[4, 0] + Qmin[4, 1] + Qmin[4, 2] + Qmin[4, 3] + Qmin[4, 4]
    ])

    G = matrix([
    [-1.0, 0., 0., 0., 0.],
    [ 0., -1.0, 0., 0., 0.],
    [ 0., 0., -1.0, 0., 0.],
    [ 0., 0., 0., -1.0, 0.],
    [ 0., 0., 0., 0., -1.0]
    ])
    h = matrix([ 0.0, 0.0, 0.0, 0.0, 0.0])

    A = matrix([
        [1.],[1.],[1.],[1.],[1.]
    ])

    b = matrix([1.])
    solvers.options['show_progress'] = False
    sol = solvers.lp(c, G, h, A, b)

    primeDist = [sol['x'][0],sol['x'][1],sol['x'][2],sol['x'][3],sol['x'][4]]
    return primeDist

for T in range(num_iterations):
    s = s0  
    q_sa = Q_1[test_state, 4, 0]

    for t in range(timeout):
        choice = np.random.rand()

        if choice <= e:
            a1 = actions[np.random.randint(5)]
            a2 = actions[np.random.randint(5)]
        else:
            pi_1[s] = np.array(findMinQ(Q_1[s])) 
            pi_2[s]= np.array(findMinQ(Q_2[s]))
            
            a1 = np.argmax(pi_1[s])
            a2 = np.argmax(pi_2[s])

        a = [a1, a2]
        
        s_prime = transition(s, a) 

        r1 = R[s_prime, 0]
        r2 = R[s_prime, 1]

        v1 = pi_1[s_prime]* Q_1[s_prime]
        v2 = pi_2[s_prime]* Q_2[s_prime]
        Q_1[s, a1, a2] = (1. - alpha) * Q_1[s, a1, a2] + alpha * (r1 + gamma * v1.max())
        Q_2[s, a2, a1] = (1. - alpha) * Q_2[s, a2, a1] + alpha * (r2 + gamma * v2.max())


        s = s_prime
        if e > .001:
            e = e - epsilon_decay


        if r1 != 0 or r2 != 0:
            rewards.append([r1, r2])
            break

    if alpha > .001:
        alpha = alpha - alpha_decay

    err.append(np.abs(Q_1[test_state, 4, 0] - q_sa))
    print(T)


plt.plot(err)
plt.ylim([0,.5])
plt.show()
