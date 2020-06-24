from env import *
from cvxopt import matrix, solvers


gamma = .9 
alpha = .5 
epsilon = .9

test_action = 21 
test_state = 71

num_iterations = 1000  
timeout = 25 

epsilon_decay= epsilon/(num_iterations)
alpha_decay = alpha/num_iterations

Q_1 = np.random.rand(112, 25)
Q_2 = np.random.rand(112, 25)

pi_1 = np.ones((112,25))
pi_2 = np.ones((112,25))

s0 = 71 

error = [] 

prob = .9 

def findMinQ_2(Q_1):

    c = matrix(
    [
        -Q_1[0,0],
        -Q_1[0, 1],
        -Q_1[0, 2],
        -Q_1[0, 3],
        -Q_1[0, 4],
        -Q_1[1, 0],
        -Q_1[1, 1],
        -Q_1[1, 2],
        -Q_1[1, 3],
        -Q_1[1, 4],
        -Q_1[2, 0],
        -Q_1[2, 1],
        -Q_1[2, 2],
        -Q_1[2, 3],
        -Q_1[2, 4],
        -Q_1[3, 0],
        -Q_1[3, 1],
        -Q_1[3, 2],
        -Q_1[3, 3],
        -Q_1[3, 4],
        -Q_1[3, 0],
        -Q_1[4, 1],
        -Q_1[4, 2],
        -Q_1[4, 3],
        -Q_1[4, 4],
        -Q_2[0, 0],
        -Q_2[0, 1],
        -Q_2[0, 2],
        -Q_2[0, 3],
        -Q_2[0, 4],
        -Q_2[1, 0],
        -Q_2[1, 1],
        -Q_2[1, 2],
        -Q_2[1, 3],
        -Q_2[1, 4],
        -Q_2[2, 0],
        -Q_2[2, 1],
        -Q_2[2, 2],
        -Q_2[2, 3],
        -Q_2[2, 4],
        -Q_2[3, 0],
        -Q_2[3, 1],
        -Q_2[3, 2],
        -Q_2[3, 3],
        -Q_2[3, 4],
        -Q_2[3, 0],
        -Q_2[4, 1],
        -Q_2[4, 2],
        -Q_2[4, 3],
        -Q_2[4, 4]
        ]
    )

   
    G = matrix(np.identity(50)*-1)

    h = matrix([ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0])

    A = matrix([
        [1.],[1.],[1.],[1.],[1.],[1.],[1.],[1.],[1.],[1.],
        [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.],
        [1.], [1.], [1.], [1.], [1.],
        [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.],
        [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.],
        [1.], [1.], [1.], [1.], [1.]
    ])

    b = matrix([1.])
    solvers.options['show_progress'] = False
    sol = solvers.lp(c, G, h, A, b)

    primeDist = [sol['x'][0],sol['x'][1],sol['x'][2],sol['x'][3],sol['x'][4],sol['x'][5],sol['x'][6],sol['x'][7],sol['x'][8],sol['x'][9],
                 sol['x'][10], sol['x'][11], sol['x'][12], sol['x'][13], sol['x'][14], sol['x'][15], sol['x'][16], sol['x'][17], sol['x'][18], sol['x'][19],
                 sol['x'][20], sol['x'][21], sol['x'][22], sol['x'][23], sol['x'][24],
             
                 ]
    return primeDist

def findMinQ(Q_1, Q_2):
    

    c = matrix([
        -Q_1[0],-Q_1[1],-Q_1[2],-Q_1[3],-Q_1[4],-Q_1[5],-Q_1[6],-Q_1[7],-Q_1[8],-Q_1[9],
        -Q_1[10],-Q_1[11],-Q_1[12],-Q_1[13],-Q_1[14],-Q_1[15],-Q_1[16],-Q_1[17],-Q_1[18],-Q_1[19],
        -Q_1[20],-Q_1[21],-Q_1[22],-Q_1[23],-Q_1[24],

        -Q_2[0], -Q_2[1], -Q_2[2], -Q_2[3], -Q_2[4], -Q_2[5], -Q_2[6], -Q_2[7], -Q_2[8], -Q_2[9],
        -Q_2[10], -Q_2[11], -Q_2[12], -Q_2[13], -Q_2[14], -Q_2[15], -Q_2[16], -Q_2[17], -Q_2[18], -Q_2[19],
        -Q_2[20], -Q_2[21], -Q_2[22], -Q_2[23], -Q_2[24],
        ])

    G = matrix(np.identity(50) * -1)

    h = matrix(
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0])

    A = matrix([
        [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.],
        [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.],
        [1.], [1.], [1.], [1.], [1.],
        [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.],
        [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.], [1.],
        [1.], [1.], [1.], [1.], [1.]
    ])

    b = matrix([1.])
    solvers.options['show_progress'] = False
    sol = solvers.lp(c, G, h, A, b)

    primeDist = [sol['x'][0], sol['x'][1], sol['x'][2], sol['x'][3], sol['x'][4], sol['x'][5], sol['x'][6], sol['x'][7],
                 sol['x'][8], sol['x'][9],
                 sol['x'][10], sol['x'][11], sol['x'][12], sol['x'][13], sol['x'][14], sol['x'][15], sol['x'][16],
                 sol['x'][17], sol['x'][18], sol['x'][19],
                 sol['x'][20], sol['x'][21], sol['x'][22], sol['x'][23], sol['x'][24],
                 
                 ]
    return primeDist


for T in range(num_iterations):
    s = s0  
    q_sa = Q_1[test_state, 21]

    for t in range(timeout):
        choice = np.random.rand()
        # QtableV = Q_1.sum()

        if choice <= e:
            a1 = np.random.randint(25)
            a2 = np.random.randint(25)
        else:

            prime1 = findMinQ(Q_1[s], Q_2[s]) 
            prime2 = findMinQ(Q_2[s], Q_1[s])

            pi_1[s] = prime1 
            pi_2[s] = prime2

            QwithProb1 = Q_1[s]*prime1 
            QwithProb2 = Q_2[s]*prime2

            a1c = np.argmax(QwithProb1) 
            a2c = np.argmax(QwithProb2)
          

            a1 = A[a1c][0]
            a2 = A[a2c][0]
            

        a = [a1, a2] 

        s_prime = transition(s, a) 

        
        r1 = R[s_prime, 0]
        r2 = R[s_prime, 1]

        anp = np.array(a)
        for i in range(A.shape[0]):
            if np.array_equal(A[i], anp):
                aindex = i
                break
        anp = np.array([a2,a1])
        for j in range(A.shape[0]):
            if np.array_equal(A[j], anp):
                aindex = j
                break

        v1 = Q_1[s_prime]*pi_1[s_prime]
        v2 = Q_2[s_prime]*pi_2[s_prime]

        Q_1[s, i] = (1. - alpha) * Q_1[s, i] + alpha * ((1-gamma)*r1 + gamma * v1.max())
        Q_2[s, j] = (1. - alpha) * Q_2[s, j] + alpha * ((1-gamma)*r2 + gamma * v2.max())

        
        s = s_prime
        if e > .001:
            e = e - e_decay
      
        if r1 != 0 or r2 != 0:
            break
            

    error.append(np.abs(Q_1[test_state, 21] - q_sa))
        print(T)
    
    if alpha > .001:
        alpha = alpha * .99999
    


plt.plot(error)
plt.ylim([0,.5])
plt.show()
