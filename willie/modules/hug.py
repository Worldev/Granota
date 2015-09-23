# -*- coding: utf-8 -*-

from willie.module import commands, example

@commands("hug", "abraza", "abrazar", "abraca", "abracada")
@example(".hug John")
def hug(bot, trigger):
    """Hugs the specified nick"""
    if not trigger.group(2):
        nick = trigger.nick
    else:
        nick = trigger.group(2)
    if nick == r'$nickname':
        if bot.config.lang == 'ca':
            bot.msg(trigger.sender, u"\x01ACTION s'abraça a ell mateix\x01")
        elif bot.config.lang == 'es':
            bot.msg(trigger.sender, u"\x01ACTION se abraza a si mismo\x01")
        else:
            bot.msg(trigger.sender, u"\x01ACTION hugs himself\x01")
        return
    else:
        if bot.config.lang == 'ca':
            bot.msg(trigger.sender, u"\x01ACTION abraça a %s\x01" % nick)
        elif bot.config.lang == 'es':
            bot.msg(trigger.sender, u"\x01ACTION abraza a %s\x01" % nick)
        else:
            bot.msg(trigger.sender, "\x01ACTION hugs %s\x01" % nick)
        return
