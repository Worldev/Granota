# -*- coding: cp1252 -*-

from willie.module import commands, example

@commands('reinicia', 'reboot', 'reinici', 'reinicio', 'restart')
def reboot(bot, trigger):
    if trigger.owner:
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

    if not trigger.owner:
        return bot.reply(u"You aren't my owner")
