# -*- coding: utf-8 -*-

from willie.module import commands
import random

@commands('reverse', 'reves')
def reversetext(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            bot.reply("Error de sintaxi. Escriu .reves <text>")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis. Escribe .reves <texto>")
        else:
            bot.reply("Syntax error. Type .reverse <text>")
        return
    text = trigger.group(2)
    bot.say(text[::-1])

@commands('rainbow', 'arcoiris', 'colores', 'colors')
def rainbow(bot, trigger):
    text = trigger.group(2)
    if not text:
        if bot.config.lang == 'ca':
            bot.reply("Error de sintaxi. Escriu .colors <text>")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis. Escribe .arcoiris <texto>")
        else:
            bot.reply("Syntax error. Type .rainbow <text>")
        return
    colorlist = ["\x034","\x037","\x038","\x039","\x0311","\x0312","\x0313","\x036","\x034"]
    rainbowed = ""
    for letter in text:
        rainbowed += random.choice(colorlist) + letter
    bot.say(rainbowed.encode("utf8", "replace"))

@commands('cipher', 'xifra', 'cifra', 'rot13')
def encrypt(bot, trigger):
    text = trigger.group(2)
    if not text:
        if bot.config.lang == 'ca':
            bot.reply("Error de sintaxi. Escriu .xifra <text>")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis. Escribe .cifra <texto>")
        else:
            bot.reply("Syntax error. Type .cipher <text>")
        return
    bot.say(text.encode('rot13'))
    
@commands('numchar')
def c_numchar(bot, trigger):
    text = trigger.group(2)
    if len(text) > 1:
        if bot.config.lang == 'ca':
            bot.say(u"Només accepto una sola lletra per aquest argument.")
        elif bot.config.lang == 'es':
            bot.say("Solo acepto una sola letra para ese argumento.")
        else:
            bot.say("I only accept one letter for this argument.")
        return
    numchar = lambda z: '0'*(3-len(str(z)))+str(z)
    if not text:
        if bot.config.lang == 'ca':
            bot.reply("Error de sintaxi. Escriu .numchar <text>")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis. Escribe .numchar <texto>")
        else:
            bot.reply("Syntax error. Type .numchar <text>")
        return
    bot.say(numchar(ord(text)))

@commands('tonum')
def c_tonum(bot, trigger):
    toNum = lambda z: ''.join(numchar(ord(z[i])) for i in range(len(z)))
    text = trigger.group(2)
    if text.isdigit() == True:
        if bot.config.lang == 'ca':
            bot.say(u"Només accepto text per aquesta ordre.")
        elif bot.config.lang == 'es':
            bot.say(u"Solo acepto texto  para ese comando.")
        else:
            bot.say("I only accept text for this command.")
        return      
    if not text:
        if bot.config.lang == 'ca':
            bot.reply("Error de sintaxi. Escriu .tonum <text>")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis. Escribe .tonum <texto>")
        else:
            bot.reply("Syntax error. Type .tonum <text>")
        return
    bot.say(toNum(text))

@commands('totext')
def c_totext(bot, trigger):
    toText = lambda z: ''.join(chr(int(z[i:i+3])) for i in range(0, len(z), 3))
    text = trigger.group(2)
    if not text:
        if bot.config.lang == 'ca':
            bot.reply("Error de sintaxi. Escriu .totext <text>")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis. Escribe .totext <texto>")
        else:
            bot.reply("Syntax error. Type .totext <text>")
        return
    try:
        bot.say(toText(text).decode('cp1252').encode("utf-8"))
    except ValueError:
        if bot.config.lang == 'ca':
            bot.say(u"Només accepto números més petits de 256 per aquesta ordre.")
        elif bot.config.lang == 'es':
            bot.say(u"Solo acepto números menores a 256 para ese comando.")
        else:
            bot.say("I only accept numbers smaller than 256 for this command.")
        return
