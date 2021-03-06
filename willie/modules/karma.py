# -*- coding: utf-8 -*-
import willie
import re

homedir = "config"

karmare = re.compile(r"^([a-zA-Z0-9\[\]\{\}\\\|\-\_\`^]*)(:?,? ?)?(\+\+|\-\-)")
    
try:
    from config.karma import karmas
except:
    karmas = {}
    
try:
    karmafilev = open(homedir + "/karma.py", "w")
    try:
        karmafilev.truncate()
    except:
        pass
    karmafilev.write("karmas = " + str(dict(karmas)))
    karmafilev.close()
except:
    pass
try:
    karmafilew = open(homedir + "/karma.py", "w")
except:
    raise Exception("I can't load karma file!")

@willie.module.commands('karma')
def karma(bot, trigger):
    if trigger.group(2):
        user = trigger.group(2).lower().replace(" ", "")
    else:
        user = trigger.nick.lower()
    if trigger.group(2):
        oriuser = trigger.group(2)
    else:
        oriuser = trigger.nick
    try: 
        karmas[user]
    except:
        if bot.config.lang == 'ca':
            return bot.reply(oriuser + " no ha rebut cap karma!")
        elif bot.config.lang == 'es':
            return bot.reply(oriuser + u" no ha recibido ningún karma!")
        else:
            return bot.reply(oriuser + " never have been karmed!")
    if bot.config.lang == 'ca':
        bot.reply(oriuser + u" t́e " + str(karmas[user]) + " punts de karma.")
    elif bot.config.lang == 'es':
        bot.reply(oriuser + u" tiene " + str(karmas[user]) + " puntos de karma.")
    else:
        bot.reply(oriuser + u" has " + str(karmas[user]) + " of karma.")
       
@willie.module.rule(r".*")
def karmaman(bot, trigger):
    k = karmare.match(trigger.group(0))
    if k != None and k.group(1).replace(" ", "") != "":
        if k.group(1).lower() == trigger.nick.lower():
            if bot.config.lang == 'ca':
                return bot.notice(trigger.nick, "No pots donar-te karma a tu mateix.")
            elif bot.config.lang == 'es':
                return bot.notice(trigger.nick, "No puedes darte karma a ti mismo.")
            else:
                return bot.notice(trigger.nick, "You can't karma yourself.")

        try:
            karmas[k.group(1).lower()]
        except:
            karmas[k.group(1).lower()] = 0
        if k.group(3) == "++":
            karmas[k.group(1).lower()] += 1
            if bot.config.lang == 'ca':
                bot.notice(trigger.nick, "Has donat un punt de karma a " + k.group(1) + ".")
            elif bot.config.lang == 'es':
                bot.notice(trigger.nick, "Has dado un punto de karma a " + k.group(1) + ".")
            else:
                bot.notice(trigger.nick, "You have karmed up " + k.group(1) + ".")
        else:
            karmas[k.group(1).lower()] -= 1
            if bot.config.lang == 'ca':
                bot.notice(trigger.nick, "Has tret un punt de karma a " + k.group(1) + ".")
            elif bot.config.lang == 'es':
                bot.notice(trigger.nick, "Has quitado un punto de karma a " + k.group(1) + ".")
            else:
                bot.notice(trigger.nick, "You have karmed down " + k.group(1) + ".")
        try:
            karmafilew.truncate()
        except:
            pass
        karmafilew.write("karmas = " + str(dict(karmas)))
