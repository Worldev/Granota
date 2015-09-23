# -*- coding: utf-8 -*-

from willie.module import commands, example
import random

hugs_ca = [u"abraça a %s", u"es menja a petons a %s", u"es llança a sobre de %s per abraçar-lo", u"omple de petons a %s"]
hugs_es = [u"abraza a %s", u"se come a besos a %s", u"se lanza sobre %s para abrazarlo", "llena de besitos a %s"]
hugs_en = [u"hugs %s", u"eats %s with kisses", u"throws himself over %s to hug them"]

@commands("hug", "abraza", "abrazar", "abraca", "abracada")
@example(".hug John")
def hug(bot, trigger):
    """Hugs the specified nick"""
    if not trigger.group(2):
        nick = trigger.nick
    else:
        nick = trigger.group(2)
    if bot.config.nick in nick:
        if bot.config.lang == 'ca':
            bot.msg(trigger.sender, u"\x01ACTION s'abraça a ell mateix\x01")
        elif bot.config.lang == 'es':
            bot.msg(trigger.sender, u"\x01ACTION se abraza a si mismo\x01")
        else:
            bot.msg(trigger.sender, u"\x01ACTION hugs himself\x01")
        return
    else:
        if bot.config.lang == 'ca':
            msg = (random.choice(hugs_ca) % nick)
            bot.msg(trigger.sender, u"\x01ACTION %s\x01" % msg)
        elif bot.config.lang == 'es':
            msg = (random.choice(hugs_es) % nick)
            bot.msg(trigger.sender, u"\x01ACTION %s\x01" % msg)
        else:
            msg = (random.choice(hugs_en) % nick)
            bot.msg(trigger.sender, "\x01ACTION %s\x01" % msg)
        return
