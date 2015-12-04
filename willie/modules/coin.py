# -*- coding: cp1252 -*-
import willie
import random
import time

@willie.module.commands('moneda', 'coin')
def moneda(bot, trigger):
    if bot.config.lang == 'ca':
    	moneda = ['cara', 'creu']
    elif bot.config.lang == 'es':
    	moneda = ['cara', 'cruz']
    else:
    	moneda = ["heads", "tails"]
    if bot.config.lang == 'ca':
          bot.say('\x01ACTION tira una moneda i surt... \x02%s\x02!\x01' % random.choice(moneda))
    elif bot.config.lang == 'es':
    	bot.say('\x01ACTION tira una moneda y sale... \x02%s\x02!\x01' % random.choice(moneda))
    else:
    	bot.say('\x01ACTION tosses a coin into the air that lands on... \x02%s\x02!\x01' % random.choice(moneda))
