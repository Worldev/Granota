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
            bot.me(u"s'abraça a ell mateix")
        elif bot.config.lang == 'es':
            bot.me(u"se abraza a si mismo")
        else:
            bot.me(u"hugs himself")
        return
    else:
        if bot.config.lang == 'ca':
            bot.me(u"abraça a %s" % nick)
        elif bot.config.lang == 'es':
            bot.me(u"abraza a %s" % nick)
        else:
            bot.me("hugs %s" % nick)
        return
