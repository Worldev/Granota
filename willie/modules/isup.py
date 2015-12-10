# -*- coding: utf-8 -*-
from willie import web
from willie.module import commands
import re

def is_http_url(s):
    if re.match('(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?',s):
        return True
    else:
        return False

@commands('isup')
def isup(bot, trigger):
    site = trigger.group(2)
    if not site:
        if bot.config.lang == 'ca':
            return bot.reply("Quina web vols que comprovi?")
        elif bot.config.lang == 'es':
            return bot.reply("Que web quieres que compruebe?")
        else:
            return bot.reply("What web do you want to check?")

    if 'localhost' in site or '127.0.0.1' in site or '0::1' in site:
        bot.reply("I'm minding on not say you it.")
        return
    elif site[:6] != 'http://' and site[:7] != 'https://':
        if '://' in site:
            protocol = site.split('://')[0] + '://'
            if bot.config.lang == 'ca':
                return bot.reply("Torna-ho a provar sense el %s" % protocol)
            elif bot.config.lang == 'es':
                return bot.reply("Vuelve a intentar sin el %s" % protocol)
            else:
                return bot.reply("Try it again without the %s" % protocol)
        else:
            if is_http_url(site) is False:
               return bot.reply("That URL looks not valid for me.")
            site = 'http://' + site
    try:
        response = web.get(site)
    except Exception:
        if bot.config.lang == 'ca':
            bot.say('Sembla que ' + site + ' no funciona o no existeix.')
        elif bot.config.lang == 'es':
            bot.say('Parece que ' + site + ' no funciona o no existe.')
        else:
            bot.say(site + ' looks down from here.')
        return

    if response:
        if bot.config.lang == 'ca':
            bot.say('No veig cap problema a ' + site)
        elif bot.config.lang == 'es':
            bot.say('No veo ningun problema en ' + site)
        else:
            bot.say(site + ' looks fine to me.')
    else:
        if bot.config.lang == 'ca':
            bot.say('Sembla que ' + site + ' no funciona o no existeix.')
        elif bot.config.lang == 'es':
            bot.say('Parece que ' + site + ' no funciona o no existe.')
        else:
            bot.say(site + ' looks down from here.')
        return
