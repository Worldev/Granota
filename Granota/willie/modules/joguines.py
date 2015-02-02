# -*- coding: cp1252 -*-
import willie
import random
import time

rbirra = [u'mmmhhh... prohibida la venda a menors de 18 anys :\'(', u'Uiui, quina temptació...',
          u'Crec que no hi puc fer res...']
rbirra2 = [u'glup glup glup. Aaaaaahhhh, estic als núvols!', u'Hip! Hip! Quin singlot!',
           u'Estic borratxo... hip!']

@willie.module.commands('cafe')
def cafe(bot, trigger):
    bot.say('Ui, millor que no, que em posa com una moto! ;)')

@willie.module.commands('birra', 'cervesa', 'vi', 'licor', 'whisky', 'cava')
def alcohol(bot, trigger):
    bot.say(random.choice(rbirra))
    time.sleep(5)
    bot.say(random.choice(rbirra2))

@willie.module.commands('saluda')
def saluda(bot, trigger):
    bot.say('Hola a tots i a totes!')

@willie.module.commands('moneda')
def moneda(bot, trigger):
    bot.say('Tiro una moneda i surt...')
    time.sleep(2)
    moneda = ["cara", "creu"]
    bot.say(random.choice(moneda) + "!")

@willie.module.commands('joguines')
def joguines(bot, trigger):
    bot.say(u'\x02 Llista de joguines:\x02 cafe, birra, cervesa, vi, licor, whisky, cava, saluda, moneda. Si us plau, no n\'abuseu.')
