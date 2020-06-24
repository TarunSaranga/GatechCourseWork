
"""
@author: Tharun Saranga
"""

import pandas as pd
import matplotlib.pyplot as plt
import util as ut
import numpy as np
import datetime as dt

def sma(df,sym="JPM"):
    ## simple moving average
    prices = df[sym]
    
    sma = prices.rolling(window=14,center=False).mean()
    
    return sma

def bollinger(df,sym="JPM"):
    
    prices = df[sym]
    
    rm = prices.rolling(window=14,center=False).mean()
    sd = prices.rolling(window=14,center=False).std()
    upper_band = rm + (2*sd)
    lower_band = rm - (2*sd)
    
    return upper_band,lower_band


def macd(df,sym="JPM"):
    ## 12-period EMA - 26 period EMA
    prices = df[sym]
    #prices = prices/prices[0]
    ema12 = prices.ewm(span=12).mean()
    #ema12s = ema12/ema12[0] - 1
    ema26 = prices.ewm(span=26).mean()
    #ema26s = ema26/ema26[0] - 1
    
    return ema12-ema26

def stoch(df,sym="JPM"):
    ## (price - lowestin14)/(highestin14-lowestin14) x 100
    prices = df[sym]
    
    stoch  = 100.0 * (prices - prices.rolling(window=14).min())/(prices.rolling(window=14).max()-prices.rolling(window=14).min())
    
    return stoch

def tsi(df,sym="JPM"):
    
    prices = df[sym]
    m = (prices - prices.shift(1)).fillna(method="ffill")
    r = 25
    s = 13
    
    n1 = m.ewm(span=r).mean()
    
    n2 = n1.ewm(span=s).mean()
    #m_abs = pd.DataFrame(m.abs())
    #print(type(n1.head()))
    d1 = m.abs().ewm(span=r).mean()
    d2 = d1.ewm(span=s).mean()
    
    tsi = n2/d2 * 100
    #print(tsi)
    #print(tsi.head())
    return tsi

def author():
    
    return "tsaranga3"
    

def insample_data(symbol="JPM",start_date=dt.datetime(2008,1,1),end_date=dt.datetime(2009,12,31)):
    
    dates = pd.date_range(start_date,end_date)
    
    prices = ut.get_data([symbol],dates)
    
    return prices

def outsample_data(symbol="JPM",start_date=dt.datetime(2010,1,1),end_date=dt.datetime(2011,12,31)):
    
    dates = pd.date_range(start_date,end_date)
    
    prices = ut.get_data([symbol],dates)
    
    return prices
    
def plot_sma(df,sym="JPM"):
    plt.figure(figsize=[15,8])
    df[sym].plot(label="JPM Price")
    s = sma(df)
    s.plot(label="SMA")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Simple Moving Average of Period 14")
    plt.legend()
    plt.savefig("SMA.png")

def plot_bollinger(df,sym="JPM"):
    plt.figure(figsize=[15,8])
    df[sym].plot(label="JPM Price")
    upper, lower = bollinger(df)
    s = sma(df)
    upper.plot(label="Upper Bollinger Band",style=["--"],color="red")
    lower.plot(label="Lower Bollinger Band",style=["--"],color="green")
    s.plot(label="SMA",color="orange")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Bollinger Bands of Period 14")
    plt.legend()
    plt.savefig("bollinger.png")

def plot_macd(df,sym="JPM"):
    plt.figure(figsize=[15,8])
    df[sym].plot(label="JPM Price")
    m = macd(df)
    #macd12.plot(label="macd12")
    #macd26.plot(label="macd26")
    m.plot(label="macd")
    plt.axhline(y=0,linestyle="--",color="grey")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("MACD ")
    plt.legend()
    plt.savefig("macd.png")

def plot_stoch(df,sym="JPM",factor = 5):
    plt.figure(figsize=[15,8])
    df[sym].plot(label="JPM Price")
    s = factor*stoch(df)/100
    s.plot(label="stochastic")
    plt.axhline(y=0,linestyle="--",color="grey")
    plt.axhline(y=factor,linestyle="--",color="grey")
    plt.axhline(y=factor*0.3,linestyle="--",color="Red")
    plt.axhline(y=factor*0.7,linestyle="--",color="Green")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Stochastic of Period 14")
    plt.legend()
    
def plot_tsi(df,sym="JPM",factor = 5):
    plt.figure(figsize=[15,8])
    df[sym].plot(label="JPM Price")
    t = factor*tsi(df)/100
    t.plot(label="tsi")
    plt.axhline(y=0,linestyle="--",color="grey")
    plt.axhline(y=factor,linestyle="--",color="grey")
    plt.axhline(y=-factor,linestyle="--",color="grey")
    plt.axhline(y=factor*0.25,linestyle="--",color="Red")
    plt.axhline(y=-0.25*factor,linestyle="--",color="Green")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("True Strength Index")
    plt.legend()
    plt.savefig("tsi.png")

if __name__ == "__main__":
    print("Main Program")
    insample_prices = insample_data()  
    plot_sma(insample_prices)
    plot_bollinger(insample_prices)
    plot_macd(insample_prices)
    plot_tsi(insample_prices)
    #plot_stoch(insample_prices)
    #print(insample_prices["JPM"]/insample_prices["JPM"][0])
