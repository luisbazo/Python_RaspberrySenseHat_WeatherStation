# Python_RaspberrySenseHat_WeatherStation
Python program that turns your RaspberrySenseHat into your Home Weather Station

This is an example of python program that reads weather data on a range of time, stores data in a mongoDB and performs some weather analysis over data stored.

The project is composed by 3 python scripts

1. homeWeatherStation: Python script to get weather data from your city (where Raspberry is connected) and optionally a list of cities. It also gets temperature from senseHat as the "Home" temperature. 
  
  python homeWeatherStation.py -c "London,uk" -o 1 -a xxxxxxxxx -s y
  
  It gets 3 parameters: 

                       -c the list of additional cities to get weather data
                       -o how often data should be collected (offset)
                       -a API key to get data from OpenWeather http://openweathermap.org/appid
                       -s is data stored 'y' or not 'n'
  
  Considering, it is executed "python homeWeatherStation.py -c "London,uk" -o 1 -a xxxxxxxxx -s y" and the raspberry is plugged in a network around Madrid:
  1. Weather data of city of London is collected from OpenWeather every second and stored in a mongodb.
  2. Weather data if city of Madrid is collected from OpenWeather every second and stored in a mongodb.
  3. Temperature data from rapsberry sensehat sensor is collected every second and stored in a mongodb.

  
2. calculateCityTemperatureAverage: Python script to calculate given city temperature average from data stored in mongoDB.
 
  python calculateCityTemperatureAverage.py -c "Home" 
 
  It gets 1 parameter: 
                      
                        -c the city to be calculated the average temperature. If city is "Home", average is performed against "Home" data collected.
3. resetCityData: Python script to delete all the weather data stored of a given city.
  
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
    
  MongoDB

  
  It is needed to have a mongoDB server installed with a "test" database created. Change the scripts and database name on your convenience.
  Install mongoDB instructions: https://docs.mongodb.com/manual/administration/install-community/
  Once the database server is installed to create a db called "test" execute the steps documented in,
     http://www.tutorialspoint.com/mongodb/mongodb_create_database.htm
  
  Extensions

  More calculations and analysis could be introduced as part of this project. At this initial version it is only provided a mechanism to perform temperature average analysis in a given city. 
  

