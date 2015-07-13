# -*- coding: utf-8 -*-

import unicodedata
from willie.module import commands, example, NOLIMIT


@commands('u')
@example('.u 203D')
def codepoint(bot, trigger):
    arg = trigger.group(2).strip()
    if len(arg) == 0:
        if bot.config.lang == 'ca':
            bot.reply("Error de sintaxi. Escriu .u <caràcter>")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis. Utiliza .u <carácter>")
        else:
            bot.reply('Syntax error. Use .u <character>')
        return NOLIMIT
    elif len(arg) > 1:
        try:
            arg = unichr(int(arg, 16))
        except:
            if bot.config.lang == 'ca':
                bot.reply(u"Aquest no és un caràcter vàlid.")
            elif bot.config.lang == 'es':
                bot.reply(u"Ese no es un caracter válido.")
            else:
                bot.reply("That's not a valid code point.")
            return NOLIMIT

    # Get the hex value for the code point, and drop the 0x from the front
    point = str(hex(ord(u'' + arg)))[2:]
    # Make the hex 4 characters long with preceding 0s, and all upper case
    point = point.rjust(4, '0').upper()
    try:
        name = unicodedata.name(arg)
    except ValueError:
        if bot.config.lang == 'ca':
            return 'U+%s (No s\'ha trobat el nom)' % point
        elif bot.config.lang == 'es':
            return 'U+%s (No se ha encontrado el nombre)' % point
        else:
            return 'U+%s (No name found)' % point

    if not unicodedata.combining(arg):
        template = 'U+%s %s (%s)'
    else:
        template = 'U+%s %s (\xe2\x97\x8c%s)'
    bot.say(template % (point, name, arg))
