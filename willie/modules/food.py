# -*- coding: utf-8 -*-
from willie.module import commands, example
import time
import random
import re

@commands('cake', 'pastel', 'pastis')
def pastis(bot, trigger):
    if ' ' in trigger.group(2):
        nick = trigger.group(2).split()[0]
    elif bot.nick in trigger.group(2):
        nick = bot.nick
    else:
        nick = trigger.group(2)
    if bot.config.lang == 'ca':
        cakes = [u"...me'l menjo tot sencer, deixant les espelmes per %s, es clar!",
                    u"...el dono a %s, per bona persona!",
                    u"...el tiro a la cara de %s, per golafre!"]
    elif bot.config.lang == 'es':
        cakes = [u"...me lo como enterito, dejando las velas para %s, claro!",
                    u"...lo doy a %s, por ser buena persona!",
                    u"...lo tiro a la cara de %s, por glotón!"]
    else:
        cakes = [u"...I eat all the cake, but giving the candles to %s!",
                    u"...I give the cake to %s, because is a nice person!",
                    u"...I throw the cake to %s's face!"]
    if bot.config.lang == 'ca':
        bot.say(u"Agafo un pastís i...")
    elif bot.config.lang == 'es':
        bot.say(u"Cojo un pastel y...")
    else:
        bot.say(u"I take a cake and...")
    time.sleep(1)
    bot.say(random.choice(cakes) % nick)

@commands('galeta', 'galleta', 'cookie')
def galeta(bot, trigger):
    if not trigger.group(2):
        return
    if bot.config.lang == 'ca':
        elme = u'\x01ACTION dóna una galeta a %s\x01' % trigger.group(2)
        bot.msg(trigger.sender, elme)
    elif bot.config.lang == 'es':
        elme = u'\x01ACTION da una galleta a %s\x01' % trigger.group(2)
        bot.msg(trigger.sender, elme)
    else:
        elme = u'\x01ACTION gives a cookie to %s\x01' % trigger.group(2)
        bot.msg(trigger.sender, elme)
