import willie
import json
import os
import re
import shutil
import time

homedir = os.path.join(os.path.expanduser('~'), '.willie')

karmare = re.compile(r"^([a-zA-Z0-9\[\]\{\}\\\|\-\_\`^]*)(:?,? ?)?(\+\+|\-\-)")

try:
    shutil.copy2(homedir + '/karma.py', 'karma.py')
    import karma
    os.remove('karma.py')
except:
    karmas = {}
karmafilew = open(homedir + "/karma.py", "w")
def def_karmafile():
    karmafilew = karmafile

@willie.module.commands('karma')
def karma(bot, trigger):
    if trigger.group(2):
       user = trigger.group(2).lower()
    else:
       user = trigger.nick.lower()
    if trigger.group(2):
       oriuser = trigger.group(2)
    else:
       oriuser = trigger.nick
    try: 
       karmas[user]
    except:
       return bot.reply(oriuser + " never have been karmed!")
    bot.reply(oriuser + " has " + str(karmas[user]) + " of karma.")

@willie.module.rule(r".*")
def karmaman(bot, trigger):
    k = karmare.match(trigger.group(0))
    if k != None:
       if k.group(1).lower() == trigger.nick.lower():
           return bot.notice(trigger.nick, "You can't karma yourself.")

       try:
          karmas[k.group(1).lower()]
       except:
          karmas[k.group(1).lower()] = 0
       if k.group(3) == "++":
          karmas[k.group(1).lower()] += 1
          bot.notice(trigger.nick, "You have karmed up " + k.group(1) + ".")
       else:
          karmas[k.group(1).lower()] -= 1
          bot.notice(trigger.nick, "You have karmed down " + k.group(1) + ".")
       karmafilew.close()
       os.remove(homedir + "/karma.py")
       karmafile = open(homedir + "/karma.py", "w")
       karmafile.write("karmas = " + str(dict(karmas)))
       def_karmafile()
