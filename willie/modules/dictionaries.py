# -*- coding: cp1252 -*-

from willie import web, tools
from willie.module import commands, example
from HTMLParser import HTMLParser

@commands('diec')
def diec(bot, trigger):
    if trigger.group(2):
        bot.reply('http://dlc.iec.cat/results.asp?txtEntrada=%s' % (trigger.group(2)))
    if trigger.group(2) == None:
        if bot.config.lang == 'ca':
            bot.reply(u"Digue'm que vols buscar, però!")
        elif bot.config.lang == 'es':
            bot.reply(u"Pero dime que quieres buscar!")
        else:
            bot.reply(u"But tell me what I have to search!")
        return

@commands('drae')
def drae(bot, trigger):
    if trigger.group(2):
        bot.reply('http://lema.rae.es/drae/?val=%s' % (trigger.group(2)))
    if trigger.group(2) == None:
        if bot.config.lang == 'ca':
            bot.reply(u"Digue'm que vols buscar, però!")
        elif bot.config.lang == 'es':
            bot.reply(u"Pero dime que quieres buscar!")
        else:
            bot.reply(u"But tell me what I have to search!")
        return

@commands('wordreference', 'define')
def wordreference(bot, trigger):
    if trigger.group(2):
        bot.reply('http://www.wordreference.com/definition/%s' % (trigger.group(2)))
    if trigger.group(2) == None:
        if bot.config.lang == 'ca':
            bot.reply(u"Digue'm que vols buscar, però!")
        elif bot.config.lang == 'es':
            bot.reply(u"Pero dime que quieres buscar!")
        else:
            bot.reply(u"But tell me what I have to search!")
        return
