"""
Student Name: Tharun Saranga
GT User ID: tsaranga3
GT ID: 903457046
"""
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from StrategyLearner import StrategyLearner
from marketsimcode import compute_portvals

def author():
    return 'tsaranga3'


def experiment2_plot(impact = 0.0, symbol="JPM"):

    st = StrategyLearner(impact=impact)

    st.addEvidence(symbol=symbol,sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    trades = st.testPolicy(symbol=symbol,sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)

    portvals = compute_portvals(trades,symbol=symbol,impact=impact)
    nrm_portvals = portvals/portvals[0]

    cum_ret=(portvals[-1]/portvals[0])-1
    daily_ret=(portvals/portvals.shift(1))-1
    avg_daily_ret=daily_ret.mean()
    std_daily_ret=daily_ret.std()
    sharpe_ratio=np.sqrt(252)*(daily_ret).mean()/std_daily_ret

    # Portfolio details
    print("~~~~~~~~~~~~~~~~~~~~~~impact="+str(impact)+"~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    print(f"Cumulative Return of Strategy: {cum_ret}")
    print()
    print(f"Standard Deviation of Strategy: {std_daily_ret}")
    print()
    print(f"Average Daily Return of Strategy: {avg_daily_ret}")
    print()
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    print()

    nrm_portvals.plot(label=str(impact))


if __name__ == "__main__":
#    print("~~~~~~~~~~~~~~insample_data~~~~~~~~~~~~~~")
#    print()
    plt.figure(figsize=(12,8))
    experiment2_plot(impact=0.001)
    experiment2_plot(impact=0.005)
    experiment2_plot(impact=0.01)
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Returns")
    plt.legend(title="Impact:")
    plt.title("Effect of Impact Value on insample test")
    plt.savefig("experiment2.png")