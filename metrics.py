import pandas as pd
import numpy as np
from datetime import date
import yfinance as yf

#https://python.plainenglish.io/i-used-python-to-develop-investment-portfolio-performance-indicators-c52a7671d49b

# User Inputs
years = 1 # make this a user input maybe?
end_date = date.today()
start_date = date.today() - pd.DateOffset(years=years) # make this a maximum number of years
tickers = ['RPAR'] #this is a test variable

stock_data = yf.download(tickers, start_date, end_date)


#def get_benchmark(benchmark, start, end):
#    benchmark = benchmark.drop(['symbol'], axis=1)
#    benchmark.reset_index(inplace=True)
#    return benchmark


def CAGR(data):
    df = data.copy()
    df['daily_returns'] = df['Adj Close'].pct_change()
    df['cumulative_returns'] = (1 + df['daily_returns']).cumprod()
    trading_days = 252
    n = len(df)/ trading_days
    cagr = (df['cumulative_returns'][-1])**(1/n) - 1
    return cagr


def volatility(data):
    df = data.copy()
    df['daily_returns'] = df['Adj Close'].pct_change()
    trading_days = 252
    vol = df['daily_returns'].std() * np.sqrt(trading_days)
    return vol


def sharpe_ratio(data, rf):
    df = data.copy()
    sharpe = (CAGR(df) - rf)/ volatility(df)
    return sharpe


def sortino_ratio(data, rf):
    df = data.copy()
    df['daily_returns'] = df['Adj Close'].pct_change()
    df["negative_returns"] = np.where(df["daily_returns"]<0,df["daily_returns"],0)
    negative_volatility = df['negative_returns'].std() * np.sqrt(252)
    sortino = (CAGR(df) - rf)/ negative_volatility
    return sortino


def maximum_drawdown(data):
    df = data.copy()
    df['daily_returns'] = df['Adj Close'].pct_change()
    df['cumulative_returns'] =  (1 + df['daily_returns']).cumprod()
    df['cumulative_max'] = df['cumulative_returns'].cummax()
    df['drawdown'] = df['cumulative_max'] - df['cumulative_returns']
    df['drawdown_pct'] = df['drawdown'] / df['cumulative_max']
    max_dd = df['drawdown_pct'].max()
    return max_dd


def calmar_ratio(data, rf):
    df = data.copy()
    calmar = (CAGR(df) - rf) / maximum_drawdown(data)
    return calmar

print("CAGR: " + str(CAGR(stock_data) * 100) + "%")
print("Annualized Volatility: " + str(volatility(stock_data) * 100) + "%")
print("Sharpe Ratio: " + str(sharpe_ratio(stock_data, 0.03)))
print("Sortino Ratio: " + str(sortino_ratio(stock_data, 0.03)))
print("Maximum Drawdown: " + str(maximum_drawdown(stock_data) * 100) + "%")
print("Calmar Ratio: " + str(calmar_ratio(stock_data, 0.03)))
