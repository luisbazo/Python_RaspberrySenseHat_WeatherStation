#by luis.bazo@gmail.com

from pymongo import MongoClient
from datetime import datetime


import sys,getopt

try:
	opts, args = getopt.getopt(sys.argv[1:],"hc:",["city="])
except getopt.GetoptError:
	print 'resetCityWeather.py -c city'
	print 'Example: resetCityWeather.py -c "Madrid,sp"' 
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print 'resetCityWeather.py -c city'
		print 'Example: resetCityWeather.py -c "Madrid,sp"'  
		sys.exit()
	elif opt in ("-c", "--city"):
		city = arg

client = MongoClient()

result = client.test.weather.delete_many({"city":city})
