from flask import Flask, render_template, request
import datetime
import random
import pyowm

# import Sensor Library if platform supports it
try:
    import Adafruit_DHT
except ImportError:
    temp_sens = False
    print 'WARNING: failed to import Temperature Sensor library'


"""To Do: Figure out how to fix the whole 'burn-in' thing """

app = Flask(__name__)

class Module:
    """base class for all widgets"""
    def __init__(self):
        pass

    def get_data(self):
        return

class Weather(Module):
    def __init__(self):
        """interface with pyOWM and get weather for today"""
        self.API_KEY = "b73be8484d3f27de362941e1b3777485"
        self.owm = pyowm.OWM(self.API_KEY)
        self.observation = self.owm.weather_at_id(2179537)
        self.weather = self.observation.get_weather()

    def get_data(self):
        """get relevant weather stats"""
        data = {}
        data['will_rain'] = self.get_rainy(1)
        data['temp'], data['temp_max'], data['temp_min'] = self.get_temperature()

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
        return [int(t['temp']), int(t['temp_max']), int(t['temp_min'])]

class TempSensor(Module):
    def __init__(self):
        """class for interfacing with AM2302 Temperature Sensor"""
        self.sensor = Adafruit_DHT.AM2302
        self.pin = 4

    def get_data(self):
        """get readings until one is found"""
        temperature, humidity = Adafruit_DHT.read_retry(self.sensor, self.pin)
        
        if temperature is not None and humidity is not None:
            return temperature, humidity
        else:
            return self.get_data()

class ApproximateTime(Module):
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
        self.name = 'Benjamin'

    def get_data(self):
        """return the name or randomly change the name to something flattering"""
        if random.randint(0,8) == 1:
            return random.choice(['Sexy','Beautiful','Handsome','Gorgeous'])
        else:
            return self.name

class Footer(Module):
    def get_data(self):
        """get a quote or rss feed, depending on if theres anything 
        interesting on RSS"""
        return "Nothing interesting happening today."


def get_render_template(**kwargs):
    """get render template. kwargs: each module class"""
    return render_template("test_layout_mirror.html", **kwargs)

@app.route("/")
def home():

    # get temperature inside
    if temp_sens:
        temperature = TempSensor
    else:
        # set temperature to empty module
        temperature = Module

    # get all the arguments for the template
    modules = [Name, Weather, ApproximateTime, temperature, Footer]
    
    for module in modules:
        mod = module()
            
    kwargs = {"greeting":"Yo Dawg"}

    # send values to page
    return get_render_template(**kwargs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=85, debug=True)