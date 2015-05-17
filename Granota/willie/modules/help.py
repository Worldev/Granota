# coding=utf-8
"""
help.py - Willie Help Module
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright © 2013, Elad Alfassa, <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""
from willie.module import commands, rule, example, priority


@rule('$nick' '(?i)(help|doc) +([A-Za-z]+)(?:\?+)?$')
@example('.help tell')
@commands('help', 'ajuda', 'ayuda')
@priority('low')
def help(bot, trigger):
    """T'ofereix ajuda per una ordre i, a vegades, un exemple"""
    if not trigger.group(2):
    	if bot.config.lang == 'ca':
    		bot.reply(u'Escriu .ajuda <ordre> (per exemple .help c) per obtindre ajuda per una ordre, o .ordres per una llista d\'ordres')
    	elif bot.config.lang == 'es':
    		bot.reply(u'Escribe .ayuda <orden> (por ejemplo .ayuda c) para obtener ayuda sobre un comando, o .comandos para una lista de órdenes')
    	else:
    		bot.reply(u'Write .help <command> (for example .help c) to get help about a command, or .commands to get a list of commands.')
    
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

@commands('commands', 'ordres', 'o')
@priority('low')
def commands(bot, trigger):
    """Retorna una llista de les ordres disponibles en un missatge privat"""
    #ordres = """=, admins, ban, bots, choose, commands, countdown, d, debug_print, deop, devoice, diec, drae, ety, frase, g, galeta, gc, gcs, help, ip, isup, kick, kickban, length, link, lmgtfy, movie, op, pastis, pregaria, privs, py, quiet, recomana, ves, \x02join, part, quit, anunci, msg, me, recover\x02"""
    names = ', '.join(sorted(bot.doc.iterkeys()))
    listnames = names.split()
    num = len(listnames)
    if trigger.group(1).startswith('commands'):
	bot.msg(trigger.sender, '\x02' + str(num) + ' avaiable commands:\x02 ' + names + '.', max_messages=10)
	bot.reply("For help on a specific command (in catalan), type .help <command>")
	return
    if trigger.group(1).startswith('ordres'):
        bot.msg(trigger.sender, '\x02' + str(num) + ' ordres disponibles:\x02 ' + names + '.', max_messages=10)
        bot.reply("Per obtenir ajuda sobre una ordre en concret, escriu .ajuda <ordre>")
    else:
    	bot.msg(trigger.sender, '\x02' + str(num) + ' ordres disponibles:\x02 ' + names + '.', max_messages=10)
    	bot.reply("Para obtener ayuda sobre un comando en concreto, escribe .ayuda <comando>")

@rule('$nick' r'(?i)ajuda(?:[?!]+)?$')
@priority('low')
def help2(bot, trigger):
    response = (
        u'Hola, Sóc un bot (Per si no ho sabies encara ;)). Escriu ".ordres" per una llista d\'ordres ' +
        u'o segueix el següent enllaç per més detalls: https://github.com/NeoMahler/Granota El meu propietari és el gran %s.'
    ) % bot.config.owner
    bot.reply(response)

if __name__ == '__main__':
    print __doc__.strip()
