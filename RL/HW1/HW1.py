import numpy as np
import mdptoolbox

N = 6
isBadSide = [0]+[1,1,1,0,0,0]

prob = np.zeros((2,N+1,N+1))

bankroll = 0

for i in range(len(prob[0])):
    for j in range(len(prob[0][0])):
        prob[0][i][j] = 1.0/N
        prob[0][i][0] = isBadSide[i]
        
        prob[1][i][0] = 1.0

rewards = np.zeros((N,2))

for i in range(N):
    rewards[i,0] = (1+i)*(1-isBadSide[i])
    rewards[1,1] = bankroll


vi = mdptoolbox.mdp.ValueIteration(prob, rewards, 1)

vi.run()

optimal_policy = vi.policy
expected_values = vi.V
sum = 0 
for i in range(len(expected_values)):
    sum += expected_values[i]

e = sum/len(expected_values)
