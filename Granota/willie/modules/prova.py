# -*- coding: cp1252 -*-
import willie

@willie.module.commands('provajoin')
def prova(bot, trigger):
    if not trigger.owner:
        bot.reply(u"No tens permisos")
        return
    if trigger.sender.startswith('#'):
        bot.reply(u"En prvat, si us plau")
        return 
    if trigger.owner:
        channel, key = trigger.group(2), trigger.group(3)
        if not channel:
            bot.say(u"??")
            return
        if not key:
            bot.join(channel)
        else:
            bot.join(channel, key)
