# -*- coding: utf-8 -*-
from willie.module import commands, example
import time
import random
import re

@commands('cake', 'pastel', 'pastis')
@example('.cake NeoMahler')
def pastis(bot, trigger):
    u"""
    Give a cake to the specified user.
    """
    if bot.config.lang == 'ca':
        cakes = ["...me'l menjo tot sencer, deixant les espelmes per %s, es clar!",
                    "...el dono a %s, per bona persona!",
                    "...el tiro a la cara de %s, per golafre!"]
    elif bot.config.lang == 'es':
        cakes = ["...me lo como enterito, dejando las velas para %s, claro!",
                    "...lo doy a %s, por ser buena persona!",
                    "...lo tiro a la cara de %s, por glotón!"]
    else:
        cakes = ["...I eat all the cake, but giving the candles to %s!",
                    "...I give the cake to %s, because is a nice person!",
                    "...I throw the cake to %s's face!"]
    if bot.config.lang == 'ca':
        bot.say(u"Agafo un pastís i...")
    elif bot.config.lang == 'es':
        bot.say(u"Cojo un pastel y...")
    else:
        bot.say(u"I take a cake and...")
    time.sleep(1)
    bot.say(random.choice(cakes) % trigger.group(2))

@commands('galeta', 'galleta', 'cookie')
@example('.cookie NeoMahler')
def galeta(bot, trigger):
    u"""
    Gives a cookie to the specified user.
    """
    if not trigger.group(2):
        return
    if bot.config.lang == 'ca':
        elme = '\x01ACTION dóna una galleta a %s\x01' % trigger.group(2)
        bot.msg(trigger.sender, elme)
    elif bot.config.lang == 'es':
        elme = '\x01ACTION da una galleta a %s\x01' % trigger.group(2)
        bot.msg(trigger.sender, elme)
    else:
        elme = '\x01ACTION gives a cookie to %s\x01' % trigger.group(2)
        bot.msg(trigger.sender, elme)
