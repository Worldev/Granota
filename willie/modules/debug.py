# coding=utf-8

from willie.module import commands, example
import platform, sys, time

startTime = time.time()

@commands('privs')
def privileges(bot, trigger):
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
def admins(bot, trigger):
    owner = bot.config.core.owner
    admins = str(bot.config.core.get_list('admins'))
    bot.say("[Owner]"+owner+" [Admins]"+admins)

@commands('version', 'versio')
def version(bot, trigger):
    if platform.system() == 'Linux':
        ver = ("%s %s" % (platform.linux_distribution()[0], platform.linux_distribution()[1]))
    elif platform.system() == 'Windows':
        ver = ("%s %s" % (platform.system(), platform.release()))
    else:
        ver = ("some OS which is not Linux or Windows")
    pyver = sys.version.split()[0]
    bot.say("I'm Granota, version 1.0, running on %s and using Python %s since %s" % (ver, pyver, startTime))

@commands('debug_print')
def debug_print(bot, trigger):
    try:
        version(bot, trigger)
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
def cause_problems(bot, trigger):
    raise Exception("Problems were caused on command.")
