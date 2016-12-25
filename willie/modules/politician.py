# -*- coding: utf-8 -*-
import willie
import json
import urllib2

@willie.module.commands('partido', 'partit', 'politician')
def politician(bot, trigger):
    name = trigger.group(2)
    try:
        politician = name.replace(" ", "%20")
        search_api = urllib2.urlopen("http://www.wikidata.org/w/api.php?action=wbsearchentities&search=%s&language=%s&format=json" % (politician, bot.config.lang))
        search_data = json.loads(search_api.read())
        pol_name = search_data["searchinfo"]["search"]
        format_name = pol_name.replace(" ", "_")
        id = search_data["search"][0]["id"]

        api = urllib2.urlopen("http://www.wikidata.org/w/api.php?action=wbgetentities&ids=%s&format=json" % id)
        api_data = json.loads(api.read())
        entity = "Q" + str(api_data['entities'][id]['claims']['P102'][0]['mainsnak']['datavalue']['value']['numeric-id'])
        wiki = bot.config.lang + 'wiki' # Both bot language and wiki language codes are ISO. yay!
        wikilink = api_data['entities'][id]['sitelinks'][wiki]['title'].replace(" ", "_")
        
        api_link = urllib2.urlopen("http://www.wikidata.org/w/api.php?action=wbgetentities&ids=%s&languages=%s&format=json" % (entity, bot.config.lang))
        api_link_data = json.loads(api_link.read())
        wikilink_party = api_link_data['entities'][entity]['labels'][bot.config.lang]['value'].replace(" ", "_")
        party = api_link_data['entities'][entity]['labels'][bot.config.lang]['value']
        final_wikilink_party = ("http://enwp.org/%s:%s" % (bot.config.lang, wikilink_party))
    
        if bot.config.lang == 'ca':
            bot.say(pol_name + " (" + wikilink + ")" + " milita a " + party + " (" + final_wikilink_party + ")")
        elif bot.config.lang == 'es':
            bot.say(pol_name + " (" + wikilink + ")" + " milita en " + party + " (" + final_wikilink_party + ")")
        else:
            bot.say(pol_name + " (" + wikilink + ")" + " is member of " + party + " (" + final_wikilink_party + ")")
    except KeyError:
        if bot.config.lang == 'ca':
            bot.say(u"Aquest polític no existeix")
        elif bot.config.lang == 'es':
            bot.say(u"Este político no existe")
        else:
            bot.say(u"This politician doesn't exist")
    except AttributeError:
        if bot.config.lang == 'ca':
            bot.say(u"No hi ha res a cercar")
        elif bot.config.lang == 'es':
            bot.say(u"No hay nada a buscar")
        else:
            bot.say(u"There is nothing to search")
