# -*- coding: cp1252 -*-

from willie.module import commands, example

@commands('reinicia', 'reboot')
@example(u'.reinicia mòdul')
def reinicia(bot, trigger):
    u"""Recarrega un mòdul"""
    if trigger.owner:
        bot.callables = None
        bot.commands = None
        bot.setup()
        return bot.reply('Fet ;)')

    if not trigger.owner:
        return bot.reply(u"Tros d'esclau! Aixo només ho pot fer la noblesa!! XD")
