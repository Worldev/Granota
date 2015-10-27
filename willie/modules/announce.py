# -*- coding: utf8 -*-

import willie
import time


@willie.module.commands('anunci', 'anuncia', 'announce', 'anuncio')
@willie.module.example('.announce message')
def announce(bot, trigger):
    u"""
    Fa un anunci a tots els canals
    """
    if not trigger.owner:
        if bot.config.lang == 'ca':
            bot.reply(u'No ets el meu owner.')
        elif bot.config.lang == 'es':
            bot.reply(u"No eres mi owner.")
        else:
            bot.reply(u"You are not my owner.")
        return
    channels = bot.config.channels.split(',')
    for channel in channels:
        if bot.config.lang == 'ca':
            bot.msg(channel, '[ANUNCI GLOBAL] %s' % trigger.group(2))
            time.sleep(2) # To avoid anti-flood measures.
        elif bot.config.lang == 'es':
            bot.msg(channel, '[ANUNCIO GLOBAL] %s' % trigger.group(2))
            time.sleep(2) # To avoid anti-flood measures.
        else:
            bot.msg(channel, '[GLOBAL ANNOUNCE] %s' % trigger.group(2))
            time.sleep(2) # To avoid anti-flood measures.
