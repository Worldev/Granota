# coding=utf-8
"""
translate.py - Willie Translation Module
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright © 2013, Elad Alfassa <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""

from willie import web
from willie.module import rule, commands, priority, example
import urllib2
import json
import random
import os

def translate(text, input='auto', output='en'):
    raw = False
    if output.endswith('-raw'):
        output = output[:-4]
        raw = True

    opener = urllib2.build_opener()
    opener.addheaders = [(
        'User-Agent', 'Mozilla/5.0' +
        '(X11; U; Linux i686)' +
        'Gecko/20071127 Firefox/2.0.0.11'
    )]

    input, output = urllib2.quote(input), urllib2.quote(output)
    try:
        if text is not text.encode("utf-8"):
            text = text.encode("utf-8")
    except:
        pass
    text = urllib2.quote(text)
    result = opener.open('http://translate.google.com/translate_a/t?' +
        ('client=t&sl=%s&tl=%s' % (input, output)) +
        ('&q=%s' % text)).read()

    while ',,' in result:
        result = result.replace(',,', ',null,')
        result = result.replace('[,', '[null,')
    data = json.loads(result)

    if raw:
        return str(data), 'en-raw'

    try:
        language = data[2]  # -2][0][0]
    except:
        language = '?'

    return ''.join(x[0] for x in data[0]), language


@rule(ur'$nickname[,:]\s+(?:([a-z]{2}) +)?(?:([a-z]{2}|en-raw) +)?["“](.+?)["”]\? *$')
@example('$nickname: "mon chien"? or $nickname: fr "mon chien"?')
@priority('low')
def tr(bot, trigger):
    """Tradueix una frase, en la llengua indicada. Sintaxi: NeoBot: <codi de llengua> "<frase>"?."""
    input, output, phrase = trigger.groups()

    phrase = phrase.encode('utf-8')

    if (len(phrase) > 350) and (not trigger.admin):
        return bot.reply(u'La frase ha de tenir menys de 350 caràcters.')

    input = input or 'auto'
    input = input.encode('utf-8')
    output = (output or 'ca').encode('utf-8')

    if input != output:
        msg, input = translate(phrase, input, output)
        if isinstance(msg, str):
            msg = msg.decode('utf-8')
        if msg:
            msg = web.decode(msg)  # msg.replace('&#39;', "'")
            msg = '"%s" (De %s a %s, translate.google.com)' % (msg, input, output)
        else:
            msg = u'La traducció de %s a %s ha fallat!' % (input, output)

        bot.reply(msg)
    else:
        bot.reply("Problemes amb l'idioma. Prova'n u altre!")


@commands('translate', 'tr', 'tradueix')
def tr2(bot, trigger):
    """Tradueix una frase a l'anglès."""
    command = trigger.group(2).encode('utf-8')

    def langcode(p):
        return p.startswith(':') and (2 < len(p) < 10) and p[1:].isalpha()

    args = ['auto', 'en']

    for i in xrange(2):
        if not ' ' in command:
            break
        prefix, cmd = command.split(' ', 1)
        if langcode(prefix):
            args[i] = prefix[1:]
            command = cmd
    phrase = command

    if (len(phrase) > 350) and (not trigger.admin):
        return bot.reply(u'La frase ha de tenir menys de 350 caràcters.')

    src, dest = args
    if src != dest:
        msg, src = translate(phrase, src, dest)
        if isinstance(msg, str):
            msg = msg.decode('utf-8')
        if msg:
            msg = web.decode(msg)  # msg.replace('&#39;', "'")
            msg = '"%s" (De %s a %s, translate.google.com)' % (msg, src, dest)
        else:
            msg = u'La traducció de %s a %s ha fallat!' % (src, dest)

        bot.reply(msg)
    else:
        bot.reply(u"Problemes amb l'idioma. Intenta-ho amb un altre")


def get_random_lang(long_list, short_list):
    random_index = random.randint(0, len(long_list) - 1)
    random_lang = long_list[random_index]
    if not random_lang in short_list:
        short_list.append(random_lang)
    else:
        return get_random_lang(long_list, short_list)
    return short_list
