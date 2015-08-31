# -*- coding: cp1252 -*-

from willie.module import commands, example

@commands('reinicia', 'reboot', 'reinici', 'reinicio', 'restart')
def reboot(bot, trigger):
    if trigger.owner or trigger.admin:
        bot.callables = None
        bot.commands = None
        bot.setup()
        if bot.config.lang == 'ca':
            bot.reply("Bot reiniciat correctament")
        elif bot.config.lang == 'es':
            bot.reply("Bot reiniciado correctamente")
        else:
            bot.reply("Bot rebooted.")
        return
    else:
        return bot.reply("You aren't my owner")
