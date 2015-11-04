from willie.module import commands

@commands('reverse', 'reves')
def reversetext(bot, trigger):
    if bot.config.lang == 'ca':
        """Retorna el text al revés."""
    elif bot.config.lang == 'es':
        """Retorna el texto al revés."""
    else
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
