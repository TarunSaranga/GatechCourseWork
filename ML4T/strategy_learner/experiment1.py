"""
Student Name: Tharun Saranga
GT User ID: tsaranga3
GT ID: 903457046
"""
import pandas as pd
import numpy as np
import util as ut
from StrategyLearner import StrategyLearner
from ManualStrategy import testPolicy
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
import datetime as dt



def author():
    return 'tsaranga3'

def plot_graphs(sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),title="Strategy Learner vs Manual Strategy vs Benchmark (insample data)",symbol = 'JPM'):

    order_df = testPolicy(sd=sd,ed=ed,symbol=symbol)
    portvals = compute_portvals(order_df,symbol=symbol)
    cum_ret=(portvals[-1]/portvals[0])-1
    daily_ret=(portvals/portvals.shift(1))-1
    avg_daily_ret=daily_ret.mean()
    std_daily_ret=daily_ret.std()
    sharpe_ratio=np.sqrt(252)*(daily_ret).mean()/std_daily_ret

    # Portfolio details
    print(f"Cumulative Return of Manual Strategy: {cum_ret}")
    print()
    print(f"Standard Deviation of Manual Strategy: {std_daily_ret}")
    print()
    print(f"Average Daily Return of Strategy: {avg_daily_ret}")
    print()
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    print()

    bench_order = order_df.copy().head(1)
    bench_order = bench_order.append(order_df.copy().tail(1))
    bench_order.iloc[0] = 1000
    bench_order.iloc[1:] = 0

    bench_portvals = compute_portvals(bench_order,symbol=symbol)
    #print(bench_portvals)
    cum_ret=(bench_portvals[-1]/bench_portvals[0])-1
    daily_ret=(bench_portvals/bench_portvals.shift(1))-1
    avg_daily_ret=daily_ret.mean()
    std_daily_ret=daily_ret.std()
    sharpe_ratio=np.sqrt(252)*(daily_ret).mean()/std_daily_ret

    # Portfolio details
    print("-------------------------------------------------")
    print()
    print(f"Cumulative Return of Benchmark: {cum_ret}")
    print()
    print(f"Standard Deviation of Benchmark: {std_daily_ret}")
    print()
    print(f"Average Daily Return of Benchmark: {avg_daily_ret}")
    print()
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    print()

    st = StrategyLearner()
    st.addEvidence(symbol=symbol,sd=sd,ed=ed,sv=100000)
    trades = st.testPolicy(symbol=symbol,sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    strategy_portvals = compute_portvals(trades,symbol=symbol)

    cum_ret=(strategy_portvals[-1]/strategy_portvals[0])-1
    daily_ret=(strategy_portvals/strategy_portvals.shift(1))-1
    avg_daily_ret=daily_ret.mean()
    std_daily_ret=daily_ret.std()
    sharpe_ratio=np.sqrt(252)*(daily_ret).mean()/std_daily_ret

    # Portfolio details
    print("-------------------------------------------------")
    print()
    print(f"Cumulative Return of Strategy Learner: {cum_ret}")
    print()
    print(f"Standard Deviation of Strategy Learner: {std_daily_ret}")
    print()
    print(f"Average Daily Return of Strategy Learner: {avg_daily_ret}")
    print()
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    print()

    portvals_nrm = portvals/portvals[0]
    bench_portvals_nrm = bench_portvals/bench_portvals[0]
    strategy_portvals_nrm = strategy_portvals/strategy_portvals[0]

    plt.figure(figsize=[12,8])
    strategy_portvals_nrm.plot(label="Strategy Learner Portfolio",color="blue")
    portvals_nrm.plot(label="Manual Strategy Portfolio",color="red")
    bench_portvals_nrm.plot(label="Benchmark Portfolio",color="green")
    plt.legend(loc="upper left")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio value")
    plt.xlim([sd,ed])
    #plt.ylim([0.65,1.5])
    plt.title(title)
    plt.savefig("experiment1.png")


if __name__ == "__main__":
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~insample_data~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    plot_graphs()

