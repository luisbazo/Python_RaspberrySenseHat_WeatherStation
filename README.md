# Python_RaspberrySenseHat_WeatherStation
Python program that turns your RaspberrySenseHat into your Home Weather Station

This is an example of python program that reads weather data on a range of time, stores data in a mongoDB and/or sends to IBM Watson IoT Platform and performs some weather analysis over data stored.

The project is composed by 3 python scripts

1. homeWeatherStation: Python script to get weather data from your city (where the Raspberry is connected, script uses http://freegeoip.net/json/ to get the location) and optionally a list of cities. It also gets temperature from senseHat as the "Home" temperature. Data can be stored locally in mongoDB database or send to the IBM Watson IoT Platform.

  python homeWeatherStation.py -h

  Usage: homeWeatherStation.py [options]

  Options:
    -h, --help            show this help message and exit
    -c CITY,COUNTRY_CODE, --cities=CITY,COUNTRY_CODE
                          Cities to get weather from: Example: London,uk
    -o OFFSET, --offset=OFFSET
                          how fast in seconds weather has to be retreived
    -a API, --api=API     api key to get access to OpenWeather
    -s, --saveData        Whether to store data on local mongoDB or not
    -w, --watsoniot       Whether to send data to Watson IoT platform or not
    -l org sense_type sense_id token, --watsoniotoptions=org sense_type sense_id token
                          Watson IoT Connection Options: org sense_type sense_id
                          token

  Considering, it is executed

      python homeWeatherStation.py -c "Mexico DF,MX|London,uk|Susqueda,ES" -o 20 -a xxxxxxxxx -s -w -l i8go1q raspberry senrasp01 xxxxx

  1. Weather data of city of London,MexicoDF,Susqueda is collected from OpenWeather every 20s and optionally stored in a local mongodb and/or send the data to IBM Watson IoT Platfrom.
  2. Weather data of where raspberry is connected is collected from OpenWeather every 20s and stored in a local mongodb and/or send to IBM Watson IoT Platfrom.
  3. Temperature data from Rapsberry Sensehat Sensor is collected every 20s and and stored in a local mongodb and/or send to IBM Watson IoT Platfrom.
  4. Weather data (how is weather like -Clear, Rain, etc- and temperature) from all cities (including local) is displayed in the SenseHat display 8x8 pixels.

  Data is stored or sent to IBM Watson IoT only if parameters -s or -w are provided.

  If parameter -w is passed to the script, -l has to be provided with the info to connect IBM Watson IoT Platform Sensor. Read https://console.ng.bluemix.net/docs/starters/IoT/iot500.html to get started with IBM Watson IoT Platform and know how to create sensors, receive data and optionally store and process data in the platform.

2. calculateCityTemperatureAverage: Python script to calculate given city temperature average from data stored in local mongoDB.

  python calculateCityTemperatureAverage.py -c "Home"

  It gets 1 parameter:

                        -c the city to be calculated the average temperature. If city is "Home", average is calculated against "Home" data.

3. resetCityData: Python script to delete all the weather data locally stored of a given city.

  python resetCityWeather.py -c "Home"

  It gets 1 parameter:

                        -c the city to be reset all weather data stored.  
Prerequisites

  Python Libraries


  Use library pymongo to connect the mongoDB. To install execute command

        pip install pymongo

  For more related information please visit: https://docs.mongodb.com/getting-started/python/
  Use library pyown to get weather data from http://openweathermap.org/. To install execute command

      pip install pyowm

  MongoDB (Local)


  It is needed to have a mongoDB server installed with a "test" database created. Change the scripts and database name on your convenience.
  Install mongoDB instructions: https://docs.mongodb.com/manual/administration/install-community/
  Once the database server is installed to create a db called "test" execute the steps documented in,
     http://www.tutorialspoint.com/mongodb/mongodb_create_database.htm

  Watson IoT Sensor


  It is needed to have a Watson IoT sensor created to send data to the IBM Watson IoT platform. Read https://console.ng.bluemix.net/docs/starters/IoT/iot500.html to get started.

  Extensions


  More calculations and analysis could be introduced as part of this project. At this initial version it is only provided a mechanism to perform temperature average analysis in a given city.

  It can be created, in the case data is sent to the IBM Watson IoT Platform, a service to analyze data or store data using a graphical interface called node-red. Please read https://developer.ibm.com/recipes/tutorials/deploy-watson-iot-node-on-raspberry-pi/ to get started.
