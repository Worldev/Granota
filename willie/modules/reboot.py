# -*- coding: cp1252 -*-

from willie.module import commands, example

@commands('reboot')
def reboot(bot, trigger):
    if trigger.owner or trigger.admin:
        bot.callables = None
        bot.commands = None
        bot.setup()
        if bot.config.lang == 'ca':
            bot.reply(u"Bot reiniciat correctament")
        elif bot.config.lang == 'es':
            bot.reply(u"Bot reiniciado correctamente")
        else:
            bot.reply(u"Bot rebooted.")
        return
    else:
        return bot.reply(u"You aren't my owner")
