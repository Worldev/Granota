# -*- coding: utf-8 -*-

import willie
import json
from willie import web
import time
import re
import urllib2

@willie.module.commands('ves', u'curt')
def ves(bot, trigger):
    if not trigger.group(2):
        bot.say(u'Quina adreça vols escurçar?')
        return
    link = trigger.group(2)
    url = 'http://ves.cat/?url=%s&format=json' % link
    if not link.startswith('http'):
        url = 'http://ves.cat/?url=http://%s&format=json' % link
    extracte = json.loads(web.get(url))
    linkcurt = extracte['link']
    bot.say(u"L'adreça escurçada de %s és %s" % (link, linkcurt))
