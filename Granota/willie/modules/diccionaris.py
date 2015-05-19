# -*- coding: cp1252 -*-

from willie import web, tools
from willie.module import commands, example
from HTMLParser import HTMLParser

@commands('diec')
@example('.diec paraula')
def diec(bot, trigger):
    """Busca una paraula al DIEC"""
    if trigger.group(2):
        bot.say('http://dlc.iec.cat/results.asp?txtEntrada=%s' % (trigger.group(2)))
    if trigger.group(2) == None:
        if bot.config.lang == 'ca':
            bot.reply(u"Digue'm que vols buscar, però!")
        elif bot.config.lang == 'es':
            bot.reply(u"Pero dime que quieres buscar!")
        else:
            bot.reply(u"But tell me what I have to search!")
        return

@commands('drae')
@example('.drae paraula')
def drae(bot, trigger):
    """Busca una paraula al DRAE"""
    if trigger.group(2):
        bot.say('http://lema.rae.es/drae/?val=%s' % (trigger.group(2)))
    if trigger.group(2) == None:
        if bot.config.lang == 'ca':
            bot.reply(u"Digue'm que vols buscar, però!")
        elif bot.config.lang == 'es':
            bot.reply(u"Pero dime que quieres buscar!")
        else:
            bot.reply(u"But tell me what I have to search!")
        return
