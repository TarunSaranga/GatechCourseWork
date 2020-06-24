# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 21:52:07 2019

@author: Tharun Saranga
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(order, start_val = 100000, commission=0, impact=0, symbol ="JPM"):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    #order = order.sort_index()
    #print(order.head(5))
    sym = symbol
    #print(sym)
    start_date = order.index.values[0]
    end_date = order.index.values[-1]
    date_range = pd.date_range(start_date, end_date)

    prices = get_data([sym],date_range)
    #prices = prices[sym]
    #print(prices.head())
    prices['Cash'] = 1.00
    #print(prices.head())

    trade = pd.DataFrame(index = prices.index, columns = prices.columns)
    trade = trade.fillna(0)
    trade['Cash'].iloc[0] = start_val
    #print(order)

    #order = orders_df.iloc[0]
    #print(order)
    for idx, row in order.iterrows():
        order_price = prices[sym].loc[idx]
        order_units = row[0]
        trade.loc[idx,sym] += order_units
        trade.loc[idx,"Cash"] += order_units*order_price*-1
        trade.loc[idx,"Cash"] -= commission
        share_impact = abs(order_units)*order_price*impact
        trade.loc[idx,"Cash"] -= share_impact

    #print(trade)

    for i in range(1,trade.shape[0]):
        for j in range(0,trade.shape[1]):
            trade.iloc[i,j] += trade.iloc[i-1,j]

    portvals = prices * trade
    portvals = portvals.sum(axis=1)
    return portvals

def author():
    return 'tsaranga3'


if __name__=="__main__":
    print()