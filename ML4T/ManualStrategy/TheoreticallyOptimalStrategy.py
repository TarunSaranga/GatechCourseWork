
"""
@author: Tharun Saranga
"""

import pandas as pd
import numpy as np
import datetime as dt
import util as ut
import matplotlib.pyplot as plt
from marketsimcode import *

def testPolicy(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000):
    
    dates = pd.date_range(sd,ed)
    df_prices = ut.get_data([symbol],dates)
    prices = df_prices[symbol]
    #prices = prices#/prices[0]
    #prices.plot()
    temp1 = pd.DataFrame()
    temp2 = pd.DataFrame()
    df = pd.DataFrame()
    temp1['Order'] = prices > prices.shift(-1)
    
    temp1['Order'].replace(True,'SELL',inplace=True)
    temp1['Order'].replace(False,'BUY',inplace=True)
    
    temp2['Order'] = temp1['Order'].shift(1)
    #print(temp1['Order'])
    #print(temp2['Order'])
    temp2['Order'].replace('BUY','tmp',inplace=True)
    temp2['Order'].replace('SELL','BUY',inplace=True)
    temp2['Order'].replace('tmp','SELL',inplace=True)

    df[symbol] = temp1['Order'].append(temp2['Order']).dropna()
    
    df.sort_index(inplace=True)
    df[symbol].replace("BUY",1000,inplace=True)
    df[symbol].replace("SELL",-1000,inplace=True)
    
    #prices.plot()
    #temp1.plot()
    #print(df)
    
    return df

def author():
    return "tsaranga3"

def plot_graph():
    
    order_df = testPolicy()
    #print(order_df.tail(1))
    portvals = compute_portvals(order_df)
    #print(portvals)
    cum_ret=(portvals[-1]/portvals[0])-1
    daily_ret=(portvals/portvals.shift(1))-1
    avg_daily_ret=daily_ret.mean()
    std_daily_ret=daily_ret.std()

    # Compare portfolio against $SPX  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of Fund: {cum_ret}")
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of Fund: {std_daily_ret}")
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()
    bench_order = order_df.copy().head(1)
    bench_order = bench_order.append(order_df.copy().tail(1))
    bench_order.iloc[0] = 1000
    bench_order.iloc[1:] = 0
    
    bench_portvals = compute_portvals(bench_order)
    #print(bench_portvals)
    cum_ret=(bench_portvals[-1]/bench_portvals[0])-1
    daily_ret=(bench_portvals/bench_portvals.shift(1))-1
    avg_daily_ret=daily_ret.mean()
    std_daily_ret=daily_ret.std()
    print("------------------------------------------------------------------")
    print()
    # Compare portfolio against $SPX  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of Fund: {cum_ret}")
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of Fund: {std_daily_ret}")
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()
    
    portvals_nrm = portvals/portvals[0]
    #portvals_nrm=portvals_nrm.values
    bench_portvals_nrm = bench_portvals/bench_portvals[0]
    #bench_portvals_nrm = bench_portvals_nrm.values
    plt.figure(figsize=[15,8])
    portvals_nrm.plot(label="Optimal Portfolio",color="red")
    bench_portvals_nrm.plot(label="Benchmark Portfolio",color="green")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio value")
    plt.title("Optimal Portfolio vs Benchmark")
    plt.savefig("OptimalStrategy.png")
    




if __name__ == "__main__":
    #testPolicy()
    plot_graph()
    