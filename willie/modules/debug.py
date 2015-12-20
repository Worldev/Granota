# coding=utf-8

from willie.module import commands, example, calcuptime
import platform, sys, time

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

@commands("uptime")
def uptime(bot, trigger):
    now = calcuptime(time.time())
    if bot.config.lang == 'ca':
        bot.say("Porto %s hores despert." % now)
    elif bot.config.lang == 'es':
        bot.say("Llevo %s horas despierto." % now)
    else:
        bot.say("I have been running for %s hours." % now)
        
@commands('version', 'versio')
def version(bot, trigger):
    version = '1.0'
    if platform.system() == 'Linux':
        osver = ("%s %s" % (platform.linux_distribution()[0], platform.linux_distribution()[1]))
    elif platform.system() == 'Windows':
        osver = ("%s %s" % (platform.system(), platform.release()))
    else:
        osver = ("some OS which is not Linux or Windows")
    pyver = sys.version.split()[0]
    if bot.config.lang == 'ca':
        bot.say(u"Sóc Granota, versió %s, en el sistema operatiu %s i utilitzant Python %s." % (version, osver, pyver))
    elif bot.config.lang == 'es':
        bot.say(u"Soy Granota, versión %s, en el sistema operativo %s y usando Python %s." % (version, osver, pyver))
    else:
        bot.say(u"I'm Granota, version %s, on %s and using Python %s." % (version, osver, pyver))

@commands('debug_print')
def debug_print(bot, trigger):
    version(bot, trigger)
    uptime(bot, trigger)
    admins(bot, trigger)
    privileges(bot, trigger)

@commands('raiseException', 'causeProblems', 'giveError')
def cause_problems(bot, trigger):
    raise Exception("Problems were caused on command.")
