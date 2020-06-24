"""                                                                                                                  
Test a learner.  (c) 2015 Tucker Balch                                                                                                                  
                                                                                                                  
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
"""                                                                                                                  
                                                                                                                  
import numpy as np  
import matplotlib.pyplot as plt                                                                                                                
import math      
import util     
import time                                                                                                       
import LinRegLearner as lrl      
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl    
import sys                                                                                                                  
                                                                                                                  

def experiment1(trainX,trainY,testX,testY):
    """
    Over fitting with respect to leaf_size on DTLearner
    Plot RMSE for different leaf_sizes
    """
    insample_rmse = []
    outsample_rmse = []
    leaf = []
    for leaf_size in range(1,100):
        leaf.append(leaf_size)
        learner = dt.DTLearner(leaf_size = leaf_size, verbose = True) 
        learner.addEvidence(trainX, trainY) 
        
        predY = learner.query(trainX) # get the predictions                                                                                                                  
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])                                                                                                                  
        insample_rmse.append(rmse)        
        
        predY = learner.query(testX) # get the predictions                                                                                                                  
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])                                                                                                                  
        outsample_rmse.append(rmse)
    
    plt.figure()
    plt.plot(leaf,insample_rmse,'c',label="insample")
    plt.plot(leaf,outsample_rmse,'g',label="outsample")
    plt.legend()
    plt.xlim(0,100)
    
    plt.xlabel("leaf_size")
    plt.ylabel("RMSE")
    plt.title("Experiment1")
    plt.savefig("Experiment1.png")




def experiment2(trainX,trainY,testX,testY):
    """
    Over fitting with respect to leaf_size on DTLearner with bagging
    Plot RMSE for different leaf_sizes
    """
    insample_rmse = []
    outsample_rmse = []
    leaf = []
    for leaf_size in range(1,100):
        leaf.append(leaf_size)
        learner = bl.BagLearner(dt.DTLearner,kwargs={"leaf_size":leaf_size}, verbose = True) 
        learner.addEvidence(trainX, trainY) 
        
        predY = learner.query(trainX) # get the predictions                                                                                                                  
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])                                                                                                                  
        insample_rmse.append(rmse)        
        
        predY = learner.query(testX) # get the predictions                                                                                                                  
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])                                                                                                                  
        outsample_rmse.append(rmse)
    
    plt.figure()
    plt.plot(leaf,insample_rmse,'c',label="insample")
    plt.plot(leaf,outsample_rmse,'g',label="outsample")
    plt.legend()
    plt.xlim(0,100)
    
    plt.xlabel("leaf_size")
    plt.ylabel("RMSE")
    plt.title("Experiment2")
    plt.savefig("Experiment2.png")
    

def experiment3(trainX,trainY,testX,testY):
    """
    Over fitting with respect to leaf_size on DTLearner with bagging
    Plot RMSE for different leaf_sizes
    """
    dtoutsample_rmse = []
    dttime = []
    rttime = []
    rtoutsample_rmse = []
    leaf = []
    for leaf_size in range(1,100):
        leaf.append(leaf_size)
        start_time = time.time()
        learner = dt.DTLearner(leaf_size=leaf_size, verbose = True) 
        learner.addEvidence(trainX, trainY) 
        dttime.append(time.time()-start_time)
        
        predY = learner.query(testX) # get the predictions                                                                                                                  
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])                                                                                                                  
        dtoutsample_rmse.append(rmse)
        
        start_time = time.time()
        learner = rt.RTLearner(leaf_size=leaf_size, verbose = True) 
        learner.addEvidence(trainX, trainY) 
        rttime.append(time.time()-start_time)
                
        predY = learner.query(testX) # get the predictions                                                                                                                  
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])                                                                                                                  
        rtoutsample_rmse.append(rmse)
    
    
    plt.figure()
    plt.plot(leaf,dtoutsample_rmse,'c',label="Classical Decision Tree")
    plt.plot(leaf,rtoutsample_rmse,'g',label="Random Decision Tree")
    plt.legend()
    plt.xlim(0,100)
    
    plt.xlabel("leaf_size")
    plt.ylabel("RMSE")
    plt.title("Experiment3_outsample_errors")
    plt.savefig("Experiment3_outsample.png")
    
    plt.figure()
    plt.plot(leaf,dttime,'c',label="Classical Decision Tree")
    plt.plot(leaf,rttime,'g',label="Random Decision Tree")
    plt.legend()
    plt.xlim(0,100)
    
    plt.xlabel("leaf_size")
    plt.ylabel("Time")
    plt.title("Experiment3_ConstructionTime")
    plt.savefig("Experiment3_time.png")


if __name__=="__main__":                                                                                                                  
    if len(sys.argv) != 2:                                                                                                                  
        print("Usage: python testlearner.py <filename>")                                                                                                                  
        sys.exit(1)                                                                                                                  
    datafile = sys.argv[1]
     		   	  			  	 		  		  		    	 		 		   		 		  
    alldata = np.genfromtxt(str(datafile),delimiter=',')  		   	  			  	 		  		  		    	 		 		   		 		  
    # Skip the date column and header row if we're working on Istanbul data  		   	  			  	 		  		  		    	 		 		   		 		  
    alldata = alldata[1:,1:]  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                                            
#    # compute how much of the data is training and testing                                                                                                                  
    train_rows = int(0.6* alldata.shape[0])                                                                                                                  
    test_rows = alldata.shape[0] - train_rows                                                                                                                  
                                                                                                                  
    # separate out training and testing data                                                                                                                  
    trainX = alldata[:train_rows,0:-1]                                                                                                                  
    trainY = alldata[:train_rows,-1]                                                                                                                  
    testX = alldata[train_rows:,0:-1]                                                                                                                  
    testY = alldata[train_rows:,-1]                                                                                                                  
                                                                                                                  
    print(f"{testX.shape}")                                                                                                                  
    print(f"{testY.shape}")      
    
    experiment1(trainX,trainY,testX,testY)                                                                   
    experiment2(trainX,trainY,testX,testY)
    experiment3(trainX,trainY,testX,testY)                    
                                                                                                             
                                                                                                                                                                                                                                
                                                                                                                  
                                                                                                            


    
    