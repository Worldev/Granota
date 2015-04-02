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

allcolors = ['Red', 'Yellow', 'Blue', 'White', 'Black', 'Vermell', 'Groc', 'Blau', 'Blanc', 'Negre'] 
colors_en = ['Red', 'Yellow', 'Blue', 'White', 'Black'] 
colors = ['Vermell', 'Groc', 'Blau', 'Blanc', 'Negre']
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
    if target == bot.nick or target == bot.config.owner:
        if trigger.group(1) == 'bomb':
            bot.say(u"Yes, sure!")
            return
        else:
            bot.say(u"Si home!")
            return
    if target in bombs:
        if trigger.group(1) == 'bomb':
            bot.say(u"I can't put another bomb to " + target + "!")
            return
        else:
            bot.say(u'No puc posar una altre bomba a ' + target + '!')
            return
    if trigger.group(1) == 'bomb':
        message = 'Hey, ' + target + u'! Somebody has given you a bomb! You have  2 minutes and 5 wires: Red, Yellow, Blue, White and Black. What wire should I cut? Don\'t worry, I know what I\'m doing ! (answer with ".cutwire color")'
        bot.say(message)
        color = choice(colors_en)
        bot.msg(trigger.nick,
                   u"Hey, don't tell it to %s, but is the %s one! "
                   u"But sshhh! Don't tell it to anybody!" % (target, color))
        code = sch.enter(fuse, 1, explode_en, (bot, trigger))
        bombs[target.lower()] = (color, code)
        sch.run()
    else:       
        message = 'Ei, ' + target + u'! Sembla que algÃº t\'ha posat una bomba... Tens  2 minuts i 5 cables: Vermell, Groc, Blau, Blanc i Negre. Quin cable he de tallar? No pateixis, jo sÃ© el que em faig! (respon amb ".talla color")'
        bot.say(message)
        color = choice(colors)
        bot.msg(trigger.nick,
                   u"Ei, no li diguis a %s, perÃ² Ã©s el cable %s! "
                   u"PerÃ² xxxt! No li diguis a ningÃº!" % (target, color))
        code = sch.enter(fuse, 1, explode, (bot, trigger))
        bombs[target.lower()] = (color, code)
        sch.run()

@commands('cutwire', 'talla')
def cutwire(bot, trigger):
    u"""
    Talla el cable especificat quan algÃº et posa una bomba.
    """
    global bombs, colors, colors_en, allcolors
    target = trigger.nick
    if target.lower() != bot.nick.lower() and target.lower() not in bombs:
        return
    color, code = bombs.pop(target.lower())  # remove target from bomb list
    wirecut = trigger.group(2).rstrip(' ')
    if wirecut.lower() in ('all', 'all!', 'tots', 'tot', 'tot!', 'tots!', 'todo', 'todos'):
        sch.cancel(code)  # defuse timer, execute premature detonation
        if trigger.group(1) == 'cutwire':
            kmsg = (u'KICK %s %s:Cutting ALL wires! *boom!!!* (You should cut the %s one.)'
                    % (trigger.sender, target, color))
        else:
            kmsg = (u'KICK %s %s:Tallant TOTS els cables! *boom!!!* (Hauries d\'haver tallat el cable %s.)'
                    % (trigger.sender, target, color))
        bot.write([kmsg])
    elif wirecut.capitalize() not in allcolors:
        if trigger.group(1) == 'cutwire':
            bot.say(u'I don\'t see that wire, ' + target + u'! That wire doesn\'t exist!')
        else:
            bot.say(u'No trobo aquest cable, ' + target + u'! Vols dir que no has d\'anar a l\'oculista? Aquest cable no existeix!')
        bombs[target.lower()] = (color, code)  # Add the target back onto the bomb list,
    elif wirecut.capitalize() == color:
        if trigger.group(1) == 'cutwire':
            bot.say(u'Well done, ' + target + u'! You have defused the bomb before exploding!!')
        else:
            bot.say(u'Molt bÃ©, ' + target + u'! Has aconseguit desactivar la bomba abans de que explotÃ©s! Bona feina!!')
        sch.cancel(code)  # defuse bomb
    else:
        sch.cancel(code)  # defuse timer, execute premature detonation
        if trigger.group(1) == 'cutwire':
            kmsg = 'KICK ' + trigger.sender + ' ' + target + \
                   u' :No! No, that was the bad one. Ouch you have killed yourself... sorry (You should choose the ' + color + ' wire)'
        else:
            kmsg = 'KICK ' + trigger.sender + ' ' + target + \
                   u' :No! No, aquest Ã©s el dolent. Aii, t\'has matat a tu mateix... ho sento (Haguessis hagut de triar el cable ' + color + ')'
        bot.write([kmsg])

def explode(bot, trigger):
    target = trigger.group(2)
    kmsg = 'KICK ' + trigger.sender + ' ' + target + \
           u' :Oh, vinga, ' + target + u'! Com a mÃ­nim ho haguessis pogut intentar! Ara estas mort.'
    bot.write([kmsg])

def explode_en(bot, trigger):
    target = trigger.group(2)
    kmsg = 'KICK ' + trigger.sender + ' ' + target + \
           u' :Oh, come on, ' + target + u'! You are now dead. D:'
    bot.write([kmsg])
