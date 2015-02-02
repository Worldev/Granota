# -*- coding: utf8 -*-
"""
announce.py - Send a message to all channels
Copyright © 2013, Elad Alfassa, <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

"""
from willie.module import commands, example


@commands('anunci', 'anuncia')
@example('.anunci missatge')
def announce(bot, trigger):
    u"""
    Fa un anunci a tots els canals on el bot està connectat
    """
    if not trigger.admin:
        bot.reply(u'Sisi, tot el que vulguis, però tu no ets administrador!')
        return
    for channel in bot.channels:
        bot.msg(channel, ' %s' % trigger.group(2))
