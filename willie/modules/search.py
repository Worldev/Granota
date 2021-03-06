# -*- coding: utf-8 -*-

import re
from willie import web
from willie.module import commands, example
import json
import time
from google import search as gsearch

def formatnumber(n):
    """Format a number with beautiful commas."""
    parts = list(str(n))
    for i in range((len(parts) - 3), 0, -3):
        parts.insert(i, ',')
    return ''.join(parts)

def google_search(query, lang):
    results = []
    for result in gsearch(query, lang=lang, stop=3):
	results.append(result)
    return results
	
@commands('g', 'google')
def g(bot, trigger):
    glogo = "\x0312G\x0304o\x0308o\x0312g\x0303l\x0304e\x0F: "
    query = trigger.group(2)
    if not query:
        return bot.reply('.g what?')
    results_list = google_search(query, bot.config.lang)
    if results_list:
        results = results_list[:3] # Get only the first 3 results to avoid flood and splitted urls (and the :3 emoji is nice too)
        results_str = " - ".join(results)		
        bot.say(glogo + results_str)
    elif uri is False:
        if bot.config.lang == 'ca':
            bot.reply("Error al connectar amb Google.")
        elif bot.config.lang == 'es':
            bot.reply("Error al conectar con Google.")
        else:
            bot.reply("Problem getting data from Google.")
    else:
        if bot.config.lang == 'ca':
            bot.reply("Cap resultat per '%s'." % query)
        elif bot.config.lang == 'es':
            bot.reply(u"Ningún resultado por '%s'." % query)
        else:
            bot.reply("No results found for '%s'." % query)
	

#@commands('gc')
#def gc(bot, trigger):
#    query = trigger.group(2)
#    if not query:
#        return bot.reply('.gc what?')
#    num = formatnumber(google_count(query))
#    bot.say(query + ': ' + num)

#r_query = re.compile(
#    r'\+?"[^"\\]*(?:\\.[^"\\]*)*"|\[[^]\\]*(?:\\.[^]\\]*)*\]|\S+'
#)


#@commands('gcs', 'comp')
#def gcs(bot, trigger):
#    if not trigger.group(2):
#        return bot.reply("Nothing to compare.")
#    queries = r_query.findall(trigger.group(2))
#    if len(queries) > 6:
#        if bot.config.lang == 'ca':
#            bot.reply(u"Només puc comparar fins a sis coses.")
#        elif bot.config.lang == 'es':
#            bot.reply(u"Sólo puedo comparar hasta seis cosas.")
#        else:
#            bot.reply('Sorry, can only compare up to six things.')
#        return

#    results = []
#    for i, query in enumerate(queries):
#        query = query.strip('[]')
#        n = int((formatnumber(google_count(query)) or '0').replace(',', ''))
#        results.append((n, query))
#        if i >= 2:
#            time.sleep(0.25)
#        if i >= 4:
#            time.sleep(0.25)

#    results = [(term, n) for (n, term) in reversed(sorted(results))]
#    reply = ', '.join('%s (%s)' % (t, formatnumber(n)) for (t, n) in results)
#    bot.say(reply)

r_bing = re.compile(r'<h3><a href="([^"]+)"')


def bing_search(query, lang='en-GB'):
    query = web.quote(query)
    base = 'http://www.bing.com/search?mkt=%s&q=' % lang
    bytes = web.get(base + query)
    m = r_bing.search(bytes)
    if m:
        return m.group(1)

r_duck = re.compile(r'nofollow" class="[^"]+" href="(.*?)">')


def duck_search(query):
    query = query.replace('!', '')
    query = web.quote(query)
    uri = 'http://duckduckgo.com/html/?q=%s&kl=uk-en' % query
    bytes = web.get(uri)
    m = r_duck.search(bytes)
    if m:
        return web.decode(m.group(1))


def duck_api(query):
    if '!bang' in query.lower():
        return 'https://duckduckgo.com/bang.html'

    uri = web.quote(query)
    uri = 'http://api.duckduckgo.com/?q=%s&format=json&no_html=1&no_redirect=1' % query
    results = json.loads(web.get(uri))
    print results
    if results['Redirect']:
        return results['Redirect']
    else:
        return None


@commands('duck', 'ddg')
def duck(bot, trigger):
    query = trigger.group(2)
    if not query:
        if bot.config.lang == 'ca':
            bot.reply("Error de sintaxi. Escriu .ddg <paraula a cercar>")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis. Escribe .ddg <palabra a buscar>")
        else:
            bot.reply("Syntax error. Use .ddg <word>")
        return
    
    #If the API gives us something, say it and stop
    result = duck_api(query)
    if result:
        bot.reply(result)
        return

    #Otherwise, look it up on the HTMl version
    uri = duck_search(query)

    if uri:
        bot.reply(uri)
        bot.memory['last_seen_url'][trigger.sender] = uri
    else:
        if bot.config.lang == 'ca':
            bot.reply("No s'han trobat resultats per '%s'." % query)
        elif bot.config.lang == 'es':
            bot.reply("No se han encontrado resultados para '%s'." % query)
        else:
            bot.reply("No results found for '%s'." % query)
        return


@commands('search', 'cerca', 'cercar', 'busca', 'buscar')
def search(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            bot.reply("Error de sintaxi. Escriu .cerca <paraula a cercar>")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis. Escribe .busca <palabra a buscar>")
        else:
            bot.reply("Syntax error. Use .search <word>")
        return
    
    query = trigger.group(2)
    gu = google_search(query, bot.config.lang)[0] or '-'
    du = duck_search(query) or '-'

    if (gu == du):
        result = '%s (Google, DuckDuckGo)' % gu
    else:
        if len(gu) > 250:
            gu = '(extremely long link)'
        if len(du) > 150:
            du = '(extremely long link)'
        result = '%s (Google), %s (DuckDuckGo)' % (gu, du)

    bot.reply(result)

@commands('suggest', 'suggereix', 'sugiere')
def suggest(bot, trigger):
    if not trigger.group(2):
	if bot.config.lang == 'ca':
            bot.reply("Error de sintaxi. Escriu .suggereix <paraula>")
	elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis. Escribe .sugiere <palabra>")
	else:
            bot.reply("Syntax error. User .suggest <word>")
	return
    query = trigger.group(2)
    uri = 'http://websitedev.de/temp-bin/suggest.pl?q='
    answer = web.get(uri + web.quote(query).replace('+', '%2B'))
    if answer:
    	bot.say(answer)
    else:
    	if bot.config.lang == 'ca':
    	    bot.reply("No hi ha resultats")
    	elif bot.config.lang == 'es':
            bot.reply("No hay resultados")
    	else:
            bot.reply('Sorry, no result.')
