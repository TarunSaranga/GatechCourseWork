"""  		   	  			  	 		  		  		    	 		 		   		 		  
template for generating data to fool learners (c) 2016 Tucker Balch  		   	  			  	 		  		  		    	 		 		   		 		  
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
import math  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
# this function should return a dataset (X and Y) that will work  		   	  			  	 		  		  		    	 		 		   		 		  
# better for linear regression than decision trees  		   	  			  	 		  		  		    	 		 		   		 		  
def best4LinReg(seed=1489683273):  		   	  			  	 		  		  		    	 		 		   		 		  
    np.random.seed(seed)  		   	  			  	 		  		  		    	 		 		   		 		  
    rows = 60
    cols = 10
    X = np.random.random((rows,cols))  		   	  			  	 		  		  		    	 		 		   		 		  
    Y = np.zeros(rows)
    for i in range(rows):
        Y[i] = X[i,:].sum()
    
    return X, Y  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
def best4DT(seed=1489683273):  		   	  			  	 		  		  		    	 		 		   		 		  
    np.random.seed(seed)  	
    rows = 60
    cols = 10	   	  			  	 		  		  		    	 		 		   		 		  
    X = np.random.random((rows,cols))  		   	  			  	 		  		  		    	 		 		   		 		  
    Y = np.zeros(rows)		   	  	
    
    for i in range(rows):
        if(X[i,1]<0.5):
            Y[i]=0
        else:
            Y[i]=1
    		  	 		  		  		    	 		 		   		 		  
    return X, Y  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
def author():  		   	  			  	 		  		  		    	 		 		   		 		  
    return 'tsaranga3' #Change this to your user ID  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    print("they call me Tim.")  		   	  			  	 		  		  		    	 		 		   		 		  
