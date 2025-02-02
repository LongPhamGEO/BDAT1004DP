from flask import Flask, request, render_template, jsonify
import pymongo
from bson import json_util
import pandas as pd

import json
from datetime import date, timedelta

import requests
import time


app=Flask(__name__)

#Import data from MongoDB
myclient = pymongo.MongoClient("mongodb+srv://Hoanglong_Pham:Long1989@cluster0.j3atpvd.mongodb.net/?retryWrites=true&w=majority")



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