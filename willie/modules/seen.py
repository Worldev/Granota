# coding=utf8

from __future__ import unicode_literals

import datetime
import json
import time
from willie.tools import Ddict, get_timezone, format_time
from willie.module import commands, rule, priority, unblockable

seen_dict = "seen_dict.json"

@commands('seen', 'vist', 'visto')
def seen(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            bot.say(u"He vist per última vegada a \x02%s\x02 ara mateix a \x02%s\x02, dient \x1D%s\x0F" % (trigger.nick, trigger.sender, trigger.group(0)))
        elif bot.config.lang == 'es':
            bot.say(u"He visto por última vez a \x02%s\x02 ahora mismo en \x02%s\x02, diciendo \x1D%s\x0F" % (trigger.nick, trigger.sender, trigger.group(0)))
        else:
            bot.say(u"I last saw \x02%s\x02 right now on \x02%s\x02, saying \x1D%s\x0F" % (trigger.nick, trigger.sender, trigger.group(0)))
        return
    name = trigger.nick
    with open(seen_dict, "r") as f:
        data = json.load(f)
    if nick in data:
        timestamp = data[name]['timestamp']
        channel = data[name]['channel']
        message = data[name]['message']

        tz = get_timezone(bot.db, bot.config, None, trigger.nick,
                          trigger.sender)
        saw = datetime.datetime.utcfromtimestamp(timestamp)
        timestamp = format_time(bot.db, bot.config, tz, trigger.nick,
                                trigger.sender, saw)
        if bot.config.lang == 'ca':
            msg = u"He vist \x02%s\x02 per última vegada el dia \x02%s\x02 al canal \x02%s\x02, dient: \x1D%s\x0F" % (name, timestamp, channel, message)
        elif bot.config.lang == 'es':
            msg = u"He visto a \x02%s\x02 por última vez el día \x02%s\x02 en el canal \x02%s\x02, diciendo: \x1D%s\x0F" % (name, timestamp, channel, message)
        else:                                
            msg = u"I last saw \x02%s\x02 at \x02%s\x02 on \x02%s\x02, saying \x1D%s\x0F" % (name, timestamp, channel, message)
        bot.say(str(trigger.nick) + ': ' + msg)
    else:
        if bot.config.lang == 'ca':
            bot.say(u"No recordo haver vist a \x02%s\x02." % name)
        elif bot.config.lang == 'es':
            bot.say(u"No recuerdo haber visto a \x02%s\x02." % name)
        else:
            bot.say("Sorry, I haven't seen \x02%s\x02 around." % name)


@rule('(.*)')
@priority('low')
@unblockable # Also tracks ignored users
def note(bot, trigger):
    if trigger.sender.startswith("#"): # Only sees users that speak on public channels
        name = "test"
        try:
            with open(seen_dict, "r+") as f:
                data = json.load(f)
                data[name] = {}
                data[name]['timestamp'] = time.time()
                data[name]['channel'] = trigger.sender
                data[name]['message'] = trigger
                f.seek(0)  # rewind
                f.dump(data, f)
                f.truncate()                    
        except IOError:
            with open(seen_dict, "w+") as f:
                data = json.load(f)
                data[name] = {}
                data[name]['timestamp'] = time.time()
                data[name]['channel'] = trigger.sender
                data[name]['message'] = trigger
                f.seek(0)  # rewind
                f.dump(data, f)
                f.truncate()          
            
