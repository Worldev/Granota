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
    colorlist = ["\x034","\x037","\x038","\x039","\x0311","\x0312","\x0313","\x036","\x034"]
    rainbowed = ""
    for letter in text:
        rainbowed += random.choice(colorlist) + letter
    bot.say(rainbowed.encode("utf8", "replace"))

@commands('cipher', 'xifra', 'cifra', 'rot13')
def encrypt(bot, trigger):
    bot.say(trigger.group(2).lower().encode('rot13'))
