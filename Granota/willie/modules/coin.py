# -*- coding: cp1252 -*-
import willie
import random
import time

@willie.module.commands('moneda', 'coin')
def moneda(bot, trigger):
    if bot.config.lang == 'ca':
          bot.me('Tira una moneda i surt...')
    elif bot.config.lang == 'es':
    	bot.me('Tira una moneda y sale...')
    else:
    	bot.me('tosses a coin into the air that lands on...')
    if bot.config.lang == 'ca':
    	moneda = ['cara', 'creu']
    elif bot.config.lang == 'es':
    	moneda = ['cara', 'cruz']
    else:
    	moneda = ["heads", "tails"]
    bot.say(random.choice(moneda) + "!")
