from flask import Flask, render_template, request
import datetime
import random
import pyowm
#import Adafruit_DHT

# import Sensor Library if platform supports it
app = Flask(__name__)
DEBUG = True

class Module:
    """base class for all widgets"""
    def __init__(self):
        self.module_id = 'None'

    def get_data(self):
        return

class Weather(Module):
    def __init__(self):
        """interface with pyOWM and get weather for today and tomorrow"""
        self.module_id = 'weather'
        self.API_KEY = "b73be8484d3f27de362941e1b3777485"
        self.owm = pyowm.OWM(self.API_KEY)

        self.observation = self.owm.weather_at_coords( -41.29, 174.78 )
        self.forecast = self.owm.three_hours_forecast('Wellington,nz')

        self.weather = self.observation.get_weather()
        self.weather_forecast = self.forecast.get_forecast()

        #tomorrow weather
        tomorrow = pyowm.timeutils.tomorrow(9, 0)
        tomorrow_weather = self.forecast.get_weather_at(tomorrow)
        print tomorrow_weather.__dict__


    def get_data(self):
        """get relevant weather stats"""
        data = {}
        data['will_rain'] = self.get_rainy(1)
        data['temp'] = self.get_temperature()
        data['status'] = self.weather.get_detailed_status()

        return data

    def get_rainy(self, DEBUG = 0):
        """return 'will' or 'won't' if its going to rain today"""

        if DEBUG:
            return 'might'

        if self.weather.will_have_rain():
            return 'will'
        else:
            return 'wont'

    def get_temperature(self):
        """parse temperature input and get current, max and min"""
        t = self.weather.get_temperature(unit='celsius')
        return round(t['temp'], 1)

    def get_icon(self):
        pass

class TempSensor(Module):
    def __init__(self):
        """class for interfacing with AM2302 Temperature Sensor"""
        self.module_id = 'tempsensor'
        self.sensor = Adafruit_DHT.AM2302
        self.pin = 4

    def get_data(self):
        """get readings until one is found. TEST THIS"""
        humidity, temperature  = Adafruit_DHT.read_retry(self.sensor, self.pin)
        
        if temperature is not None and humidity is not None:
            return humidity, round(temperature, 2)
        else:
            return self.get_data()

class ApproximateTime(Module):
    def __init__(self):
        self.module_id = 'approximatetime'

    def get_data(self):
        """return a string for the current rough time of day for greetings"""
        dt = datetime.datetime.now()

        if dt.hour < 12:
            return 'morning'
        elif dt.hour < 18:
            return 'afternoon'
        elif dt.hour < 23:
            return 'evening'
        else:
            return 'night'

class Name(Module):
    def __init__(self):
        self.module_id = 'name'
        self.name = 'Benjamin'

    def get_data(self):
        """return the name or randomly change the name to something flattering"""
        if random.randint(0,8) == 1:
            return random.choice(['Sexy','Beautiful','Handsome','Gorgeous'])
        else:
            return self.name

class Footer(Module):
    def __init__(self):
        self.module_id = 'footer'

    def get_data(self):
        """get a quote or rss feed, depending on if theres anything 
        interesting on RSS"""
        return "Nothing interesting happening today."

@app.route("/")
def home():

    # get all the arguments for the template
    modules = [Name, Weather, ApproximateTime, Footer]
    
    kwargs = {}
    for module in modules:
        mod = module()
        kwargs[mod.module_id] = mod.get_data()

    if DEBUG:
        print kwargs
    else:
        # send values to page
        return render_template("index.html",**kwargs)

if __name__ == "__main__":
    if DEBUG:
        home()
    else:
        app.run(host='0.0.0.0', port=85, debug=True)
