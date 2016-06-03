# coding=utf-8

from willie.module import commands, example
import platform, sys, time
from os import path
import urllib, json

@commands('privs')
def privileges(bot, trigger):
    if trigger.group(2):
        try:
            bot.say(str(bot.privileges[trigger.group(2)]))
        except Exception:
            if bot.config.lang == 'ca':
                bot.reply("Canal desconegut.")
            elif bot.config.lang == 'es':
                bot.reply("Canal desconocido.")
            else:
                bot.reply("Channel not found.")
    else:
        bot.say(str(bot.privileges))

@commands('admins')
def admins(bot, trigger):
    owner = bot.config.core.owner
    admins = str(bot.config.core.get_list('admins'))
    bot.say("[Owner]"+owner+" [Admins]"+admins)

def git_info():
    repo = path.join(path.dirname(path.dirname(path.dirname(__file__))), '.git')
    head = path.join(repo, 'HEAD')
    if path.isfile(head):
        with open(head) as h:
            head_loc = h.readline()[5:-1]  # strip ref: and \n
        head_file = path.join(repo, head_loc)
        if path.isfile(head_file):
            with open(head_file) as h:
                sha = h.readline()
                if sha:
                    return sha
                else:
                    return ''

@commands("latest")
def get_latest_version(bot, trigger):
    web = urllib.urlopen("https://api.github.com/repos/Worldev/Granota/releases/latest").read()
    data = json.load(web)
    n = data['tag_name']
    bot.say(n)

@commands('version', 'versio')
def version(bot, trigger):
    version = '2.5-beta'
    if platform.system() == 'Linux':
        osver = ("%s %s" % (platform.linux_distribution()[0], platform.linux_distribution()[1]))
    elif platform.system() == 'Windows':
        osver = ("%s %s" % (platform.system(), platform.release()))
    else:
        osver = ("some OS which is not Linux or Windows")
    pyver = sys.version.split()[0]
    commit = git_info()
    if commit == '':
        commitinfo = ''
    else:
        commitinfo = ' (commit %s)' % commit
    if bot.config.lang == 'ca':
        bot.say(u"Sóc Granota, versió %s%s, en el sistema operatiu %s i utilitzant Python %s." % (version, commitinfo, osver, pyver))
    elif bot.config.lang == 'es':
        bot.say(u"Soy Granota, versión %s%s, en el sistema operativo %s y usando Python %s." % (version, commitinfo, osver, pyver))
    else:
        bot.say(u"I'm Granota, version %s%s, on %s and using Python %s." % (version, commitinfo, osver, pyver))

@commands('debug_print')
def debug_print(bot, trigger):
    version(bot, trigger)
    admins(bot, trigger)
    privileges(bot, trigger)

@commands('raiseException', 'causeProblems', 'giveError')
def cause_problems(bot, trigger):
    raise Exception("Problems were caused on command.")
