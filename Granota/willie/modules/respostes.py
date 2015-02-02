# coding=utf-8
"""
admin.py - Willie Admin Module
Copyright 2010-2011, Sean B. Palmer (inamidst.com) and Michael Yanovich
(yanovich.net)
Copyright © 2012, Elad Alfassa, <elad@fedoraproject.org>
Copyright 2013, Ari Koivula <ari@koivu.la>

Licensed under the Eiffel Forum License 2.

http://willie.dfbta.net
"""

import random, time
import willie

class respostes:
	def __init__(self):
		self.saludo=[
			[('M',u"Benvingut %s",1,0)],
		        [('M',u"Ei %s!",1,0)],
		        [('M',u"Bon dia %s",1,0)],
		        [('M',u"Bon dia",0,0)],
		        [('M',u"Allô",0,0)],
		        [('M',u"bip... bip... detectant un intrús al canal...",0,0)],
		        [('M',u"Ei tio, que passa?",0,0)],
		        [('M',u"Hello %s, how are you?",1,0)],
		        [('M',u"Hola %s, què tal?",1,0)],
		]
		self.adeu=[
			[('M',u'Adéu... que faré jo, sense tu? snif snif...',1,0)],
		        [('M',u"Adéu %s!",1,0)],
		        [('M',u"A reveure %s",1,0)],
		        [('M',u"Que vagi bé!",0,0)],
		        [('M',u"Cuida't!",0,0)],
		        [('M',u"Per fi marxa, aquest!",0,0)],
		        [('M',u"No em deixis sol amb aquesta colla de bandarres!",0,0)],
		        [('M',u"Au revoir!",1,0)],
		]
		self.resposta=[
			[('M',u"Et penses que et repondré? Bah!",0,0)],
			[('M',u"Digues, amor meu!",0,0)],
			[('M',u"Dieu algo?",0,0)],
			[('M',u"Vigila amb el que dius, que no saps qui sóc jo!",0,0)],
			[('M',u"Bah",0,0)],
			[('M',u"%s, per què dius això? No m'ofenguis!",1,0)],
			[('M',u"Aquí la bot-central. Digui?",0,0)],
			[('M',u"pssss (faig pipi)",0,0)],
			[('M',u"hola!",0,0)],
			[('M',u"Calla, que estic ocupat!",0,0)],
			[('M',u"No siguis burro!",1,0)],
			[('M',u"mmmmmhhh",0,0)],
			[('M',u"Tu creus?",0,0)],
			[('M',u"un segon",0,0)],
			[('M',u"hi hi hi",0,0)],
			[('A',u"està pensant en conxorxar-se amb altres bots i exterminar els humans",0,0)],
		]
		self.respowner=[		
			[('M',u"Potser...",0,0)],
			[('M',u"L'amo sap guiar-nos molt bé...",0,0)],
			[('M',u"Sí, amo, el que tu diguis.",0,0)],
			[('M',u"A la órden!",0,0)],
			[('M',u"per servir-lo",0,0)],
			[('M',u"servidor",0,0)],
			[('M',u"Senyor meu, m'omple de joia sentir el meu nom en el teu admirable discurs.",0,0)],
			[('M',u":)",0,0)],
			[('M',u"Els meus respectes, %s",1,0)],
			[('M',u"Oh, %s, és evident que us recolzaré sempre, en totes les vostres decisions!",1,0)],
			[('M',u"El jefe és un pesat, que algú el faci fora del xat!!! >:D",0,0)],
			[
				('M',u"Que poderosa és la veu del meu amo...",0,20),
				('M',u"Només una cosa: calla pesat! :P",0,0),
			],
		]
		self.error=[		
			[('M',u"Si et penses que t'ho diré, vs equivocat!",0,0)],
			[('M',u"Estic fent vaga, aixi que t'aguantes!",0,0)],
			[('M',u"Què t'has cregut? No sóc el teu esclau!",0,0)],
			[('M',u"Oops, crec que no t'ajudaré...",0,0)],
			[('M',u"Algo ha passa per aquí...",0,0)],
		]
		self.cafe=[
			[('M',u"No gràcies",0,0)],
			[('M',u"Amb molt sucre i molt llet",0,0)],
			[('M',u"Sí, si us plau",0,0)],
		]
		self.tabac=[
			[('M',u"He deixat de fumar, gràcies ;)",0,0)],
			[('M',u"Just avui, que he deixat de fumar...",0,0)],
			[('M',u"Dóna'm 2... paquets!",0,0)],
			[('M',u"Va, fumador social :)",0,0)],
		]
		self.porro=[
			[('M',u"Hi han coses irresistiblement irresistibles",0,0)],
		]
		self.birra=[
			[('M',u"Faré un esforç... per no veure-me'n dues gerres de 2 litres ;)",0,0)],
			[	('A',u"agafa una gera d'un litre i.... glub glub glub glub....",0,4), #elimine \001
				('A',u"deixa la botella buida a terra",0,7), #elimine \001
				('M',u"bbbbbbuuuuuuurrrRRRRRrrrppppppp",0,0),
                                ('M',u"Cambrer! Una de dos litres!",0,0)
			],
		]
		self.guapo=[
			[('M',u"gràcies",0,0)],
			[('M',u"i esbelt :)",0,0)],
			[('M',u"més que tu!",0,0)],
		]
		self.sexy=[
			[('M',u"gràcies",0,0)],
			[('M',u"^_^",0,0)],
			[('M',u"Et cases amb mi? :D!",0,0)],
		]
		self.llest=[
			[('M',u"Més que tu, cregut!",0,0)],
			[('M',u"gràcies",0,0)],
			[('A',u"et fa una reverència",0,0)],
		]
		"""
		self.variable=[
			[('M',u"texto",0,0)],
		]
		"""
		
	def respuesta(self,bot,trigger):
		"""
		Elige una frase de las que le pasemos y la dice con probabilidad que le digamos, las frases permiten respuestas dirigidas.
		TODO: Que funcione con mÃºltiples parÃ¡metros
		"""
		dado=random.randint(0,1)
		for i in respostes().__init__()[dado]:
			if i[2]==0: #La frase no tiene parÃ¡metros
				if i[0]=='M': #Mensaje
					#con.send_raw("PRIVMSG %s :%s" % (config.canal,i[1]))
					bot.say(i[1].encode('utf-8'))
				elif i[0]=='A': #Action (/me(
					#con.send_raw("PRIVMSG %s :\001ACTION %s\001" % (config.canal,i[1]))
					bot.write('ACTION', i[1].encode('utf-8'))
				elif i[0]=='N': #Notice
					#con.send_raw("NOTICE %s :%s" % (config.canal,i[1]))
					bot.write('NOTICE' + trigger.sender,i[1].encode('utf-8'))
			else:
				if i[0]=='M': #Mensaje
					bot.say(i[1].encode('utf-8'))
				elif i[0]=='A': #Action (/me)
					bot.write('ACTION', i[1].encode('utf-8'))
				elif i[0]=='N': #Notice
					bot.write('NOTICE' + trigger.sender,i[1].encode('utf-8'))
			time.sleep(i[3])


#Creo una instancia de los mÃ©todos pÃºblicos para que puedan ser llamados sin necesidad de instanciar la clase. 
_inst = respostes()
respuesta = _inst.respuesta
# Variables
adeu = _inst.adeu
saludo = _inst.saludo
resposta = _inst.resposta
error = _inst.error
cafe = _inst.cafe
tabac = _inst.tabac
porro = _inst.porro
birra = _inst.birra
guapo = _inst.guapo
sexy = _inst.sexy
llest = _inst.llest
respowner = _inst.respowner

if __name__ == '__main__':
    print "Clase "+__name__

