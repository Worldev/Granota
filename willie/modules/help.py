# -*- coding: utf-8 -*-
from willie.module import commands, rule, example, priority
import willie.config as config
import json


@rule('$nick' '(?i)(help|doc) +([A-Za-z]+)(?:\?+)?$')
@commands('help', 'ajuda', 'ayuda')
@priority('low')
def help(bot, trigger):
    if not trigger.group(2):
    	if bot.config.lang == 'ca':
    	    bot.reply(u'Escriu {0}ajuda <ordre> (per exemple {0}help c) per obtindre ajuda per una ordre, o {0}ordres per una llista d\'ordres'.format(bot.config.prefix.replace("\\", "")))
    	elif bot.config.lang == 'es':
    	    bot.reply(u'Escribe {0}ayuda <orden> (por ejemplo {0}ayuda c) para obtener ayuda sobre un comando, o {0}comandos para una lista de órdenes'.format(bot.config.prefix.replace("\\", "")))
    	else:
    	    bot.reply(u'Write {0}help <command> (for example {0}help c) to get help about a command, or {0}commands to get a list of commands.'.format(bot.config.prefix.replace("\\", "")))
    
    else:
        name = trigger.group(2).lower()
        l = bot.config.lang
        f = 'doc/alias.json'
        aliasfile = open(f, 'r')
        datalias = json.load(aliasfile)
        aliasfile.close()
        for i in datalias:
            if name in datalias[i]["alias"]:
                command = datalias[i]["alias"][0].lower()
                global command
        ff = 'doc/commands.json'
        helpfile = open(ff, 'r')
        data = json.load(helpfile)
        helpfile.close()
        if command not in list(data):
            if bot.config.lang == "ca":
            	doc = u"\x02%s\x02: Ho sento, però aquesta ordre no existeix o encara no disposa de documentació." % command
            elif bot.config.lang == "es":
            	doc = u"\x02%s\x02: Lo siento, pero ese comando no existe o aún no tiene documentación." % command
            else:
            	doc = "\x02%s\x02: Sorry, but this command doesn't exist or doesn't have documentation yet." % command
        else:
            doc = "\x02%s\x02: %s | \x02Example\x02: %s | \x02Alias\x02 (or in other languages): %s" % (command, data[command][l]["help"], bot.config.prefix.replace("\\", "") + data[command][l]["example"], ", ".join(datalias[command]["alias"]))
        bot.say(doc)
        
@commands('commands', 'ordres', 'o', 'comandos')
@priority('low')
def commands(bot, trigger):
    f = open('doc/alias.json', 'r')
    data = json.load(f)
    f.close()
    names = ', '.join(sorted(list(data)))
    listnames = names.split()
    num = len(listnames)
    if bot.config.lang == 'ca':
        bot.msg(trigger.sender, '\x02' + str(num) + ' ordres disponibles:\x02 ' + names + '.', max_messages=10)
        bot.reply("Per obtenir ajuda sobre una ordre en concret, escriu {0}ajuda <ordre>".format(bot.config.prefix.replace("\\", "")))
        return
    elif bot.config.lang == 'es':
    	bot.msg(trigger.sender, '\x02' + str(num) + ' comandos disponibles:\x02 ' + names + '.', max_messages=10)
    	bot.reply("Para obtener ayuda sobre un comando en concreto, escribe {0}ayuda <comando>".format(bot.config.prefix.replace("\\", "")))
    	return
    else:
	bot.msg(trigger.sender, '\x02' + str(num) + ' avaiable commands:\x02 ' + names + '.', max_messages=10)
	bot.reply("For help on a specific command, type {0}help <command>".format(bot.config.prefix.replace("\\", "")))
	return

@rule('$nick' r'(?i)(ajuda|ayuda|help)(?:[?!]+)?$')
@priority('low')
def help2(bot, trigger):
    if bot.config.lang == 'ca':
    	response = (
    		'Hola, Sóc un bot del projecte Worldev. Escriu "{0}ordres" per una llista d\'ordres '.format(bot.config.prefix.replace("\\", "")) +
	        'El meu propietari és %s.'
	    % bot.config.owner)
    elif bot.config.lang == 'es':
    	response = (
	        'Hola, Soy un bot del proyecto Worldev Escribe "{0}comandos" por una lista de mis comandos '.format(bot.config.prefix.replace("\\", "")) +
	        'Mi propietario es %s.'
	    ) % bot.config.owner
    else:
    	response = (
	        'Hi, I\'m a Worldev project bot. Write "{0}commands" for a commands list '.format(bot.config.prefix.replace("\\", "")) +
	        'My owner is %s.'
	    ) % bot.config.owner
	   
    bot.reply(response)

if __name__ == '__main__':
    print __doc__.strip()
