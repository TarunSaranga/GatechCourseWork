
"""
@author: Tharun Saranga
"""
import pandas as pd
import numpy as np
import datetime as dt
import util as ut
import matplotlib.pyplot as plt
from indicators import *
from marketsimcode import *

def testPolicy(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000):

    dates = pd.date_range(sd,ed)
    df_prices = ut.get_data([symbol],dates)
    prices = df_prices[symbol]

    ## MACD
    tsi_ = tsi(df_prices,sym=symbol)
    tsi_5 = tsi_.shift(2)
    t = tsi_ - tsi_5

    macd_ = macd(df_prices,sym=symbol)
    macd_5 = macd_.shift(2)
    m = macd_ - macd_5
    #print(m)
    ## SMA
    s = sma(df_prices,sym=symbol)

    ## Bollinger Bands
    upper,lower = bollinger(df_prices, sym=symbol)

    orders = []
    #orders.append([str(sd),0])
    #print(orders)
    holdings = 0
    for idx,price in prices.iteritems():
        if(holdings <=0):
            if(m.loc[idx]<0 and t.loc[idx]<0 and prices.loc[idx] < s.loc[idx] and prices.loc[idx] < lower.loc[idx] ):
                #print(idx,"BUY")
                holdings += 1000
                orders.append([idx,1000])
            else:
                orders.append([idx,0])
        elif(holdings >=0):
            if(m.loc[idx]>0 and t.loc[idx]>0 and prices.loc[idx] > s.loc[idx] and prices.loc[idx] > upper.loc[idx] ):
                #print(idx,"SELL")
                holdings -= 1000
                orders.append([idx,-1000])
            else:
                orders.append([idx,0])
        else:
            orders.append([idx,0])

    #orders.append([str(ed),0])
    orders = pd.DataFrame(orders,columns=["Date",symbol])
    orders = orders.set_index("Date")
    #print(orders)
    return orders

def plot_graph(sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),title="Manual Strategy vs Benchmark (insample data)"):

    order_df = testPolicy(sd=sd,ed=ed)
    #print(order_df.tail(1))
    portvals = compute_portvals(order_df)
    #print(portvals)
    cum_ret=(portvals[-1]/portvals[0])-1
    daily_ret=(portvals/portvals.shift(1))-1
    avg_daily_ret=daily_ret.mean()
    std_daily_ret=daily_ret.std()

    # Compare portfolio against $SPX
    print(f"Cumulative Return of Strategy: {cum_ret}")
    print()
    print(f"Standard Deviation of Strategy: {std_daily_ret}")
    print()
    print(f"Average Daily Return of Strategy: {avg_daily_ret}")
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

    print("-------------------------------------------------")
    print()
    print(f"Cumulative Return of Benchmark: {cum_ret}")
    print()
    print(f"Standard Deviation of Benchmark: {std_daily_ret}")
    print()
    print(f"Average Daily Return of Benchmark: {avg_daily_ret}")
    print()

    portvals_nrm = portvals/portvals[0]
    #portvals_nrm=portvals_nrm.values
    bench_portvals_nrm = bench_portvals/bench_portvals[0]
    #bench_portvals_nrm = bench_portvals_nrm.values
    plt.figure(figsize=[15,8])
    portvals_nrm.plot(label="Manual Strategy Portfolio",color="red")
    for idx,order in order_df.iterrows():
        if(order[0]>0):
            plt.axvline(x=idx,color="blue")
        if(order[0]<0):
            plt.axvline(x=idx,color="black")
    bench_portvals_nrm.plot(label="Benchmark Portfolio",color="green")
    plt.legend(loc="upper right")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio value")
    plt.xlim([sd,ed])
    #plt.ylim([0.65,1.5])
    plt.title(title)
    if(title=="Manual Strategy vs Benchmark (outsample data)"):
        plt.savefig("ManualStrategy_outsample.png")
    else:
        plt.savefig("ManualStrategy_insample.png")


def outsample_data(symbol="JPM",start_date=dt.datetime(2010,1,1),end_date=dt.datetime(2011,12,31)):

    plot_graph(sd=start_date,ed=end_date,title="Manual Strategy vs Benchmark (outsample data)")

def author():
    return "tsaranga3"

if __name__ == "__main__":
    print("~~~~~~~~~~~~~~insample_data~~~~~~~~~~~~~~")
    print()
    plot_graph()
    print("##################################################")
    print()
    print("~~~~~~~~~~~~~~outsample data~~~~~~~~~~~~~~")
    print()
    outsample_data()