# -*- coding: utf-8 -*-

import willie
import json
from willie import web
import re
import urllib2

@willie.module.commands('ves', u'curt', 'shorturl', 'acorta')
def ves(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            bot.reply(u'Error de sintaxi. Escriu .curt <url>')
        elif bot.config.lang == 'es':
            bot.reply(u'Error de sintaxis. Escribe .acorta <url>')
        else:
            bot.reply(u'Syntax error. Use .shorturl <url>')
        return
    link = trigger.group(2)
    url = 'http://ves.cat/?url=%s&format=json' % link
    if not link.startswith('http'):
        url = 'http://ves.cat/?url=http://%s&format=json' % link
    extracte = json.loads(web.get(url))
    linkcurt = extracte['link']
    if bot.config.lang == 'ca':
        bot.reply(u"L'adreça escurçada de %s és %s" % (link, linkcurt))
    elif bot.config.lang == 'es':
        bot.reply(u"El url acortado de %s és %s" % (link, linkcurt))
    else:
        bot.say(u"The short url of %s is %s" % (link, linkcurt))
