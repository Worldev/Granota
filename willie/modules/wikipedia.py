# -*- coding: cp1252 -*-

from willie import web
from willie.module import NOLIMIT, commands, example, event
import json
import re

REDIRECT = re.compile(r'^REDIRECT (.*)')

def configure(config):
        if config.lang == 'ca':
            config.interactive_add('core', 'wiki_link', u'Url base del wiki',
                'http://ca.wikipedia.org/wiki/')
        elif config.lang == 'es':
            config.interactive_add('core', 'wiki_link', u'Url base del wiki',
                'http://es.wikipedia.org/wiki/')
        else:
            config.interactive_add('core', 'wiki_link', u'Base url of the wiki',
                'http://en.wikipedia.org/wiki/')


def mw_search(server, query, num, bot):
    """
    Searches the specified MediaWiki server for the given query, and returns
    the specified number of results.
    """
    search_url = ('http://%s/w/api.php?format=json&action=query'
                  '&list=search&srlimit=%d&srprop=timestamp&srwhat=text'
                  '&srsearch=') % (server, num)
    if bot.config.lang == 'ca' or bot.config.lang == 'es':
        search_url += web.quote(query.encode('utf-8'))
    else:
        search_url += web.quote(query.encode('cp1252'))
    query = json.loads(web.get(search_url))
    query = query['query']['search']
    return [r['title'] for r in query]


def mw_snippet(server, query, bot):
    """
    Retrives a snippet of the specified length from the given page on the given
    server.
    """
    if bot.config.lang == 'ca':
        snippet_url = ('https://ca.wikipedia.org/w/api.php?format=json'
                '&action=query&prop=extracts&exintro&explaintext'
                '&exchars=300&redirects&titles=')
    elif bot.config.lang == 'es':
        snippet_url = ('https://es.wikipedia.org/w/api.php?format=json'
                '&action=query&prop=extracts&exintro&explaintext'
                '&exchars=300&redirects&titles=')
    else:
        snippet_url = ('https://en.wikipedia.org/w/api.php?format=json'
                '&action=query&prop=extracts&exintro&explaintext'
                '&exchars=300&redirects&titles=')
    if bot.config.lang == 'ca' or bot.config.lang == 'es':
        snippet_url += web.quote(query.encode('utf-8'))
    else:
        snippet_url += web.quote(query.encode('cp1252'))
    snippet = json.loads(web.get(snippet_url))
    snippet = snippet['query']['pages']

    # For some reason, the API gives the page *number* as the key, so we just
    # grab the first page number in the results.
    snippet = snippet[snippet.keys()[0]]

    return snippet['extract']


@commands('w', 'wiki', 'wik')
def wikipedia(bot, trigger):
    query = trigger.group(2)
    if not query:
        if bot.config.lang == 'ca':
            bot.reply('Mmmmhhh... sóc un bot però no et puc llegir el pensament...')
        if bot.config.lang == 'es':
            bot.reply('Mmmmhhh... soy un bot pero no puedo leerte el pensamiento...')
        else:
            bot.reply('Mmmmhhh... I\'m a bot but I can\'t read your thoughts...')
        return NOLIMIT
    if bot.config.lang == 'ca':
        server = 'ca.wikipedia.org'
    elif bot.config.lang == 'es':
        server = 'es.wikipedia.org'
    else:
        server = 'en.wikipedia.org'
    query = mw_search(server, query, 1, bot)
    if not query:
        if bot.config.lang == 'ca':
            bot.reply("No he trobat res, encara no sóc perfecte ;)")
        elif bot.config.lang == 'es':
            bot.reply("No he encontrado nada, aun no soy perfecto ;)")
        else:
            bot.reply("I haven't found anything, I'm not perfect yet ;)")
        return NOLIMIT
    else:
        query = query[0]
    snippet = mw_snippet(server, query, bot)

    query = query.replace(' ', '_')
    if bot.config.lang == 'ca':
        bot.say('"%s" - http://ca.wikipedia.org/wiki/%s' % (snippet, query))
    elif bot.config.lang == 'es':
        bot.say('"%s" - http://es.wikipedia.org/wiki/%s' % (snippet, query))
    else:
        bot.say('"%s" - http://en.wikipedia.org/wiki/%s' % (snippet, query))

@event(".*\[\[.+\]\]")
def show_wikilink(bot, trigger):
    page = trigger.group(0).split('[[')[1].split(']]')[0]
    if not bot.config.wiki_link:
        link = 'https://%s.wikipedia.org/wiki/' % bot.config.lang
    else:
        link = bot.config.wiki_link
    bot.say(link + page)
