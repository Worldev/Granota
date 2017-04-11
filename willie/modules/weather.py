# -*- coding: utf-8 -*-

from willie.module import commands
import urllib2, urllib, json 
from decimal import Decimal


@commands('weather', 'tiempo', 'temps')
def weather(bot, trigger):
    weatherLocation = trigger.group(2)
    
    if not weatherLocation:
        if bot.config.lang == 'ca':
            bot.reply(u'Mmmmhhh... sóc un bot però no et puc llegir el pensament...')
        if bot.config.lang == 'es':
            bot.reply('Mmmmhhh... soy un bot pero no puedo leerte el pensamiento...')
        else:
            bot.reply('Mmmmhhh... I\'m a bot but I can\'t read your thoughts...')
            
    else:
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + weatherLocation + "')"
        yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
        result = urllib2.urlopen(yql_url).read()
        data = json.loads(result)
        if not data or data.get('query').get('results') is None:
            if bot.config.lang == 'ca':
                bot.reply(u'No he pogut obtenir la informació meteorològica d\'aquest lloc.')
            if bot.config.lang == 'es':
                bot.reply(u'No pude obtener la información meteorológica de este lugar.')
            else:
                bot.reply('Sorry, I couldn\'t get the weather conditions for the location you entered')
        else:
            
            text = data.get('query').get('results').get('channel').get('item').get('condition').get('text')
            temp = data.get('query').get('results').get('channel').get('item').get('condition').get('temp')
            if temp:
                temp = convert_f2c(temp)
                
            
            if text and temp:
                if bot.config.lang == 'ca':
                    text = translate(text.lower(), 'ca')
                    bot.reply(u'Actualment, %s a %s amb una temperatura de %s graus.' % (text.lower(), weatherLocation, str(temp).replace('.', ',')))
                if bot.config.lang == 'es':
                    text = translate(text.lower(), 'es')
                    bot.reply(u'Actualmente, %s en %s con una temperatura de %s grados Celsius.' % (text.lower(), weatherLocation, str(temp).replace('.', ',')))
                else:
                    bot.reply('It is currently %s in %s with a temperature of %s Celsius' % (text.lower(), weatherLocation, temp))
            else:
                if bot.config.lang == 'ca':
                    bot.reply(u'No he pogut obtenir tota la informació que necessito.')
                if bot.config.lang == 'es':
                    bot.reply(u'No pude obtener toda la información que necesito.')
                else:
                    bot.reply('Sorry, I couldn\'t get all the information I needed')
                    
                    
def convert_f2c(S):
    """(str): float

    Converts a Fahrenheit temperature represented as a string
    to a Celsius temperature with two decimals.
    """
    fahrenheit = float(S)
    celsius = Decimal((fahrenheit - 32) * 5 / 9)
    return round(celsius, 2)

def translate(c, lang):
    # List of possible conditions: https://developer.yahoo.com/weather/documentation.html#codes
    conditions_ca = {
        'tropical storm': 'tempesta tropical',
        'hurricane': u'huracà',
        'severe thunderstorms': 'temporal sever',
        'thunderstorm': 'temporal',
        'mixed rain and snow': 'barreja de pluja i neu',
        'mixed rain and sleet': 'barreja de pluja i aiguaneu',
        'mixed snow and sleet': 'barreja de neu i aiguaneu',
        'freezing drizzle': 'plovisqueig gelat',
        'drizzle': 'plovisqueig',
        'freezing rain': 'pluja gelada',
        'showers': 'plugim',
        'snow flurries': 'ràfegues de neu',
        'light snow showers': 'nevada suau',
        'blowing snow': 'torb',
        'snow': 'neva',
        'hail': 'calamarsa',
        'sleet': 'aiguaneu',
        'dust': 'tempesta de pols',
        'foggy': 'boira',
        'haze': 'calitja',
        'smoky': 'smoky', # Don't know how to translate this
        'blustery': 'vent impetuós',
        'windy': 'vent',
        'cloudy': 'núvols',
        'mostly cloudy (night)': 'força ennuvolat (nit)',
        'mostly cloudy (dia)': 'força ennuvolat (dia)',
        'partly cloudy (night)': 'parcialment ennuvolat (nit)',
        'partly cloudy (day)': 'parcialment ennuvolat (dia)',
        'clear (night)': 'nit sense núvols',
        'sunny': 'sol',
        'fair (night)': 'bon temps (nit)',
        'fair (day)': 'bon temps (dia)',
        'mixed rain and hail': 'barreja de pluja i calamarsa',
        'hot': 'temperatures altes',
        'isolated thunderstorms': 'tempestes aïllades',
        'scattered thunderstorms': 'tempestes disperses',
        'scattered showers': 'plugims dispersos',
        'heavy snow': 'nevada forta',
        'scattered snow showers': 'nevades disperses',
        'partly cloudy': 'parcialment ennuvolat',
        'thundershowers': 'pluja amb tempesta elèctrica',
        'snow showers': 'nevada',
        'isolated thundershowers': 'plujes amb tempestes elèctriques aïllades',
        'breezy': 'brisa'
    }
    conditions_es = {
        'tropical storm': 'tormenta tropical',
        'hurricane': u'huracán',
        'severe thunderstorms': 'temporal severo',
        'thunderstorm': 'temporal',
        'mixed rain and snow': 'mezcla de lluvia y nieve',
        'mixed rain and sleet': 'mezcla de lluvia y aguanieve',
        'mixed snow and sleet': 'mezcla de nieve y aguanieve',
        'freezing drizzle': 'llovizna helada',
        'drizzle': 'llovizna',
        'freezing rain': 'lluvia helada',
        'showers': 'lluvias',
        'snow flurries': 'ráfagas de nieve',
        'light snow showers': 'nevada suave',
        'blowing snow': 'ventisca',
        'snow': 'nevada',
        'hail': 'calamarsa',
        'sleet': 'aguanieve',
        'dust': 'tormenta de polvo',
        'foggy': 'niebla',
        'haze': 'neblina',
        'smoky': 'smoky', # Don't know how to translate this
        'blustery': 'viento tempestuoso',
        'windy': 'viento',
        'cloudy': 'nubes',
        'mostly cloudy (night)': 'bastante nublado (noche)',
        'mostly cloudy (dia)': 'bastante nublado (día)',
        'partly cloudy (night)': 'parcialmente nublado (noche)',
        'partly cloudy (day)': 'parcialmente nublado (día)',
        'clear (night)': 'noche sin nubes',
        'sunny': 'sol',
        'fair (night)': 'buen tiempo (noche)',
        'fair (day)': 'buen tiempo (día)',
        'mixed rain and hail': 'mezcla de lluvia y calamarsa',
        'hot': 'temperaturas altas',
        'isolated thunderstorms': 'tormentas aisladas',
        'scattered thunderstorms': 'tormentas dispersas',
        'scattered showers': 'llovizna dispersa',
        'heavy snow': 'fuerte nevada',
        'scattered snow showers': 'nevada dispersa',
        'partly cloudy': 'parcialmente nublado',
        'thundershowers': 'lluvia con tormenta eléctrica',
        'snow showers': 'nevada',
        'isolated thundershowers': 'lluvia con tormenta eléctrica aislada',
        'breezy': 'brisa'
    }
    try:
        if lang == 'ca':
            return conditions_ca[c]
        elif lang == 'es':
            return conditions_es[c]
        # No need for English here
    except KeyError:
        return c
