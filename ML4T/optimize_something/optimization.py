"""MC1-P2: Optimize a portfolio.                                                                                                                  
                                                                                                                  
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
                                                                                                                  
                                                                                                                  
import pandas as pd                                                                                                                  
import matplotlib.pyplot as plt
import matplotlib.dates as mdates                                                                                                                  
import numpy as np     
import scipy.optimize as spo
from scipy.optimize import Bounds
from scipy.optimize import LinearConstraint
import datetime as dt                                                                                                                  
from util import get_data, plot_data                                                                                                                  
                                                                                                                  
# This is the function that will be tested by the autograder                                                                                                                  
# The student must update this code to properly implement the functionality                                                                                                                  
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):                                                                                                                  
                                                                                                                  
    # Read in adjusted closing prices for given symbols, date range                                                                                                                  
    dates = pd.date_range(sd, ed)                                                                                                                  
    prices_all = get_data(syms, dates)  # automatically adds SPY                                                                                                                  
    prices = prices_all[syms]  # only portfolio symbols                                                                                                                  
    prices_SPY = prices_all['SPY']
    prices_SPY_nrm = prices_SPY/prices_SPY[0]# only SPY, for comparison later                                                                                                                  
    #print(prices.ix[1:].head())                                                                                                            
    # find the allocations for the optimal portfolio                                                                                                                  
    # note that the values here ARE NOT meant to be correct for a test case                                                                                                                  
    alloc = [1.0/prices.shape[1]]*prices.shape[1]
    allocs = np.array(alloc) # add code here to find the allocations
    #print("allocs\n",allocs)
    def optimize_alloc(allocs):
        
        prices_nrm = prices.copy()
        prices_nrm = prices.iloc[0:]/prices.iloc[0]
        #print("prices_nrm\n",prices_nrm.head())
        ## find values after allocation
        allocated = prices_nrm * allocs
        #print("allocated\n",allocated.head())
        ## daily portfolio values
        port_val = allocated.sum(axis=1)
        #print("port_val\n",port_val.head())
        ## find daily returns
        daily_rets = port_val.copy()
        daily_rets[1:] = port_val[1:]/(port_val[:-1].values) - 1
        daily_rets[0] = 0
        #print("daily_rets\n",daily_rets.head())
        ## sharpe ratio
        #print("daily_mean:",daily_rets.mean())
        #print("daily_std:",daily_rets.std())
        sr = np.sqrt(252.0)*daily_rets.mean()/daily_rets.std()
        #print("Sharpe Ratio\n",sr)
        ## optimize sharpe ratio to get optimal allocs
        return -sr
    
    bounds = Bounds([0]*prices.shape[1],[1.0]*prices.shape[1])
    linear_constraint = LinearConstraint([1]*prices.shape[1],[1],[1])
    
    res = spo.minimize(optimize_alloc,allocs,method='trust-constr',bounds=bounds,constraints=linear_constraint,options = {'disp':False})
    #print("res",res['x'])
    #print("sumOfRes",res['x'].sum())
    allocs =  res['x'] #[0.2,0.2,0.2,0.2,0.2]#
    
    prices_nrm = prices.copy()
    prices_nrm = prices.iloc[0:]/prices.iloc[0]
    #print("prices_nrm\n",prices_nrm.head())
    ## find values after allocation
    allocated = prices_nrm * allocs
    #print("allocated\n",allocated.head())
    ## daily portfolio values
    port_val = allocated.sum(axis=1)
    #print("port_val\n",port_val.head())
    ## find daily returns
    daily_rets = port_val.copy()
    daily_rets[1:] = port_val[1:]/(port_val[:-1].values) - 1
    daily_rets[0] = 0
    #print("daily_rets\n",daily_rets.head())
    ## sharpe ratio
    #print("daily_mean:",daily_rets.mean())
    #print("daily_std:",daily_rets.std())
    sr = np.sqrt(252.0)*daily_rets.mean()/daily_rets.std()
    #print("Sharpe Ratio\n",sr)
    
    ## Cummulative Returns
    cr = port_val[-1]/port_val[0] - 1
    ## Average Daily return
    adr = daily_rets.mean()
    ## Volatility (stdev of daily returns)
    sddr = daily_rets.std()
    #cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats                                                                                                                  
                                                                                                                  
    # Get daily portfolio value                                                                                                                  
    #port_val = prices_SPY # add code here to compute daily portfolio values                                                                                                                  
                                                                                                                  
    # Compare daily portfolio value with SPY using a normalized plot                                                                                                                  
    if gen_plot:                                                                                                                  
        # add code to plot here  
        df_temp = pd.concat([port_val, prices_SPY_nrm], keys=['Portfolio', 'SPY'], axis=1)                                                                                                                  
        ax = df_temp.plot(figsize=(12,7.5))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.grid(b=True)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title("Daily Portfolio Value and SPY")
        plt.legend()
        plt.savefig('Figure1.png')
        #plt.show()                                                                                                                  
                                                                                                                  
    return allocs, cr, adr, sddr, sr                                                                                                                  
                                                                                                                  
def test_code():                                                                                                                  
    # This function WILL NOT be called by the auto grader                                                                                                                  
    # Do not assume that any variables defined here are available to your function/code                                                                                                                  
    # It is only here to help you set up and test your code                                                                                                                  
                                                                                                                  
    # Define input parameters                                                                                                                  
    # Note that ALL of these values will be set to different values by                                                                                                                  
    # the autograder!                                                                                                                  
                                                                                                                  
    start_date = dt.datetime(2008,6,1)                                                                                                                  
    end_date = dt.datetime(2009,6,1)                                                                                                                  
    symbols = ['GLD','X','IBM','JPM']                                                                                                                  
                                                                                                                  
    # Assess the portfolio                                                                                                                  
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)                                                                                                                  
                                                                                                                  
    # Print statistics                                                                                                                  
    print(f"Start Date: {start_date}")                                                                                                                  
    print(f"End Date: {end_date}")                                                                                                                  
    print(f"Symbols: {symbols}")                                                                                                                  
    print(f"Allocations:{allocations}")
    print(f"Sharpe Ratio: {sr}")                                                                                                                  
    print(f"Volatility (stdev of daily returns): {sddr}")                                                                                                                  
    print(f"Average Daily Return: {adr}")                                                                                                                  
    print(f"Cumulative Return: {cr}")                                                                                                                  
                                                                                                                  
if __name__ == "__main__":                                                                                                                  
    # This code WILL NOT be called by the auto grader                                                                                                                  
    # Do not assume that it will be called                                                                                                                  
    test_code()                                                                                                                  
