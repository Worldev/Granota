# -*- coding: utf-8 -*-

from willie.module import commands, rule, example, priority
import willie.config as config
import json

def configure(config):
        if config.lang == 'ca':
            config.interactive_add('core', 'project', u'Quin és el nom del teu projecte?',
                'Worldev')
            config.interactive_add('core', 'project_url',
                u'Quin és l\'url del teu projecte?', 'http://exemple.com')
        elif config.lang == 'es':
            config.interactive_add('core', 'project', u'¿Cuál es el nombre de tu proyecto?',
                'Worldev')
            config.interactive_add('core', 'project_url',
                u'¿Cuál es el url de tu proyecto?', 'http://ejemplo.com')
        else:
            config.interactive_add('core', 'project', u'What\'s the name of your project?',
                'Worldev')
            config.interactive_add('core', 'project_url',
                u'What\'s the url of your project?', 'http://exemple.com')

@rule('$nick' '(?i)(help|doc) +([A-Za-z]+)(?:\?+)?$')
@commands('help', 'ajuda', 'ayuda')
@priority('low')
def help(bot, trigger):
    if not trigger.group(2):
    	if bot.config.lang == 'ca':
    	    bot.reply(u'Escriu \x02{0}ajuda <ordre>\x02 (per exemple \x02{0}help wiki\x02) per obtindre ajuda per una ordre, o \x02{0}ordres\x02 per una llista d\'ordres'.format(bot.config.prefix.replace("\\", "")))
    	elif bot.config.lang == 'es':
    	    bot.reply(u'Escribe \x02{0}ayuda <orden>\x02 (por ejemplo \x02{0}ayuda wiki\x02) para obtener ayuda sobre un comando, o \x02{0}comandos\x02 para una lista de órdenes'.format(bot.config.prefix.replace("\\", "")))
    	else:
    	    bot.reply(u'Type \x02{0}help <command>\x02 (for example \x02{0}help wiki\x02) to get help about a command, or \x02{0}commands\x02 to get a list of commands.'.format(bot.config.prefix.replace("\\", "")))
    
    else:
        name = trigger.group(2).lower().replace(' ', '')
        l = bot.config.lang
        f = 'doc/alias.json'
        aliasfile = open(f, 'r')
        datalias = json.load(aliasfile)
        aliasfile.close()
        command = ""
        for i in datalias:
            if name in datalias[i]["alias"]:
                command = datalias[i]["alias"][0].lower()
        ff = 'doc/commands.json'
        helpfile = open(ff, 'r')
        data = json.load(helpfile)
        helpfile.close()
        if not command in list(data):
            if bot.config.lang == "ca":
            	doc = u"Ho sento, però aquesta ordre no existeix o encara no disposa de documentació."
            elif bot.config.lang == "es":
            	doc = u"Lo siento, pero ese comando no existe o aún no tiene documentación."
            else:
            	doc = "Sorry, but this command doesn't exist or doesn't have documentation yet."
        else:
	    if bot.config.lang == 'ca':
            	doc = "\x02%s\x02: %s | \x02Exemple\x02: %s | \x02Alies\x02 (oen altres idiomes): %s" % (command, data[command][l]["help"], bot.config.prefix.replace("\\", "") + data[command][l]["example"], ", ".join(datalias[command]["alias"]))
	    elif bot.config.lang == 'es':
		doc = "\x02%s\x02: %s | \x02Ejemplo\x02: %s | \x02Alias\x02 (o en otros idiomas): %s" % (command, data[command][l]["help"], bot.config.prefix.replace("\\", "") + data[command][l]["example"], ", ".join(datalias[command]["alias"]))
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
    cmds = listnames[:len(listnames)/2]
    cmdss = listnames[len(listnames)/2:]
    firstnames = ' '.join(cmds)
    secondnames = ' '.join(cmdss)
    if bot.config.lang == 'ca':
        bot.notice(trigger.nick, '\x02' + str(num) + ' ordres disponibles:\x02 ' + firstnames)
	bot.notice(trigger.nick, secondnames + '.')
        bot.reply("T'he enviat un missatge amb totes les meves ordres. Per obtenir ajuda sobre una ordre en concret, escriu \x02{0}ajuda <ordre>\x02".format(bot.config.prefix.replace("\\", "")))
        return
    elif bot.config.lang == 'es':
    	bot.notice(trigger.nick, '\x02' + str(num) + ' comandos disponibles:\x02 ' + firstnames)
	bot.notice(trigger.nick, secondnames + '.')
    	bot.reply("Te he enviado un mensaje con todos mis comandos. Para obtener ayuda sobre un comando en concreto, escribe \x02{0}ayuda <comando>\x02".format(bot.config.prefix.replace("\\", "")))
    	return
    else:
	bot.notice(trigger.nick, '\x02' + str(num) + ' available commands:\x02 ' + firstnames)
	bot.notice(trigger.nick, secondnames + '.')
	bot.reply("I've sent you a notice with all my commands. For help on a specific command, type \x02{0}help <command>\x02".format(bot.config.prefix.replace("\\", "")))
	return

@rule('$nick' r'(?i)(ajuda|ayuda|help)(?:[?!]+)?$')
@priority('low')
def help2(bot, trigger):
	if not bot.config.has_option("core", "project"):
		project = 'Worldev'
	if not bot.config.has_option("core", "project_url"):
		url = ''
	else:
		project = bot.config.project
		url = ' (' + bot.config.project_url + ')'
    	if bot.config.lang == 'ca':
    		response = (
    		'Hola, Sóc un bot del projecte {0}{1}. Escriu \x02{2}ordres\x02 per una llista d\'ordres. '.format(project, url, bot.config.prefix.replace("\\", "")) +
	        'El meu propietari és %s.'
	    % bot.config.owner)
	elif bot.config.lang == 'es':
    		response = (
	        'Hola, Soy un bot del proyecto {0}{1}. Escribe \x02{2}comandos\x02 por una lista de mis comandos. '.format(project, url, bot.config.prefix.replace("\\", "")) +
	        'Mi propietario es %s.'
	    ) % bot.config.owner
	else:
    		response = (
	        'Hi, I\'m a {0} project bot{1}. Type \x02{2}commands\x02 for a commands list. '.format(project, url, bot.config.prefix.replace("\\", "")) +
	        'My owner is %s.'
	    ) % bot.config.owner
		   
	bot.reply(response)

if __name__ == '__main__':
    print __doc__.strip()
