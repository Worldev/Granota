# -*- coding: utf8 -*-

import willie
import time

@willie.module.commands('custom')
def custom(bot, trigger):
    if not trigger.group(4):
        bot.reply("Bad syntax: .custom <action> <keyword> <msg>")
        return
    cmd = trigger.group(2).split()[0]
    key = trigger.group(4).split()[0]
    msg = trigger.group(5)
    bot.reply("cmd: %s key: %s msg: %s" % (cmd, key, msg))
    if not trigger.admin:
        bot.reply("You don't have permission")
        return
    if cmd == 'add':
        with open("custom_msgs.txt", "a") as f:
            f.write(key + "||||" + msg + '\n')
        bot.reply("Custom message succesfully added.")

@willie.module.commands('show')
def custom_show(bot, trigger):
    if not trigger.group(2):
        bot.reply("bad syntax: .show <keyword>")
        return
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