import willie
import json
import urllib2

@willie.module.commands('partido', 'partit', 'politician')
@willie.module.example(".politician Mariano Rajoy")
def partido(bot, trigger):
    politico = trigger.group(2)

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
    linkWikipediaPersona = tododelPolitico['entities'][idWikidata]['sitelinks']['eswiki']['title']
    linkbajoWikipediaPersona = linkWikipediaPersona.replace(" ", "_")
    numerobuscaPartido = "Q" + str(numeroPartido)

    linkapidelPartido = urllib2.urlopen("http://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + numerobuscaPartido + "&languages=es&format=json")
    linkparaverapidelPartido = "http://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + numerobuscaPartido + "&languages=es&format=json"
    tododelPartido = json.loads(linkapidelPartido.read())
    linkWikipediaPartido = tododelPartido['entities'][numerobuscaPartido]['labels']['es']['value']
    linkbajoWikipediaPartido = linkWikipediaPartido.replace(" ", "_")  
    nombrePartido = tododelPartido['entities'][numerobuscaPartido]['labels']['es']['value'] 

    linkparaelprintPersona = "http://enwp.org/es:" + linkbajoWikipediaPersona
    linkparaelprintPartido = "http://enwp.org/es:" + linkbajoWikipediaPartido

    bot.say(nombrePolitico + " ( " + linkparaelprintPersona + " )" + " milita en " + nombrePartido + " ( " + linkparaelprintPartido + " )")
