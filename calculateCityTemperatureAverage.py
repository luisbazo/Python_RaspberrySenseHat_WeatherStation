#by luis.bazo@gmail.com

from pymongo import MongoClient
from datetime import datetime


import sys,getopt

try:
	opts, args = getopt.getopt(sys.argv[1:],"hc:",["city="])
except getopt.GetoptError:
	print 'calculateCityTemperatureAverage.py -c city'
	print 'Example: calculateCityTemperatureAverage.py -c "Madrid,sp"' 
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print 'calculateCityTemperatureAverage.py -c city'
		print 'Example: calculateCityTemperatureAverage.py -c "Madrid,sp"' 
		sys.exit()
	elif opt in ("-c", "--city"):
		city = arg

client = MongoClient()

cursor = client.test.weather.find({"city":city})

times=0
aggr=0
for document in cursor:
	times+=1
	aggr += document["temperature"]["temp"]
temp = aggr/times

celsius = temp - 273.15
print "Averate temperature ", celsius
