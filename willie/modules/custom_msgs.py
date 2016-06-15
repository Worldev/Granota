# -*- coding: utf8 -*-

import willie
import time

@willie.module.commands('info')
def custom(bot, trigger):
    try:
        cmd = trigger.group(2).split()[0]
        key = trigger.group(4).split("||")[0]
        msg = trigger.group(0).split("||")[1]
    except IndexError:
        if bot.config.lang == 'ca':
            bot.reply(u"Error de sintaxi: %sinfo <add|del> <paraula clau>||<missatge>" % bot.config.prefix.replace("\", ""))
            return
        elif bot.config.lang == 'es':
            bot.reply(u"Error de sintaxis: %sinfo <add|del> <palabra clave>||<mensaje>" % bot.config.prefix.replace("\", ""))
            return
        else:
            bot.reply("Syntax error: %sinfo <add|del> <keyword>||<message>" % bot.config.prefix.replace("\", ""))
            return        
    if not trigger.admin:
        if bot.config.lang == 'ca':
            bot.reply("No tens permisos")
            return
        elif bot.config.lang == 'es':
            bot.reply("No tienes permiso")
        else:
            bot.reply("You don't have permission")
            return
    if cmd == 'add':
        with open("custom_msgs.txt", "a") as f:
            f.write(key + "||||" + msg + '\n')
        if bot.config.lang == 'ca':
            bot.reply("Missatge afegit correctament.")
        elif bot.config.lang == 'es':
            bot.reply("Mensaje añadido correctamente.")
        else:
            bot.reply("Message succesfully added.")
    elif cmd == 'del':
        with open("custom_msgs.txt", "r+") as f:
            msgs = f.readlines()
            for msg in msgs:
                if msg.startswith(key):
                    msgs.remove(msg)
            f.seek(0)
            for msg in msgs:
                f.write(msg)
            f.truncate()
        if bot.config.lang == 'ca':
            bot.reply("Missatge esborrat correctament.")
        elif bot.config.lang == 'es':
            bot.reply("Mensaje borrado correctamente.")
        else:
            bot.reply("Message succesfully deleted.")

@willie.module.commands('show', 'mostra', 'muestra')
def custom_show(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            bot.reply(u"Error de sintaxi: %smostra <paraula clau>" % bot.config.prefix.replace("\", ""))
            return
        elif bot.config.lang == 'es':
            bot.reply(u"Error de sintaxis: %smuestra <palabra clave>" % bot.config.prefix.replace("\", ""))
            return
        else:
            bot.reply("Syntax error: %sshow <keyword>" % bot.config.prefix.replace("\", ""))
    key = trigger.group(2)
    with open("custom_msgs.txt", 'r') as f:
        lines = f.read().splitlines()
    for line in lines:
        print(line)
        if line.startswith(key):
            correct = line
            msg = correct.split("||||")[1]
            bot.say(msg)
            return
