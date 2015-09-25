import willie
import json
import urllib2

@willie.module.commands('partido', 'partit', 'politician')
@willie.module.example(".politician Mariano Rajoy")
def partido(bot, trigger):
    politico = trigger.group(2)
    try:

        politicoParaTest = politico.decode("utf-8")
        politicoParaLink = politico.replace(" ", "%20")
        linkapiqueBusca = urllib2.urlopen("http://www.wikidata.org/w/api.php?action=wbsearchentities&search=" + politicoParaLink + "&language=%s&format=json" % bot.config.lang)
        eldearriba = ("http://www.wikidata.org/w/api.php?action=wbsearchentities&search=" + politicoParaLink + "&language=%s&format=json" % bot.config.lang)
        todo = json.loads(linkapiqueBusca.read())
        nombrePolitico = todo["searchinfo"]["search"]
        bajoPolitico = nombrePolitico.replace(" ", "_")
        idWikidata = todo["search"][0]["id"]

        linkazoparaverlo = "http://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + idWikidata + "&format=json"
        linkapidelPolitico = urllib2.urlopen("http://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + idWikidata + "&format=json")
        tododelPolitico = json.loads(linkapidelPolitico.read())
        idParaAPI = '"' + idWikidata + '"'
        numeroPartido = tododelPolitico['entities'][idWikidata]['claims']['P102'][0]['mainsnak']['datavalue']['value']['numeric-id']
        if bot.config.lang == 'ca':
            linkWikipediaPersona = tododelPolitico['entities'][idWikidata]['sitelinks']['cawiki']['title']
        elif bot.config.lang == 'es':
            linkWikipediaPersona = tododelPolitico['entities'][idWikidata]['sitelinks']['eswiki']['title']
        else:
            linkWikipediaPersona = tododelPolitico['entities'][idWikidata]['sitelinks']['enwiki']['title']
        linkbajoWikipediaPersona = linkWikipediaPersona.replace(" ", "_")
        numerobuscaPartido = "Q" + str(numeroPartido)

        linkapidelPartido = urllib2.urlopen("http://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + numerobuscaPartido + "&languages=es&format=json")
        linkparaverapidelPartido = "http://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + numerobuscaPartido + "&languages=es&format=json"
        tododelPartido = json.loads(linkapidelPartido.read())
        if bot.config.lang == 'ca':
            linkWikipediaPartido = tododelPartido['entities'][numerobuscaPartido]['labels']['ca']['value']
        elif bot.config.lang == 'es':
            linkWikipediaPartido = tododelPartido['entities'][numerobuscaPartido]['labels']['es']['value']
        else:
            linkWikipediaPartido = tododelPartido['entities'][numerobuscaPartido]['labels']['en']['value']
        linkbajoWikipediaPartido = linkWikipediaPartido.replace(" ", "_")
        if bot.config.lang == 'ca':
            nombrePartido = tododelPartido['entities'][numerobuscaPartido]['labels']['ca']['value']
        elif bot.config.lang == 'es':
            nombrePartido = tododelPartido['entities'][numerobuscaPartido]['labels']['es']['value']
        else:
            nombrePartido = tododelPartido['entities'][numerobuscaPartido]['labels']['en']['value']
        if bot.config.lang == 'es' or bot.config.lang == 'ca':
            linkparaelprintPersona = ("http://enwp.org/%s:%s" % (bot.config.lang, linkbajoWikipediaPersona))
            linkparaelprintPartido = ("http://enwp.org/%s:%s" % (bot.config.lang, linkbajoWikipediaPartido))
        else:
            linkparaelprintPersona = ("http://enwp.org/%s" % linkbajoWikipediaPersona)
            linkparaelprintPartido = ("http://enwp.org/%s" % linkbajoWikipediaPartido)
    
        if bot.config.lang == 'ca':
            bot.say(nombrePolitico + " (" + linkparaelprintPersona + ")" + " milita a " + nombrePartido + " (" + linkparaelprintPartido + ")")
        elif bot.config.lang == 'es':
            bot.say(nombrePolitico + " (" + linkparaelprintPersona + ")" + " milita en " + nombrePartido + " (" + linkparaelprintPartido + ")")
        else:
            bot.say(nombrePolitico + " (" + linkparaelprintPersona + ")" + " is a member of " + nombrePartido + " (" + linkparaelprintPartido + ")")
    except KeyError:
        if bot.config.lang == 'ca':
            bot.say("Aquest partit polític no existeix")
        elif bot.config.lang == 'es':
            bot.say("Este partido político no exsiste")
        else:
            bot.say("This political party has not been found")
    except AttributeError:
        if bot.config.lang == 'ca':
            bot.say("No hi ha res a cercar")
        elif bot.config.lang == 'es':
            bot.say("No hay nada a buscar")
        else:
            bot.say("There is nothing to search")
