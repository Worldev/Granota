# -*- coding: utf-8 -*-

from willie.module import commands

@commands('reverse', 'reves')
def reversetext(bot, trigger):
    if bot.config.lang == 'ca':
        u"""Retorna el text al revés."""
    elif bot.config.lang == 'es':
        u"""Retorna el texto al revés."""
    else:
        """Reverses a text"""
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
    """Speaks with rainbows."""
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
	if raintype == "chan":
    raintext = unicode(text, "utf8")
	for letter in text:
	    	rainbowed += random.choice(colorlist) + letter
	bot.say(rainbowed.encode("utf8", "replace"))
