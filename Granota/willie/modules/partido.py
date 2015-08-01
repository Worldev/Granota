import willie
import json
import urllib2

@willie.module.commands('partido')
def partido(bot, trigger):
    politico = trigger.group(2)

    # troll a dlcastc
    siguecontucamino = "consolito"
    if politico == "dlcastc":
        bot.say(politico + " ( http://enwp.org/es:Usuario:DLeandroc ) milita en el Partido de la Plaza Roja ( http://enwp.org/es:Plaza_Roja ) ")
    else:
        siguecontucamino = "ok"

    politicoParaTest = politico.decode("utf-8")
    politicoParaLink = politico.replace(" ", "%20")
    linkapiqueBusca = urllib2.urlopen("http://www.wikidata.org/w/api.php?action=wbsearchentities&search=" + politicoParaLink + "&language=es&format=json")
    eldearriba = "http://www.wikidata.org/w/api.php?action=wbsearchentities&search=" + politicoParaLink + "&language=es&format=json"
    todo = json.loads(linkapiqueBusca.read())
    nombrePolitico = todo["searchinfo"]["search"]
    bajoPolitico = nombrePolitico.replace(" ", "_")
    idWikidata = todo["search"][0]["id"]

    # ahora viene lo de conseguir la propiedad 120
    linkazoparaverlo = "http://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + idWikidata + "&format=json"
    linkapidelPolitico = urllib2.urlopen("http://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + idWikidata + "&format=json")
    tododelPolitico = json.loads(linkapidelPolitico.read())
    idParaAPI = '"' + idWikidata + '"'
    numeroPartido = tododelPolitico['entities'][idWikidata]['claims']['P102'][0]['mainsnak']['datavalue']['value']['numeric-id']
    linkWikipediaPersona = tododelPolitico['entities'][idWikidata]['sitelinks']['eswiki']['title']
    linkbajoWikipediaPersona = linkWikipediaPersona.replace(" ", "_")
    numerobuscaPartido = "Q" + str(numeroPartido)

    # ahora viene el partido político y sus links

    linkapidelPartido = urllib2.urlopen("http://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + numerobuscaPartido + "&languages=es&format=json")
    linkparaverapidelPartido = "http://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + numerobuscaPartido + "&languages=es&format=json"
    tododelPartido = json.loads(linkapidelPartido.read())
    linkWikipediaPartido = tododelPartido['entities'][numerobuscaPartido]['labels']['es']['value']
    linkbajoWikipediaPartido = linkWikipediaPartido.replace(" ", "_")  
    nombrePartido = tododelPartido['entities'][numerobuscaPartido]['labels']['es']['value'] 

    # para el print

    linkparaelprintPersona = "http://enwp.org/es:" + linkbajoWikipediaPersona
    linkparaelprintPartido = "http://enwp.org/es:" + linkbajoWikipediaPartido

    # el encode
    if siguecontucamino == "ok":
        bot.say(nombrePolitico + " ( " + linkparaelprintPersona + " )" + " milita en " + nombrePartido + " ( " + linkparaelprintPartido + " )")
    else:
        dontDoNothing = "meow"
