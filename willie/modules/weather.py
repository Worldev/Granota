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
                    bot.reply(u'Actualment, %s a %s amb una temperatura de %s graus.' % (text.lower(), weatherLocation, temp.replace('.', ',')))
                if bot.config.lang == 'es':
                    bot.reply(u'Actualmente, %s en %s con una temperatura de %s grados Celsius.' % (text.lower(), weatherLocation, temp.replace('.', ',')))
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
