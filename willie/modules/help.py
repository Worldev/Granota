# -*- coding: utf-8 -*-
from willie.module import commands, rule, example, priority
import willie.config as config


@rule('$nick' '(?i)(help|doc) +([A-Za-z]+)(?:\?+)?$')
@example('help tell')
@commands('help', 'ajuda', 'ayuda')
@priority('low')
def help(bot, trigger):
    """T'ofereix ajuda per una ordre i, a vegades, un exemple"""
    if not trigger.group(2):
    	if bot.config.lang == 'ca':
    		bot.reply(u'Escriu {0}ajuda <ordre> (per exemple {0}help c) per obtindre ajuda per una ordre, o {0}ordres per una llista d\'ordres'.format(bot.config.prefix))
    	elif bot.config.lang == 'es':
    		bot.reply(u'Escribe {0}ayuda <orden> (por ejemplo {0}ayuda c) para obtener ayuda sobre un comando, o {0}comandos para una lista de órdenes'.format(bot.config.prefix))
    	else:
    		bot.reply(u'Write {0}help <command> (for example {0}help c) to get help about a command, or {0}commands to get a list of commands.'.format(bot.config.prefix))
    
    else:
        name = trigger.group(2)
        name = name.lower()

        if name in bot.doc:
            bot.reply(bot.doc[name][0])
            if bot.doc[name][1]:
            	if bot.config.lang == 'ca':
            		bot.say('Ex. ' + bot.doc[name][1])
            	if bot.config.lang == 'es':
            		bot.say('Ej. ' + bot.doc[name][1])
            	else:
            		bot.say('Eg. ' + bot.doc[name][1])

@commands('commands', 'ordres', 'o', 'comandos')
@priority('low')
def commands(bot, trigger):
    """Retorna una llista de les ordres disponibles en un missatge privat"""
    #ordres = """=, admins, ban, bots, choose, commands, countdown, d, debug_print, deop, devoice, diec, drae, ety, frase, g, galeta, gc, gcs, help, ip, isup, kick, kickban, length, link, lmgtfy, movie, op, pastis, pregaria, privs, py, quiet, recomana, ves, \x02join, part, quit, anunci, msg, me, recover\x02"""
    names = ', '.join(sorted(bot.doc.iterkeys()))
    listnames = names.split()
    num = len(listnames)
    if bot.config.lang == 'ca':
        bot.msg(trigger.sender, '\x02' + str(num) + ' ordres disponibles:\x02 ' + names + '.', max_messages=10)
        bot.reply("Per obtenir ajuda sobre una ordre en concret, escriu {0}ajuda <ordre>".format(bot.config.prefix))
        return
    elif bot.config.lang == 'es':
    	bot.msg(trigger.sender, '\x02' + str(num) + ' comandos disponibles:\x02 ' + names + '.', max_messages=10)
    	bot.reply("Para obtener ayuda sobre un comando en concreto, escribe {0}ayuda <comando>".format(bot.config.prefix))
    	return
    else:
	bot.msg(trigger.sender, '\x02' + str(num) + ' avaiable commands:\x02 ' + names + '.', max_messages=10)
	bot.reply("For help on a specific command, type {0}help <command>".format(bot.config.prefix))
	return

@rule('$nick' r'(?i)(ajuda|ayuda|help|hola|hello)(?:[?!]+)?$')
@priority('low')
def help2(bot, trigger):
    if bot.config.lang == 'ca':
	    response = (
	        'Hola, Sóc un bot del projecte CatBots. Escriu "{0}ordres" per una llista d\'ordres '.format(bot.config.prefix) +
	        'o segueix el següent enllaç per més detalls: https://wikicatbots.tk/wiki/Granota/ca. El meu propietari és %s.'
	    % bot.config.owner)
    elif bot.config.lang == 'es':
    	    response = (
	        'Hola, Soy un bot del proyecto CatBots. Escribe "{0}comandos" por una lista de mis comandos '.format(bot.config.prefix) +
	        'o sigue ese enlace para más detalles: https://wikicatbots.tk/wiki/Granota/es. Mi propietario es %s.'
	    ) % bot.config.owner
    else:
       	    response = (
	        'Hi, I\'m a CatBots project bot. Write "{0}commands" for a commands list '.format(bot.config.prefix) +
	        'or follow this links for more information: https://wikicatbots.tk/wiki/Granota. My owner is %s.'
	    ) % bot.config.owner
	   
    bot.reply(response)

if __name__ == '__main__':
    print __doc__.strip()
