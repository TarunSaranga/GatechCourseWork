"""Assess a betting strategy.                                                                                                                  
                                                                                                                  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)                                                                                                                  
Atlanta, Georgia 30332                                                                                                                  
All Rights Reserved                                                                                                                  
                                                                                                                  
Template code for CS 4646/7646                                                                                                                  
                                                                                                                  
Georgia Tech asserts copyright ownership of this template and all derivative                                                                                                                  
works, including solutions to the projects assigned in this course. Students                                                                                                                  
and other users of this template code are advised not to share it with others                                                                                                                  
or to make it available on publicly viewable websites including repositories                                                                                                                  
such as github and gitlab.  This copyright statement should not be removed                                                                                                                  
or edited.                                                                                                                  
                                                                                                                  
We do grant permission to share solutions privately with non-students such                                                                                                                  
as potential employers. However, sharing with other current or future                                                                                                                  
students of CS 7646 is prohibited and subject to being investigated as a                                                                                                                  
GT honor code violation.                                                                                                                  
                                                                                                                  
-----do not edit anything above this line---                                                                                                                  
                                                                                                                  
Student Name: Tharun Saranga
GT User ID: tsaranga3
GT ID: 903457046
"""                                                                                                                  
                                                                                                                  
import numpy as np
import matplotlib.pyplot as plt                                                                                                                  
                                                                                                                  
def author():                                                                                                                  
        return 'tsaranga3' # replace tb34 with your Georgia Tech username.                                                                                                                  
                                                                                                                  
def gtid():                                                                                                                  
    return 903457046 # replace with your GT ID number                                                                                                                  
                                                                                                                  
def get_spin_result(win_prob):                                                                                                                  
    result = False                                                                                                                  
    if np.random.random() <= win_prob:                                                                                                                  
        result = True                                                                                                                  
    return result                                                                                                                  
                                                                                                                  
def experiment1():                                                                                                                  
    win_prob = 18.0/38.0 # set appropriately to the probability of a win
    np.random.seed(gtid()) # do this only once
    xaxislim = 300                                                                                                             
    # add your code here to implement the experiments
    #Figure one
    final_graph = []
    for i in range(10):
        graph = [0]
        bet_amount = 1
        episode_winnings = 0
        for j in range(1000):
            won = False
            won = get_spin_result(win_prob)
            if(episode_winnings <80 ):
                if won:
                    episode_winnings = episode_winnings + bet_amount
                    bet_amount = 1
                else:
                    episode_winnings = episode_winnings - bet_amount
                    bet_amount = bet_amount*2
                
                graph.append(episode_winnings)
            else:
                graph.append(graph[-1])
        final_graph.append(graph)
    plt.figure()    
    for k in range(10):
        plt.plot(final_graph[k],label="sim:"+str(k+1))                                                                                                              
        plt.xlim(0,xaxislim)
        plt.ylim(-256,100)
    plt.legend()
    plt.title("Figure 1: Result of 10 Simulations (Unlimited bankroll)")
    plt.xlabel("episode number")
    plt.ylabel("episode winnings")
    plt.savefig("Figure1.png")
    
    #Figure Two
    final_graph = []
    wins = 0 
    for i in range(0,1000):
        graph = [0]
        bet_amount = 1
        episode_winnings = 0
        for j in range(1000):
            won = False
            won = get_spin_result(win_prob)
            if(episode_winnings <80 ):
                if won:
                    episode_winnings = episode_winnings + bet_amount
                    bet_amount = 1
                else:
                    episode_winnings = episode_winnings - bet_amount
                    bet_amount = bet_amount*2
                
                graph.append(episode_winnings)
            else:
                graph.append(graph[-1])
        if(np.amax(graph)>=80):
            wins = wins + 1
        final_graph.append(graph)
    
    #print("UB wins= ",wins)
    
    final_graph_mean = np.mean(final_graph,axis=0)
    plt.figure()
    plt.plot(final_graph_mean,label="mean")                           
    plt.plot(final_graph_mean + np.std(final_graph,axis=0),"r-.",label="mean+std")
    plt.plot(final_graph_mean - np.std(final_graph, axis=0),"g-.",label="mean-std")
    plt.legend()
    plt.xlim(0,xaxislim)
    plt.ylim(-256,100)
    plt.title("Figure 2: Mean of 1000 Simulations (Unlimited bankroll)")
    plt.xlabel("episode number")
    plt.ylabel("episode winnings")
    plt.savefig("Figure2.png")
    
    #Figure Thre
    final_graph_median = np.median(final_graph,axis=0)
    plt.figure()
    plt.plot(final_graph_median,label="median")                                                                                                              
    plt.plot(final_graph_median + np.std(final_graph,axis=0),"r-.",label="median+std")
    plt.plot(final_graph_median - np.std(final_graph,axis=0),"g-.",label="median-std")
    plt.legend()
    plt.xlim(0,xaxislim)
    plt.ylim(-256,100)
    plt.title("Figure 3: Median of 1000 Simulations (Unlimited bankroll)")
    plt.xlabel("episode number")
    plt.ylabel("episode winnings")
    plt.savefig("Figure3.png")
    
    
def experiment2():                                                                                                                  
    win_prob = 18.0/38.0 # set appropriately to the probability of a win
    np.random.seed(gtid()) # do this only once
    xaxislim = 300                                                                                                              
    # add your code here to implement the experiments
    
    
    #Figure Four
    final_graph = []
    wins = 0
    for i in range(0,1000):
        graph = [0]
        bet_amount = 1
        episode_winnings = 0
        for j in range(0,1000):
            won = False
            won = get_spin_result(win_prob)
            #if(episode_winnings + bet_amount >80 ):
            #    bet_amount = 80-episode_winnings
            if(episode_winnings - bet_amount < -256):
                bet_amount = 256 + episode_winnings 
                
            if(episode_winnings < 80 and episode_winnings > -256):
                if won:
                    episode_winnings = episode_winnings + bet_amount
                    bet_amount = 1
                else:
                    episode_winnings = episode_winnings - bet_amount
                    bet_amount = bet_amount*2
                
                graph.append(episode_winnings)
            else:
                graph.append(graph[-1])
        
        if(np.amax(graph)>=80):
            wins = wins + 1
        final_graph.append(graph)
    
    #print("LB wins = ",wins)
    final_graph_mean = np.mean(final_graph,axis=0)
    #print("Final Mean: ",final_graph_mean[-1])
    plt.figure()
    plt.plot(final_graph_mean,label="mean")                                                                                                              
    plt.plot(final_graph_mean + np.std(final_graph, axis=0),"r-.",label="mean+std")
    plt.plot(final_graph_mean - np.std(final_graph, axis=0),"g-.",label="mean-std")
    plt.legend()
    plt.xlim(0,xaxislim)
    plt.ylim(-256,100)
    plt.title("Figure 4: Mean of 1000 Simulations(Limited bankroll)")
    plt.xlabel("episode number")
    plt.ylabel("episode winnings")
    plt.savefig("Figure4.png")
    
    #Figure Five
    final_graph_median = np.median(final_graph,axis=0)
    plt.figure()
    plt.plot(final_graph_median,label="median")                                                                                                              
    plt.plot(final_graph_median + np.std(final_graph,axis=0),"r-.",label="median+std")
    plt.plot(final_graph_median - np.std(final_graph, axis=0),"g-.",label="median-std")
    plt.legend()
    plt.xlim(0,xaxislim)
    plt.ylim(-256,100)
    plt.title("Figure 5: Median of 1000 Simulations (Limited bankroll)")
    plt.xlabel("episode number")
    plt.ylabel("episode winnings")
    plt.savefig("Figure5.png")
    
    
if __name__ == "__main__":                                                                                                                  
    experiment1()
    experiment2()                                                                                                                  
