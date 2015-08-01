import willie
import json
import urllib2

@willie.module.commands('partido')
@willie.module.example(".partido NeoMahler")
def partido(bot, trigger):
    politico = trigger.group(2)

    siguecontucamino = "consolito"
    if politico == "dlcastc":
        bot.say(politico + " ( http://enwp.org/es:Usuario:DLeandroc ) milita en el Partido de la Plaza Roja ( http://enwp.org/es:Plaza_Roja ) ")
        return
    elif politico == "ElGatoSaez":
        bot.say(politico + " ( http://enwp.org/es:Usuario:ElGatoSaez ) milita en el Partido del Mundo Gaturro ( http://enwp.org/es:Mundo_Gaturro ) ")
        return
    elif politico == "NeoMahler":
        bot.say(politico + " ( http://enwp.org/es:Usuario:Unapersona ) milita en el Partido del Basurero ( http://enwp.org/es:Basurero ) ")
        return
    elif politico == "JeDa":
        bot.say(politico + " ( http://enwp.org/es:Usuario:Jesushernandez9856 ) milita en el Partido del Internet Relay Chat ( http://enwp.org/es:Internet_Relay_Chat ) ")
        return
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

    if siguecontucamino == "ok":
        bot.say(nombrePolitico + " ( " + linkparaelprintPersona + " )" + " milita en " + nombrePartido + " ( " + linkparaelprintPartido + " )")
    else:
        dontDoNothing = "meow"
