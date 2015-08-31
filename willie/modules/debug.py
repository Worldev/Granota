# coding=utf-8

from willie.module import commands, example

@commands('privs')
@example('.privs', '.privs #channel')
def privileges(bot, trigger):
    """Print the privileges of a specific channel, or the entire array."""
    if trigger.group(2):
        try:
            bot.say(str(bot.privileges[trigger.group(2)]))
        except Exception:
            if bot.config.lang == 'ca':
                bot.reply("Canal desconegut.")
            elif bot.config.lang == 'es':
                bot.reply("Canal desconocido.")
            else:
                bot.reply("Channel not found.")
    else:
        bot.say(str(bot.privileges))

@commands('admins')
@example('.admins')
def admins(bot, trigger):
    """Print the list of admins, including the owner."""
    owner = bot.config.core.owner
    admins = str(bot.config.core.get_list('admins'))
    bot.say("[Owner]"+owner+" [Admins]"+admins)

@commands('debug_print')
@example('.debug_print')
def debug_print(bot, trigger):
    """Calls version, admins and privileges prints in sequence."""
    try:
        willie.modules.version.version(bot, trigger)
    except Exception as e:
        if bot.config.lang == 'ca':
            bot.reply(u"Error al intentar obtenir la versio actual")
        elif bot.config.lang == 'es':
            bot.reply(u"Error al intentar obtener la version actual.")
        else:
            bot.say('An error occured trying to get the current version.')
    admins(bot, trigger)
    privileges(bot, trigger)

@commands('raiseException', 'causeProblems', 'giveError')
@example('.raiseException')
def cause_problems(bot, trigger):
    """This deliberately causes willie to raise exceptional problems."""
    raise Exception("Problems were caused on command.")
