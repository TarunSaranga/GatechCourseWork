# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 00:49:57 2019

@author: Tharun Saranga
"""

"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch

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

Student Name: Tharun Saranga (replace with your name)
GT User ID: tsaranga3 (replace with your User ID)
GT ID: 903457046 (replace with your GT ID)
"""

import RTLearner as rt
import BagLearner as bl
import datetime as dt
import pandas as pd
import util as ut
from indicators import *
from marketsimcode import *
import matplotlib.pyplot as plt

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        pd.options.mode.chained_assignment = None
        self.learner = bl.BagLearner(learner = rt.RTLearner, \
                                     kwargs = {"leaf_size":5}, \
                                     bags = 200, \
                                     boost = False, \
                                     verbose = False)

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        # add your code to do learning here

        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        #prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        #if self.verbose: print(prices)

        #print(trainY)
        trainX, trainY = self.create_trainXY(prices.copy(),symbol=symbol)
        self.learner.addEvidence(trainX, trainY)

        return trainY


    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "JPM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        trades = prices_all[[symbol,]]  # only portfolio symbols
        testX = self.create_testX(trades.copy(),symbol=symbol)
        #trainX,trainY = self.create_trainXY(trades.copy())
        #print(trades)
        #print(testX)
        #prices = testX.copy()
        trades = pd.DataFrame(testX[symbol])
        trades.columns = [symbol]
        trades[symbol] = 0
        position = 0
        y_pred = self.learner.query(testX.values)
        #print(y_pred)
        for i in range(len(y_pred)):
             ## Long Position
            if(y_pred[i] >= 0.5 and position == 0): ## Buy when no stocks
                trades.iloc[i] = +1000
                position = 1
            elif(y_pred[i] >=0.5 and position == 1): ## Hold when stocks and price increasing
                trades.iloc[i] = 0
            elif(y_pred[i] < 0.5 and position == 1):
                trades.iloc[i] = -1000
                position = 0

            ## Short position
            elif(y_pred[i] < 0.5 and position == 0):
                trades.iloc[i] = -1000
                position = -1
            elif(y_pred[i] < 0.5 and position == -1):
                trades.iloc[i] = 0
            elif(y_pred[i] >= 0.5 and position == -1):
                trades.iloc[i] = +1000
                position = 0
#            print("y_pred: ",y_pred[i])
#            print("trade:",trades)
#            print("position:")
        orders = trades.copy()
#        trades = trades.replace(0,np.nan)
#        buy_sig = prices * trades.replace(1000,1).replace(-1000,np.NaN)
#        #print(buy_sig)
#        sell_sig = prices * trades.replace(-1000,1).replace(1000,np.nan)
#
#        fig, ax = plt.subplots(figsize=(20,12))
#        prices.plot(ax=ax)
#        buy_sig.plot(ax=ax, style="*",label='buy')
#        sell_sig.plot(ax=ax, style="*",label='sell')
        return y_pred

    def author(self):
        return 'tsaranga3'

    def create_trainXY(self,prices,symbol='JPM'):
        peek_future = 1
        s = sma(prices,sym=symbol)
        prices["macd"] = macd(prices,sym=symbol)
        up,low = bollinger(prices,sym=symbol)
        prices["bb"] = (up-low)/s
        prices["tsi"] = tsi(prices,sym=symbol)
        prices["next_price"] = prices[symbol].shift(-peek_future)
        prices = prices.dropna()#.fillna(method='bfill').fillna(method='ffill')
        #print(prices)
        prices['label'] = prices["next_price"] > (prices[symbol] + prices[symbol]*self.impact)
        prices['label'] = prices['label'].replace(True,1).replace(False,0)
        #print(prices)
        prices = prices.drop("next_price",axis=1)
        #prices.drop(symbol,axis=1,inplace=True)
        #print(prices)
        trainX = prices.drop('label',axis=1).values
        #print(trainX)
        trainY = prices['label'].values
        return trainX, trainY

    def create_testX(self,prices,symbol='JPM'):
        s = sma(prices,sym=symbol)
        prices["macd"] = macd(prices,sym=symbol)
        up,low = bollinger(prices,sym=symbol)
        prices["bb"] = (up-low)/s
        prices["tsi"] = tsi(prices,sym=symbol)
        prices = prices.dropna()#.fillna(method='bfill').fillna(method='ffill')
        #print(prices)
        testX = prices#.values

        return testX


if __name__=="__main__":
    print("One does not simply think up a strategy")
    symbol = "JPM"
    st = StrategyLearner()
    trainY = st.addEvidence(symbol=symbol,sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    predY = st.testPolicy(symbol=symbol,sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
#    #print(trades)
#    #trades1 = st.testPolicy(symbol="JPM",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
#    bench_trades = trades.copy()
#    bench_trades.loc[:] = 0
#    bench_trades.iloc[0] = +1000
#    portvals = compute_portvals(trades,symbol=symbol)
#    nrm_portvals = portvals/portvals[0]
#    #portvals1 = compute_portvals(trades1)
#    #nrm_portvals1 = portvals1/portvals1[0]
#    bench_portvals = compute_portvals(bench_trades,symbol=symbol)
#    nrm_bench_portvals = bench_portvals/bench_portvals[0]
#    plt.figure(figsize=(20,12))
#    nrm_portvals.plot(label='Strategy')
#    #nrm_portvals1.plot()
#    nrm_bench_portvals.plot(label='Benchmark')
#    plt.legend()
