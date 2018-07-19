#So this was basically a test to create a table of percent discrepancies in price information between CoinAPI and CoinMarketCap API
#We ended up finding about 32.5% of coins had a discrepancy over 10%

import os
import sys
import json
import requests
import tempfile
import csv

# Get request from coinAPI
url = 'https://rest.coinapi.io/v1/exchangerate/USD'
headers = {'X-CoinAPI-Key' : ''} #Get your own coinAPI api key
response2 = requests.get(url, headers=headers)
print(response2.status_code)
#Turn it into a json
data2 = response2.json()
#From the json I'm obtaining a list of dictionaries containing coin symbols and their prices
capicomp = data2['rates']
#Create a csv file of two columns
download_dir = "fullCoinDiscrepancy.csv"
csv = open(download_dir, "w") 
columnTitleRow = "Coin, Percent Discrepancy\n"
csv.write(columnTitleRow)
#CoinMarketCap only allows 100 coins per pull of tickers so we iterated to get 1600 coins
parse = [1, 101, 201, 301, 401, 501, 601, 701, 801, 901, 1001, 1101, 1201, 1301, 1401, 1501]
for x in parse:
	#Get the request from CoinMarketCap in array structure for 100 coins
	response = requests.get("https://api.coinmarketcap.com/v2/ticker/?start=" + str(x) + "&limit=" + str(x+99) + "&structure=array")
	print(response.status_code)
	#Turn that response into a json
	cmc = response.json()
	#Iterate through that 100 coins
	for dics in cmc["data"]:
		pcdif = 0 #percent difference
		#to get all of the values out of a dictionary
		symb = dics["symbol"] #symbol
		usd = dics["quotes"]
		into  = usd["USD"]
		cmprice = into["price"] #price from coin market cap
		compare = 0
		#Iterate through the coinAPI dictionaries
		for z in capicomp:
			#Check if the coin is there
			if z["asset_id_quote"] == symb:
				compare = 1/z["rate"] #we pulled exchange rate of everything for 1 dollar so this is how we get the price of everything
				capicomp.remove(z) #this is an efficiency thing. In order to prevent going through a massive array we remove
				break
		#compare will not change from 0 if the coin is not found in CoinAPI and then it will not be added
		if compare != 0:
			pcdif = (abs(cmprice - compare)/cmprice)*100
			csv.write(symb + "," + str(pcdif) + "%\n" )
