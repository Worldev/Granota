# -*- coding: cp1252 -*-
import willie
from willie import module

@willie.module.commands('amor')
def cafe(bot, trigger):
    bot.say('...com t\'estimo...')
import willie

@willie.module.commands('poema')
def alcohol(bot, trigger):
    bot.say(u'Si giro els ulls al cel, et comparo amb les estrelles. Boniques són les que ovir, més totes les senyorejes!')

@willie.module.commands('lligar')
def lligar(bot, trigger):
    bot.say('Estudies o treballes? ;)')

@willie.module.commands('casament')
def casament(bot, trigger):
    bot.say(u'Ei, ens casem demà, guapa?')

@module.rule(u'guapo')
def guapo(bot, trigger):
    bot.say(u'Gràcies!')

@module.rule(u'T\'estimo')
def estimo(bot, trigger):
    bot.say(u'Jo també... Ens casem?')

@module.rule('sexy')
def sexy(bot, trigger):
    bot.say(u'Tu més!')

@module.rule(u'gràcies')
def gracies(bot, trigger):
    bot.say(u'De res guapo!')
