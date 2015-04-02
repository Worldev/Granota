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
@commands('help', 'ajuda')
@priority('low')
def help(bot, trigger):
    """T'ofereix ajuda per una ordre i, a vegades, un exemple"""
    if not trigger.group(2):
        bot.reply(u'Escriu .ajuda <ordre> (per exemple .help c) per obtindre ajuda per una ordre, o .ordres per una llista d\'ordres')
    else:
        name = trigger.group(2)
        name = name.lower()

        if name in bot.doc:
            bot.reply(bot.doc[name][0])
            if bot.doc[name][1]:
                bot.say('Ex. ' + bot.doc[name][1])

@commands('commands', 'ordres', 'o')
@priority('low')
def commands(bot, trigger):
    """Retorna una llista de les ordres disponibles en un missatge privat"""
    #ordres = """=, admins, ban, bots, choose, commands, countdown, d, debug_print, deop, devoice, diec, drae, ety, frase, g, galeta, gc, gcs, help, ip, isup, kick, kickban, length, link, lmgtfy, movie, op, pastis, pregaria, privs, py, quiet, recomana, ves, \x02join, part, quit, anunci, msg, me, recover\x02"""
    names = ', '.join(sorted(bot.doc.iterkeys()))
    bot.msg(trigger.sender, 'Ordres que entenc: ' + names + '.', max_messages=10)
    bot.reply("Per obtenir ajuda sobre una ordre en concret, escriu .ajuda <ordre>")

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
