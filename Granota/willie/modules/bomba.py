# -*- coding: utf-8 -*-
"""
bomb.py - Simple Willie bomb prank game
Copyright 2012, Edward Powell http://embolalia.net
Licensed under the Eiffel Forum License 2.

http://willie.dfbta.net
"""
from willie.module import commands
from random import choice, randint
from re import search
import sched
import time

colors = ['Red', 'Yellow', 'Blue', 'White', 'Black']
sch = sched.scheduler(time.time, time.sleep)
fuse = 120  # seconds
bombs = dict()


@commands('bomb', 'bomba')
def start(bot, trigger):
    u"""
    Posa una bomba a l'usuari especificat.
    """
    if not trigger.group(2):
        return

    if not trigger.sender.startswith('#'):
        return
    global bombs
    global sch
    target = trigger.group(2).split(' ')[0]
    if target in bot.config.other_bots or target == bot.nick:
        return
    if target == trigger.owner:
        return
    if target in bombs:
        bot.say(u'No puc posar una altre bomba a ' + target + '!')
        return
    message = 'Ei, ' + target + u'! Sembla que algú t\'ha posat una bomba... Tens  2 minuts i 5 cables: Red, Yellow, Blue, White i Black. Quin cable he de tallar? No pateixis, jo sé el que em faig! (respon amb ".talla color")'
    bot.say(message)
    color = choice(colors)
    bot.msg(trigger.nick,
               u"Ei, no li diguis a %s, però és el cable %s! "
               u"Però xxxt! No li diguis a ningú!" % (target, color))
    code = sch.enter(fuse, 1, explode, (bot, trigger))
    bombs[target.lower()] = (color, code)
    sch.run()


@commands('cutwire','talla')
def cutwire(bot, trigger):
    u"""
    Talla el cable especificat quan algú et posa una bomba.
    """
    global bombs, colors
    target = trigger.nick
    if target.lower() != bot.nick.lower() and target.lower() not in bombs:
        return
    color, code = bombs.pop(target.lower())  # remove target from bomb list
    wirecut = trigger.group(2).rstrip(' ')
    if wirecut.lower() in ('all', 'all!', 'tots', 'tot', 'tot!', 'tots!', 'todo', 'todos'):
        sch.cancel(code)  # defuse timer, execute premature detonation
        kmsg = (u'KICK %s %s : Tallant TOTS els cables! *boom!!!* (Hauries d\'haver tallat el cable %s.)'
                % (trigger.sender, target, color))
        bot.write([kmsg])
    elif wirecut.capitalize() not in colors:
        bot.say(u'No trobo aquest cable, ' + target + u'! Vols dir que no has d\'anar a l\'oculista? Aquest cable no existeix!')
        bombs[target.lower()] = (color, code)  # Add the target back onto the bomb list,
    elif wirecut.capitalize() == color:
        bot.say(u'Molt bé, ' + target + u'! Has aconseguit desactivar la bomba abans de que explotés! Bona feina!!')
        sch.cancel(code)  # defuse bomb
    else:
        sch.cancel(code)  # defuse timer, execute premature detonation
        kmsg = 'KICK ' + trigger.sender + ' ' + target + \
               u' : No! No, aquest és el dolent. Aii, t\'has matat a tu mateix... ho sento (Haguessis hagut de triar el cable ' + color + ')'
        bot.write([kmsg])


def explode(bot, trigger):
    target = trigger.group(2)
    kmsg = 'KICK ' + trigger.sender + ' ' + target + \
           u' :Oh, vinga, ' + target + u'! Com a mínim ho haguessis pogut intentar! Ara estas mort.'
    bot.write([kmsg])
