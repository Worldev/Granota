# -*- coding: utf-8 -*-

from willie.module import commands
from random import choice, randint
from re import search
import sched
import time

allcolors = ['Red', 'Yellow', 'Blue', 'White', 'Black', 'Vermell', 'Groc', 'Blau', 'Blanc', 'Negre', 'Rojo', 'Amarillo', 'Azul', 'Blanco', 'Negro'] 
colors_en = ['Red', 'Yellow', 'Blue', 'White', 'Black'] 
colors_ca = ['Vermell', 'Groc', 'Blau', 'Blanc', 'Negre']
colors_es = ['Rojo', 'Amarillo', 'Azul', 'Blanco', 'Negro']
sch = sched.scheduler(time.time, time.sleep)
fuse = 120  # seconds
bombs = dict()


@commands('bomb', 'bomba')
def start(bot, trigger):
    """
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
            bot.say("Yes, sure!")
            return
        else:
            if bot.config.lang == 'ca':
                bot.say("Si home!")
            else:
                bot.say("Si hombre!")
            return
    if target in bombs:
        if trigger.group(1) == 'bomb':
            bot.say("I can't put another bomb to " + target + "!")
            return
        else:
            if bot.config.lang == 'ca':
                bot.say('No puc posar una altre bomba a ' + target + '!')
            else:
                bot.say("No puedo poner otra bomba a " + target + "!")
            return
    if trigger.group(1) == 'bomb':
        message = 'Hey, ' + target + '! Somebody has given you a bomb! You have 2 minutes and 5 wires: Red, Yellow, Blue, White and Black. What wire should I cut? Don\'t worry, I know what I\'m doing ! (answer with ".cutwire color")'
        bot.say(message)
        color = choice(colors_en)
        bot.msg(trigger.nick,
                   "Hey, don't tell it to %s, but is the %s one! "
                   "But sshhh! Don't tell it to anybody!" % (target, color))
        code = sch.enter(fuse, 1, explode_en, (bot, trigger))
        bombs[target.lower()] = (color, code)
        sch.run()
    else:
        if bot.config.lang == 'ca':
            message = 'Ei, ' + target + '! Sembla que algÃº t\'ha posat una bomba... Tens 2 minuts i 5 cables: Vermell, Groc, Blau, Blanc i Negre. Quin cable he de tallar? No pateixis, jo sÃ© el que em faig! (respon amb ".talla color")'
            bot.say(message)
            color = choice(colors_ca)
            bot.msg(trigger.nick,
                       "Ei, no li diguis a %s, perÃ² Ã©s el cable %s! "
                       "PerÃ² xxxt! No li diguis a ningÃº!" % (target, color))
            code = sch.enter(fuse, 1, explode_ca, (bot, trigger))
            bombs[target.lower()] = (color, code)
            sch.run()
        else:
            message = 'Ey, ' + target + '! Parece que alguien te ha puesto una bomba... Tienes 2 minutos y 5 cables: Rojo, Amarillo, Azul, Blanc y Negro. Que cable tengo que cortar? No te preocupes, yo se lo que hago! (responde con ".corta color")'
            bot.say(message)
            color = choice(colors_es)
            bot.msg(trigger.nick,
                       "Ey, no se lo digas a %s, pero es el cable %s! "
                       "Pero silencio! No se lo digas a nadie!" % (target, color))
            code = sch.enter(fuse, 1, explode_es, (bot, trigger))
            bombs[target.lower()] = (color, code)
            sch.run()

@commands('cutwire', 'talla', 'corta')
def cutwire(bot, trigger):
    """
    Talla el cable especificat quan algÃº et posa una bomba.
    """
    global bombs, colors_ca, colors_en, colors_es, allcolors
    target = trigger.nick
    if target.lower() != bot.nick.lower() and target.lower() not in bombs:
        return
    color, code = bombs.pop(target.lower())  # remove target from bomb list
    wirecut = trigger.group(2).rstrip(' ')
    if wirecut.lower() in ('all', 'all!', 'tots', 'tot', 'tot!', 'tots!', 'todo', 'todos'):
        sch.cancel(code)  # defuse timer, execute premature detonation
        if trigger.group(1) == 'cutwire':
            kmsg = ('KICK %s %s:Cutting ALL wires! *boom!!!* (You should cut the %s one.)'
                    % (trigger.sender, target, color))
        elif trigger.group(1) == 'talla':
            kmsg = ('KICK %s %s:Tallant TOTS els cables! *boom!!!* (Hauries d\'haver tallat el cable %s.)'
                    % (trigger.sender, target, color))
        else:
            kmsg = ('KICK %s %s:Cortando TODOS los cables! *boom!!!* (Tendrías que haber cortado el %s.)'
                    % (trigger.sender, target, color))
        bot.write([kmsg])
    elif wirecut.capitalize() not in allcolors:
        if trigger.group(1) == 'cutwire':
            bot.say('I don\'t see that wire, ' + target + '! That wire doesn\'t exist!')
        elif trigger.group(1) == 'talla':
            bot.say('No trobo aquest cable, ' + target + '! Vols dir que no has d\'anar a l\'oculista? Aquest cable no existeix!')
        else:
            bot.say('No encuentro ese cable, ' + target + '! Seguro que no tienes que ir al oculista? Ese cable no existe!')
        bombs[target.lower()] = (color, code)  # Add the target back onto the bomb list,
    elif wirecut.capitalize() == color:
        if trigger.group(1) == 'cutwire':
            bot.say('Well done, ' + target + '! You have defused the bomb before exploding!!')
        elif trigger.group(1) == 'talla':
            bot.say('Molt bÃ©, ' + target + '! Has aconseguit desactivar la bomba abans de que explotÃ©s! Bona feina!!')
        else:
            bot.say("Muy bien, " + target + "! Has conseguido desactivar la bomba antes de que explotara! Buen trabajo!!")
        sch.cancel(code)  # defuse bomb
    else:
        sch.cancel(code)  # defuse timer, execute premature detonation
        if trigger.group(1) == 'cutwire':
            kmsg = 'KICK ' + trigger.sender + ' ' + target + \
                   ' :No! No, that was the bad one. Ouch you have killed yourself... sorry (You should choose the ' + color + ' wire)'
        elif trigger.group(1) == 'talla':
            kmsg = 'KICK ' + trigger.sender + ' ' + target + \
                   ' :No! No, aquest Ã©s el dolent. Aii, t\'has matat a tu mateix... ho sento (Haguessis hagut de triar el cable ' + color + ')'
        else:
            kmsg = 'KICK ' + trigger.sender + ' ' + target + \
                   ' :No! No, ese es el malo. Ayy, te has matado a ti mismo... lo siento (Tendrias que haber cortado el cable ' + color + ')'
        bot.write([kmsg])

def explode_ca(bot, trigger):
    target = trigger.group(2)
    kmsg = 'KICK ' + trigger.sender + ' ' + target + \
           ' :Oh, vinga, ' + target + '! Com a mÃ­nim ho haguessis pogut intentar! Ara estas mort.'
    bot.write([kmsg])

def explode_en(bot, trigger):
    target = trigger.group(2)
    kmsg = 'KICK ' + trigger.sender + ' ' + target + \
           ' :Oh, come on, ' + target + '! You are now dead. D:'
    bot.write([kmsg])

def explode_es(bot, trigger):
    target = trigger.group(2)
    kmsg = 'KICK ' + trigger.sender + ' ' + target + \
           ' :Oh, venga, ' + target + '! Ahora estas muerto! D:'
    bot.write([kmsg])