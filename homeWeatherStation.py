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
import ibmiotf.gateway
import ibmiotf.device
from optparse import OptionParser

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
		jsonloads = json.loads(jsonweather)
		jsonloads['city']=city

		if(isLocal):
			local_temp = celciusToKelvin(sense.get_temperature())
			jsonloads['city']='Home'
			jsonloads['temperature']['temp']=local_temp

		if(display):
			#Just let one process adquire dispaly at a time
			lockscreen.acquire()
			displayCityWeatherOnSenseHatDisplay(jsonloads)
			lockscreen.release()
			#############################################
		if(sendToWatsonIoT):
			deviceCli.publishEvent("event", "json", json.dumps(jsonloads), qos=1 )
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
		sense.show_message(str(jsonloads['detailed_status']), 0.05, colour, black)
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

#MAIN
parser = OptionParser()
parser.add_option("-c", "--cities", dest="cities",help="Cities to get weather from: Example: London,uk", metavar="CITY,COUNTRY_CODE")
parser.add_option("-o", "--offset", dest="offset", help="how fast in seconds weather has to be retreived")
parser.add_option("-a", "--api", dest="api",help="api key to get access to openweather")
parser.add_option("-s", "--saveData",action="store_true",dest="saveData",default=False, help="Whether to store data on mongoDB or not")
parser.add_option("-w","--watsoniot",action="store_true",dest="sendToWatsonIoT",default=False, help="Whether to send data to WatsonIoT or not")
parser.add_option("-l","--watsoniotoptions",type="string", nargs=4, dest="woptions",help="Watson IoT Connection Options: org sense_type sense_id token",metavar="org sense_type sense_id token")

(opts, args) = parser.parse_args()
cities = opts.cities
offset=float(opts.offset)
api=opts.api
saveData=opts.saveData
sendToWatsonIoT=opts.sendToWatsonIoT
if(sendToWatsonIoT): (org,type_sensor,id_sensor,auth_token)= opts.woptions

owm = pyowm.OWM(api)
if(saveData):
	client = MongoClient()
sense = SenseHat()
sense.set_rotation(90)
loc = getLocalCity()
if(sendToWatsonIoT):
	try:
		deviceOptions = {"org": org, "type": type_sensor, "id": id_sensor, "auth-method": "token", "auth-token": auth_token}
    		deviceCli = ibmiotf.device.Client(deviceOptions)
    		deviceCli.connect()
	except ibmiotf.ConnectionException  as e:
    		print(e)


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
    t = threading.Thread(target=getWeatherDataForCity, args=(city,offset,lockscreen,False,True,))
    threads.append(t)
    t.start()
