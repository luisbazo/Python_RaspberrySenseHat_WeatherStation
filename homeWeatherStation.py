#by luis.bazo@gmail.com

from sense_hat import SenseHat
import pyowm
import json
from pymongo import MongoClient
from datetime import datetime
import sys,getopt
import threading
import time
import urllib2

red = (255, 0, 0)
green = (0, 255,0)
blue = (0,0,255)
black = (0,0,0)
saveData = False


def getWeatherDataForCity(city,offset,lockscreen,isLocal,display):
	print "Gathering weather data for city of ", city, " every ", offset, " seconds"
	# Search for current weather in London (UK)
	while (True):
		observation = owm.weather_at_place(city)
		w = observation.get_weather()

		#Add city to JSON weather
		jsonweather = w.to_JSON()
		#print jsonweather
		jsonloads = json.loads(jsonweather)
		jsonloads['city']=city

		if(isLocal):
			local_temp = sense.get_temperature();
			local_temp = celciusToKelvin(local_temp)
			jsonloads['city']='Home'
			jsonloads['temperature']['temp']=local_temp

		if(display):
			lockscreen.acquire()
			displayCityWeatherOnSenseHatDisplay(jsonloads)
			lockscreen.release()
		if(saveData):
			client.test.weather.insert_one(jsonloads)
		time.sleep(offset)

def displayCityWeatherOnSenseHatDisplay(jsonloads):

	#Display temp message out to the screen
	tcelsius = int(kelvinToCelsius(jsonloads['temperature']['temp']))
	tcelsius = str(tcelsius) + "C"

	#I like home to be blue :-)
	if (str(jsonloads['city']) == "Home"):colour = blue
	else:colour = red

	sense.clear()
	for i in range(1):
		sense.show_message(str(jsonloads['city']), 0.05 , colour, black)
		sense.show_message(str(jsonloads['status']), 0.05, colour, black)
		sense.show_message(str(tcelsius), 0.08 , colour, black)


#Utilities
def celciusToKelvin(t):
	t = t + 273.15
	return t
def kelvinToCelsius(t):
	t = t - 273.15
	return t
def getLocalCity():
	# Automatically geolocate the connecting IP
	f = urllib2.urlopen('http://freegeoip.net/json/')
	json_string = f.read()
	f.close()
	location = json.loads(json_string)
	location_city = location['city']
	location_state = location['region_name']
	location_country = location['country_name']
	location_zip = location['zip_code']
	location_countrycode = location['country_code']
	loc = location_state + "," + location_countrycode
	return str(loc)

try:
	opts, args = getopt.getopt(sys.argv[1:],"hc:o:a:s:",["cities=,times=,offset=,api=,saveData="])
except getopt.GetoptError:
	print 'homeWeatherStation.py -c city1|city2 -o 5 -a xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -s y'
	print 'Example: homeWeatherStation.py -c "London,uk|Madrid,sp" -t 100 -o 5 -a xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -s y'
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print 'homeWeatherStation.py -c city1|city2 -o 5 -a xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -s y'
		print 'Example: homeWeatherStation.py -c "London,uk|Madrid,sp" -t 100 -o 5 -a xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -s y'
		sys.exit()
	elif opt in ("-c", "--cities"):
		cities = arg
	elif opt in ("-o", "--offset"):
		offset = int(arg)
	elif opt in ("-a", "--api"):
		api = arg
	elif opt in ("-s", "--saveData"):
		saveData = arg
		if(saveData == 'y'):
			saveData = True
		else:
			saveData = False

if (offset <= 0):
	print 'offset should be greater than 0'
	print 'homeWeatherStation.py -c city1|city2 -o 5 -a xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -s y'
	print 'Example: homeWeatherStation.py -c "London,uk|Madrid,sp" -o 5 -a xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -s y'
	sys.exit()

owm = pyowm.OWM(api)
client = MongoClient()
sense = SenseHat()
sense.set_rotation(90)
loc = getLocalCity()

array_cities = cities.split("|")
lockscreen = threading.Semaphore(1)
threads = list()

#Thread to get internal local temperature
t = threading.Thread(target=getWeatherDataForCity, args=(loc,offset,lockscreen,True,True,))
threads.append(t)
t.start()

#Thread to get external local temperature
t = threading.Thread(target=getWeatherDataForCity, args=(loc,offset,lockscreen,False,True,))
threads.append(t)
t.start()

#Thread to get other cities provided in the parameters
for city in array_cities:
    t = threading.Thread(target=getWeatherDataForCity, args=(city,offset,lockscreen,False,False,))
    threads.append(t)
    t.start()
