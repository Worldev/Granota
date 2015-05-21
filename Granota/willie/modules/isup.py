# -*- coding: utf-8 -*-
from willie import web
from willie.module import commands


@commands('isup')
def isup(bot, trigger):
    """isup.me website status checker"""
    site = trigger.group(2)
    if not site:
        if bot.config.lang == 'ca':
            return bot.reply("Quina web vols que comprovi?")
        elif bot.config.lang == 'es':
            return bot.reply("Que web quieres que compruebe?")
        else:
            return bot.reply("What web do you want to check?")

    if site[:6] != 'http://' and site[:7] != 'https://':
        if '://' in site:
            protocol = site.split('://')[0] + '://'
            if bot.config.lang == 'ca':
                return bot.reply("Torna-ho a provar sense el %s" % protocol)
            elif bot.config.lang == 'es':
                return bot.reply("Vuelve a intentar sin el %s" % protocol)
            else:
                return bot.reply("Try it again without the %s" % protocol)
        else:
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

    if response
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
