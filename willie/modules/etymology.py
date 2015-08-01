# -*- coding: cp1252 -*-
import re
from willie import web
from willie.module import commands, example, NOLIMIT

etyuri = 'http://etymonline.com/?term=%s'
etysearch = 'http://etymonline.com/?search=%s'

r_definition = re.compile(r'(?ims)<dd[^>]*>.*?</dd>')
r_tag = re.compile(r'<(?!!)[^>]+>')
r_whitespace = re.compile(r'[\t\r\n ]+')

abbrs = [
    'cf', 'lit', 'etc', 'Ger', 'Du', 'Skt', 'Rus', 'Eng', 'Amer.Eng', 'Sp',
    'Fr', 'N', 'E', 'S', 'W', 'L', 'Gen', 'J.C', 'dial', 'Gk',
    '19c', '18c', '17c', '16c', 'St', 'Capt', 'obs', 'Jan', 'Feb', 'Mar',
    'Apr', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'c', 'tr', 'e', 'g'
]
t_sentence = r'^.*?(?<!%s)(?:\.(?= [A-Z0-9]|\Z)|\Z)'
r_sentence = re.compile(t_sentence % ')(?<!'.join(abbrs))


def unescape(s):
    s = s.replace('&gt;', '>')
    s = s.replace('&lt;', '<')
    s = s.replace('&amp;', '&')
    return s


def text(html):
    html = r_tag.sub('', html)
    html = r_whitespace.sub(' ', html)
    return unescape(html).strip()


def etymology(word):
    # @@ <nsh> sbp, would it be possible to have a flag for .ety to get 2nd/etc
    # entries? - http://swhack.com/logs/2006-07-19#T15-05-29

    if len(word) > 25:
        if bot.config.lang == 'ca':
            raise ValueError("Paraula massa llarga: %s[...]" % word[:10])
        elif bot.config.lang == 'es':
            raise ValueError("Palabra demasiado larga: %s[...]" % word[:10])
        else:
            raise ValueError("Too long word: %s[...]" % word[:10])
    word = {'axe': 'ax/axe'}.get(word, word)

    bytes = web.get(etyuri % word)
    definitions = r_definition.findall(bytes)

    if not definitions:
        return None

    defn = text(definitions[0])
    m = r_sentence.match(defn)
    if not m:
        return None
    sentence = m.group(0)

    maxlength = 275
    if len(sentence) > maxlength:
        sentence = sentence[:maxlength]
        words = sentence[:-5].split(' ')
        words.pop()
        sentence = ' '.join(words) + ' [...]'

    sentence = '"' + sentence.replace('"', "'") + '"'
    return sentence + ' - ' + (etyuri % word)


@commands('ety', 'etymology', 'etimologia')
@example('word')
def f_etymology(bot, trigger):
    """Diu la etimologia d'una paraula"""
    word = trigger.group(2)

    try:
        result = etymology(word)
    except IOError:
        if bot.config.lang == 'ca':
            msg = "No puc conenctar-me amb etymonline.com (%s)" % (etyuri % word)
        elif bot.config.lang == 'es':
            msg = "No puedo conectarme con etymonline.com (%s)" % (etyuri % word)
        else:
            msg = "Can't connect to etymonline.com (%s)" % (etyuri % word)
        bot.msg(trigger.sender, msg)
        return NOLIMIT
    except AttributeError:
        result = None

    if result is not None:
        bot.msg(trigger.sender, result)
    else:
        uri = etysearch % word
        if bot.config.lang == 'ca':
            msg = """No he pogut trobar res per la paraula "%s". Intenta seguir l'enllaç: %s'""" % (word, uri)
        elif bot.config.lang == 'es':
            msg = """No he encontrado nada para "%s". Prueba con seguir ese enlace: %s'""" % (word, uri)
        else:
            msg = """I couldn't find anything for "%s". Try following this link: %s'""" % (word, uri)
        bot.msg(trigger.sender, msg)
        return NOLIMIT
