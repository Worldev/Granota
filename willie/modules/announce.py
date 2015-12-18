# -*- coding: utf8 -*-

import willie
import time


@willie.module.commands('anunci', 'anuncia', 'announce', 'anuncio')
def announce(bot, trigger):
    if not trigger.admin:
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
        elif bot.config.lang == 'es':
            bot.msg(channel, '[ANUNCIO GLOBAL] %s' % trigger.group(2))
        else:
            bot.msg(channel, '[GLOBAL ANNOUNCE] %s' % trigger.group(2))
