from flask import Flask, request, render_template, jsonify
import pymongo
from bson import json_util
import pandas as pd
import pandas_datareader as pdr
from pandas_datareader import data
import json
from datetime import date, timedelta
import yfinance as yf
import requests
import time
import plotly.graph_objects as go

app=Flask(__name__)

#Import data from MongoDB
myclient = pymongo.MongoClient("mongodb+srv://Hoanglong_Pham:Long1989@cluster0.j3atpvd.mongodb.net/?retryWrites=true&w=majority")

# # Add the meta data into stock price information
# def meta_data(info, symbol):
#     company = yf.Ticker(symbol)       
#     meta = {'Meta data':{},'Time Series': {}}
#     meta['Meta data'] = company.info
#     meta['Time Series'] = info
#     return meta

# #Generate price information for specific stock based on symbol and specificed day range
# def stock_info(symbol, day_range):
#     from pandas_datareader import data
#     end_date = date.today()
#     if day_range == 'today':
#         start_date = end_date
#     elif day_range == '1 week':
#         start_date = end_date - timedelta(days=7)
#     elif day_range == '1 month':
#         start_date = end_date - timedelta(days=30)
#     elif day_range == '1 year':
#         start_date = end_date - timedelta(days=365)
#     elif day_range == '5 year':
#         start_date = end_date - timedelta(days=1825)
#     elif day_range == '10 year':
#         start_date = end_date - timedelta(days=3650)
#     elif day_range == 'All':
#         start_date = '2010-01-01'
#     data_source='yahoo'
#     df_stock = data.DataReader(symbol, data_source, start_date, end_date)
#     df_stock = df_stock.iloc[:,[1, 2, 3, 0, 4, 5]]
#     df_stock = df_stock.to_json()
#     info = json.loads(df_stock)
#     return info

# #Generate complete information of each stock
# def history_price(symbol):
#     info = stock_info(symbol, 'All')
#     meta = meta_data(info, symbol)
#     return meta

# #Generate complete informtion stock price for today date
# def today_stock():
#     today_stock = {}
#     for symbol in exchange_list:
#         info = stock_info(symbol, 'today')
#         today_stock[symbol] = info
#     return today_stock
    
# while True:
#     #Generate the list of stocks in Dow Jones exchange market:
#     dowjones_link = 'https://www.slickcharts.com/dowjones'
#     r1 = requests.get(dowjones_link, headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
#     dj_data = pd.read_html(r1.text)[0]
#     df1 = pd.DataFrame(dj_data)
#     df1 = df1.to_json(date_format = 'iso', orient='index')
#     dowjones = json.loads(df1)
#     dowjones_list=[]
#     for stock in dowjones:
#         dowjones_list.append(dowjones[stock]['Symbol'])

#     #Generate the list of stocks in Nasdaq 100 exchange market:
#     nasdaq_link = 'https://www.slickcharts.com/nasdaq100'
#     r2 = requests.get(nasdaq_link, headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
#     nd_data = pd.read_html(r2.text)[0]
#     df2 = pd.DataFrame(nd_data)
#     df2 = df2.to_json(date_format = 'iso', orient='index')
#     nasdaq = json.loads(df2)
#     nasdaq_list=[]
#     for stock in nasdaq:
#         nasdaq_list.append(nasdaq[stock]['Symbol'])
        
#     #Combine two lists together
#     exchange_list = nasdaq_list
#     for stock in dowjones_list:
#         if stock not in exchange_list:
#             exchange_list.append(stock)
#     exchang_list = exchange_list.extend(['%5ENDX','%5EDJI'])
#     exchange_list.sort()
        
#     #Upload information of stocks into MongoDB
#     myclient = pymongo.MongoClient("mongodb+srv://Hoanglong_Pham:Long1989@cluster0.j3atpvd.mongodb.net/?retryWrites=true&w=majority")
#     mydb = myclient["StockMarket"]
#     collist = mydb.list_collection_names()
#     i = 1
#     for symbol in exchange_list:
#         mycol = mydb[symbol]
#         value = history_price(symbol)
#         if symbol in collist:
#             mycol.drop()
#             mycol.insert_one(value)
#             print(str(i) + 'The collection ' + symbol + ' is updated')
#         else:
#             mycol.insert_one(value)
#             print(str(i) + 'The collection '+ symbol + ' is not here')
#             i +=1
#     time.sleep(86400)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/history')
def display_data():
  symbol = request.args.get('symbol', default="AMZN")
  period = request.args.get('period', default=360)
  mydb = myclient['StockMarket']
  mycol = mydb[symbol]
  mydoc = mycol.find_one({})
  data_display = mydoc['Time Series']
  df = pd.DataFrame(data_display).T.iloc[:, ::-1]
  data = df.iloc[0:3,0:period].iloc[:, ::-1].T.to_json(date_format ='iso')
  return data

@app.route("/quote")
def display_info():
  symbol = request.args.get('symbol', default="AMZN")
  mydb = myclient['StockMarket']
  mycol = mydb[symbol]
  mydoc = mycol.find_one({})
  quote = mydoc['Meta data']
  return jsonify(quote)

@app.route("/chart")
def chart():
    return render_template("chart.html")

@app.route('/user/<name>')
def user(name):
  mydb = myclient['StockMarket']
  collist = mydb.list_collection_names()
  if name in collist:
    noti = format(name) + ' exists'
  else:
    noti = format(name) + ' does not exist'
  return noti

@app.route('/team')
def OurTeam():
	return render_template('OurTeam.html')

if __name__ == "__main__":
  app.run()