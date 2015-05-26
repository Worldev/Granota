# -*- coding: utf8 -*-
import time
import os
import urllib2
from willie.modules.url import find_title
from willie.module import example, commands, rule, priority
from willie.tools import Ddict
import codecs


def configure(config):
    u"""
    | [meetbot] | example | purpose |
    | --------- | ------- | ------- |
    | meeting_log_path | /home/willie/www/meetings | Directori on guardar els registres de la reunió |
    | meeting_log_baseurl | http://example.com/~willie/meetings | Base URL for the meeting logs directory |
    """
    if config.option('Configure meetbot', False):
        if bot.config.lang == 'ca':
            config.interactive_add('meetbot', 'meeting_log_path', u"Directori on guardar els registres de la reunió.")
            config.interactive_add('meetbot', 'meeting_log_baseurl', "URL on desar els registres de la reunió (ex. http://example.com/logs).")
        elif bot.config.lang == 'es':
            config.interactive_add('meetbot', 'meeting_log_path', u"Directorio donde guardar el registro de las reuniones.")
            config.interactive_add('meetbot', 'meeting_log_baseurl', u"URL donde guardar los registros de la reunion".)
        else:
            config.interactive_add('meetbot', 'meeting_log_path', u"Path where you want to save the meeting log.")
            config.interactive_add('meetbot', 'meeting_log_baseurl', u"URL where you want to save the meeting log.")

meetings_dict = Ddict(dict)  # Saves metadata about currently running meetings
"""
meetings_dict is a 2D dict.

Each meeting should have:
channel
time of start
head (can stop the meeting, plus all abilities of chairs)
chairs (can add infolines to the logs)
title
current subject
comments (what people who aren't voiced want to add)

Using channel as the meeting ID as there can't be more than one meeting in a channel at the same time.
"""
meeting_log_path = ''  # To be defined on meeting start as part of sanity checks, used by logging functions so we don't have to pass them bot
meeting_log_baseurl = ''  # To be defined on meeting start as part of sanity checks, used by logging functions so we don't have to pass them bot
meeting_actions = {}  # A dict of channels to the actions that have been created in them. This way we can have .listactions spit them back out later on.


#Get the logfile name for the meeting in the requested channel
#Used by all logging functions
def figure_logfile_name(channel):
    if meetings_dict[channel]['title'] is 'Untitled meeting':
        name = 'untitled'
    else:
        name = meetings_dict[channel]['title']
    # Real simple sluggifying. This bunch of characters isn't exhaustive, but
    # whatever. It's close enough for most situations, I think.
    for c in ' ./\\:*?"<>|&*`':
        name = name.replace(c, '-')
    timestring = time.strftime('%Y-%m-%d-%H:%M', time.gmtime(meetings_dict[channel]['start']))
    filename = timestring + '_' + name
    return filename


#Start HTML log
def logHTML_start(channel):
    logfile = codecs.open(meeting_log_path + channel + '/' + figure_logfile_name(channel) + '.html', 'a', encoding='utf-8')
    timestring = time.strftime('%Y-%m-%d %H:%M', time.gmtime(meetings_dict[channel]['start']))
    title = '%s at %s, %s' % (meetings_dict[channel]['title'], channel, timestring)
    logfile.write('<!doctype html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>%TITLE%</title>\n</head>\n<body>\n<h1>%TITLE%</h1>\n'.replace('%TITLE%', title))
    logfile.write('<h4>Meeting started by %s</h4><ul>\n' % meetings_dict[channel]['head'])
    logfile.close()


#Write a list item in the HTML log
def logHTML_listitem(item, channel):
    logfile = codecs.open(meeting_log_path + channel + '/' + figure_logfile_name(channel) + '.html', 'a', encoding='utf-8')
    logfile.write('<li>' + item + '</li>\n')
    logfile.close()


#End the HTML log
def logHTML_end(channel):
    logfile = codecs.open(meeting_log_path + channel + '/' + figure_logfile_name(channel) + '.html', 'a', encoding='utf-8')
    current_time = time.strftime('%H:%M:%S', time.gmtime())
    logfile.write('</ul>\n<h4>Meeting ended at %s UTC</h4>\n' % current_time)
    plainlog_url = meeting_log_baseurl + urllib2.quote(channel + '/' + figure_logfile_name(channel) + '.log')
    logfile.write('<a href="%s">Full log</a>' % plainlog_url)
    logfile.write('\n</body>\n</html>')
    logfile.close()


#Write a string to the plain text log
def logplain(item, channel):
    current_time = time.strftime('%H:%M:%S', time.gmtime())
    logfile = codecs.open(meeting_log_path + channel + '/' + figure_logfile_name(channel) + '.log', 'a', encoding='utf-8')
    logfile.write('[' + current_time + '] ' + item + '\r\n')
    logfile.close()


#Check if a meeting is currently running
def ismeetingrunning(channel):
    try:
        if meetings_dict[channel]['running']:
            return True
        else:
            return False
    except:
        return False


#Check if nick is a chair or head of the meeting
def ischair(nick, channel):
    try:
        if nick.lower() == meetings_dict[channel]['head'] or nick.lower() in meetings_dict[channel]['chairs']:
            return True
        else:
            return False
    except:
        return False


#Start meeting (also preforms all required sanity checks)
@commands('startmeeting', 'reunio', 'reunion')
@example('.startmeeting title or .startmeeting')
def startmeeting(bot, trigger):
    """
    Start a meeting.
    https://github.com/embolalia/willie/wiki/Using-the-meetbot-module
    """
    if ismeetingrunning(trigger.sender):
        if bot.config.lang == 'ca':
            bot.say(u'Ja hi ha una reunió aquí!')
        elif bot.config.lang == 'es':
            bot.say(u'Ya hay una reunión en progreso aqui!')
        else:
            bot.say(u'There is already a meeting here!')
        return
    if not trigger.sender.startswith('#'):
        if bot.config.lang == 'ca':
            bot.say(u'Només puc començar reunions en canals')
        elif bot.config.lang == 'es':
            bot.say(u'Solo puedo comenzar una reunion en un canal')
        else:
            bot.say('Can only start meetings in channels')
        return
    if not bot.config.has_section('meetbot'):
        if bot.config.lang == 'ca':
            bot.say(u'El meetbot no està configurat. Assegura\'t de tenir el meeting_log_path i el meeting_log_baseurl definits.')
        elif bot.config.lang == 'es':
            bot.say(u'Meetbot no está configurado. Asegurate de tener el meeting_log_path y el meeting_log_baseurl definidos.')
        else:
            bot.say('Meetbot not configured, make sure meeting_log_path and meeting_log_baseurl are defined')
        return
    #Start the meeting
    meetings_dict[trigger.sender]['start'] = time.time()
    if not trigger.group(2):
        meetings_dict[trigger.sender]['title'] = 'Untitled meeting'
    else:
        meetings_dict[trigger.sender]['title'] = trigger.group(2)
    meetings_dict[trigger.sender]['head'] = trigger.nick.lower()
    meetings_dict[trigger.sender]['running'] = True
    meetings_dict[trigger.sender]['comments'] = []

    global meeting_log_path
    meeting_log_path = bot.config.meetbot.meeting_log_path
    if not meeting_log_path.endswith('/'):
        meeting_log_path = meeting_log_path + '/'
    global meeting_log_baseurl
    meeting_log_baseurl = bot.config.meetbot.meeting_log_baseurl
    if not meeting_log_baseurl.endswith('/'):
        meeting_log_baseurl = meeting_log_baseurl + '/'
    if not os.path.isdir(meeting_log_path + trigger.sender):
        try:
            os.makedirs(meeting_log_path + trigger.sender)
        except Exception as e:
            if bot.config.lang == 'ca':
                bot.say(u"No puc crear un directori pel registre d'aquest canal. La reunió no pot començar!")
            elif bot.config.lang == 'es':
                bot.say(u"No puedo crear un directorio para el registro de este canal. La reunión no puede empezar!")
            else:
                bot.say("Can't create log directory for this channel, meeting not started!")
            meetings_dict[trigger.sender] = Ddict(dict)
            raise
            return
    #Okay, meeting started!
    if bot.config.lang == 'ca':
        logplain(u'Reunió iniciada per ' + trigger.nick.lower(), trigger.sender)
        logHTML_start(trigger.sender)
        meeting_actions[trigger.sender] = []
        bot.say(u'La reunió ha començat! utilitza .action, .agreed, .info, .chairs, .subject i .comments per controlar la reunio. Al final, escriu .endmeeting')
        bot.say(u'Els usuaris sense permís per parlar poden utilitzar .comment '+trigger.sender+' seguit del comentari que volen fer en un missatge privat amb mi.')
    elif bot.config.lang == 'es':
        logplain(u'Reunión empezada por ' + trigger.nick.lower(), trigger.sender)
        logHTML_start(trigger.sender)
        meeting_actions[trigger.sender] = []
        bot.say(u'La reunion ha empezado! usa .action, .agreed, .info, .chairs, .subject y .comments para controlar la reunion. Al final, escribe .endmeeting')
        bot.say(u'Los usuarios sin permiso de hablar pueden usar .comment '+trigger.sender+' seguido de su comentario en un privado conmigo.')
    else:
        logplain('Meeting started by ' + trigger.nick.lower(), trigger.sender)
        logHTML_start(trigger.sender)
        meeting_actions[trigger.sender] = []
        bot.say('Meeting started! use .action, .agreed, .info, .chairs, .subject and .comments to control the meeting. to end the meeting, type .endmeeting')
        bot.say('Users without speaking permission can use .comment '+trigger.sender+' followed by their comment in a PM with me to vocalize themselves.')


#Change the current subject (will appear as <h3> in the HTML log)
@commands('subject')
@example('.subject roll call')
def meetingsubject(bot, trigger):
    """
    Change the meeting subject.
    https://github.com/embolalia/willie/wiki/Using-the-meetbot-module
    """
    if not ismeetingrunning(trigger.sender):
        if bot.config.lang == 'ca':
            bot.say(u'Abans has de començar la reunió')
        elif bot.config.lang == 'es':
            bot.say(u"Antes tienes que empezar la reunión')
        else:
            bot.say('Can\'t do that, start meeting first')
        return
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            bot.say(u"Sintaxi incorrecte! Utilitza .subject <tema de la reunió>")
        elif bot.config.lang == 'es':
            bot.say(u"Sintaxis incorrecta! Utiliza .subject <tema de la reunión>")
        else:
            bot.say('Bad syntax! Use .subject <meeting subject> instead.')
        return
    if not ischair(trigger.nick, trigger.sender):
        if bot.config.lang == 'ca':
            bot.say(u'No tens permisos per canviar el tema de la reunió')
        elif bot.config.lang == 'es':
            bot.say(u"No tienes permisos para cambiar el tema de la runión.')
        else:
            bot.say('Only meeting head or chairs can do that')
        return
    meetings_dict[trigger.sender]['current_subject'] = trigger.group(2)
    logfile = open(meeting_log_path + trigger.sender + '/' + figure_logfile_name(trigger.sender) + '.html', 'a')
    logfile.write('</ul><h3>' + trigger.group(2) + '</h3><ul>')
    logfile.close()
    if bot.config.lang == 'ca':
        logplain('Tema actual: ' + trigger.group(2) + ', (posat per ' + trigger.nick + ')', trigger.sender)
        bot.say('Tema actual: ' + trigger.group(2))
    elif bot.config.lang == 'es':
        logplain('Tema actual: ' + trigger.group(2) + ', (puesto por ' + trigger.nick + ')', trigger.sender)
        bot.say('Current subject: ' + trigger.group(2))
    else:
        logplain('Current subject: ' + trigger.group(2) + ', (set by ' + trigger.nick + ')', trigger.sender)
        bot.say('Current subject: ' + trigger.group(2))


#End the meeting
@commands('endmeeting')
@example('.endmeeting')
def endmeeting(bot, trigger):
    """
    End a meeting.
    https://github.com/embolalia/willie/wiki/Using-the-meetbot-module
    """
    if not ismeetingrunning(trigger.sender):
        if bot.config.lang == 'ca':
            bot.say(u"Inicia la reunió abans amb .startmeeting")
        elif bot.config.lang == 'es':
            bot.say(u"Empieza la reunión antes con .startmeeting")
        else:
            bot.say('Can\'t do that, start meeting first')
        return
    if not ischair(trigger.nick, trigger.sender):
        if bot.config.lang == 'ca':
            bot.say(u"No tens permisos per finalitzar la reunió.")
        elif bot.config.lang == 'es':
            bot.say(u"No tienes permisos para finalizar la reunión.")
        else:
            bot.say('Only meeting head or chairs can do that')
        return
    meeting_length = time.time() - meetings_dict[trigger.sender]['start']
    #TODO: Humanize time output
    if bot.config.lang == 'ca':
        bot.say(u"Reunió finalitzada! La reunió ha durat %d segons" % meeting_length)
        logHTML_end(trigger.sender)
        htmllog_url = meeting_log_baseurl + urllib2.quote(trigger.sender + '/' + figure_logfile_name(trigger.sender) + '.html')
        logplain(u'Reunió finalitzada per %s, segons totals: %d' % (trigger.nick, meeting_length), trigger.sender)
        bot.say(u'URL de la reunió: ' + htmllog_url)
    elif bot.config.lang == 'es':
        bot.say(u"Reunión acabada! ha durado %d segundos" % meeting_length)
        logHTML_end(trigger.sender)
        htmllog_url = meeting_log_baseurl + urllib2.quote(trigger.sender + '/' + figure_logfile_name(trigger.sender) + '.html')
        logplain(u'Reunión acabada por %s, y ha durado %d segundos' % (trigger.nick, meeting_length), trigger.sender)
        bot.say(u'URL de la reunión: ' + htmllog_url)
    else:    
        bot.say("Meeting ended! total meeting length %d seconds" % meeting_length)
        logHTML_end(trigger.sender)
        htmllog_url = meeting_log_baseurl + urllib2.quote(trigger.sender + '/' + figure_logfile_name(trigger.sender) + '.html')
        logplain('Meeting ended by %s, total meeting length %d seconds' % (trigger.nick, meeting_length), trigger.sender)
        bot.say('Meeting minutes: ' + htmllog_url)
        meetings_dict[trigger.sender] = Ddict(dict)
        del meeting_actions[trigger.sender]


#Set meeting chairs (people who can control the meeting)
@commands('chairs')
@example('.chairs Tyrope Jason elad')
def chairs(bot, trigger):
    """
    Set the meeting chairs.
    https://github.com/embolalia/willie/wiki/Using-the-meetbot-module
    """
    if not ismeetingrunning(trigger.sender):
        if bot.config.lang == 'ca':
            bot.say(u"Comença la reunió abans.")
        elif bot.config.lang == 'es':
            bot.say(u"Empieza la reunión antes.")
        else:
            bot.say('Can\'t do that, start meeting first')
        return
    if not trigger.group(2):
        bot.say('Syntax: .chair <nick>')
        return
    if trigger.nick.lower() == meetings_dict[trigger.sender]['head']:
        meetings_dict[trigger.sender]['chairs'] = trigger.group(2).lower().split(' ')
        chairs_readable = trigger.group(2).lower().replace(' ', ', ')
        logplain('Meeting chairs are: ' + chairs_readable, trigger.sender)
        logHTML_listitem('<span style="font-weight: bold">Meeting chairs are: </span>' + chairs_readable, trigger.sender)
        bot.say('Meeting chairs are: ' + chairs_readable)
    else:
        bot.say("Only meeting head can set chairs")


#Log action item in the HTML log
@commands('action')
@example('.action elad will develop a meetbot')
def meetingaction(bot, trigger):
    """
    Log an action in the meeting log
    https://github.com/embolalia/willie/wiki/Using-the-meetbot-module
    """
    if not ismeetingrunning(trigger.sender):
        bot.say('Can\'t do that, start meeting first')
        return
    if not trigger.group(2):
        bot.say('try .action someone will do something')
        return
    if not ischair(trigger.nick, trigger.sender):
        bot.say('Only meeting head or chairs can do that')
        return
    logplain('ACTION: ' + trigger.group(2), trigger.sender)
    logHTML_listitem('<span style="font-weight: bold">Action: </span>' + trigger.group(2), trigger.sender)
    meeting_actions[trigger.sender].append(trigger.group(2))
    bot.say('ACTION: ' + trigger.group(2))


@commands('listactions')
@example('.listactions')
def listactions(bot, trigger):
    for action in meeting_actions[trigger.sender]:
        bot.say('ACTION: ' + action)


#Log agreed item in the HTML log
@commands('agreed')
@example('.agreed Bowties are cool')
def meetingagreed(bot, trigger):
    """
    Log an agreement in the meeting log.
    https://github.com/embolalia/willie/wiki/Using-the-meetbot-module
    """
    if not ismeetingrunning(trigger.sender):
        bot.say('Can\'t do that, start meeting first')
        return
    if not trigger.group(2):
        bot.say('try .action someone will do something')
        return
    if not ischair(trigger.nick, trigger.sender):
        bot.say('Only meeting head or chairs can do that')
        return
    logplain('AGREED: ' + trigger.group(2), trigger.sender)
    logHTML_listitem('<span style="font-weight: bold">Agreed: </span>' + trigger.group(2), trigger.sender)
    bot.say('AGREED: ' + trigger.group(2))


#Log link item in the HTML log
@commands('link')
@example('.link http://example.com')
def meetinglink(bot, trigger):
    """
    Log a link in the meeing log.
    https://github.com/embolalia/willie/wiki/Using-the-meetbot-module
    """
    if not ismeetingrunning(trigger.sender):
        bot.say('Can\'t do that, start meeting first')
        return
    if not trigger.group(2):
        bot.say('try .action someone will do something')
        return
    if not ischair(trigger.nick, trigger.sender):
        bot.say('Only meeting head or chairs can do that')
        return
    link = trigger.group(2)
    if not link.startswith("http"):
        link = "http://" + link
    try:
        title = find_title(link)
    except:
        title = ''
    logplain('LINK: %s [%s]' % (link, title), trigger.sender)
    logHTML_listitem('<a href="%s">%s</a>' % (link, title), trigger.sender)
    bot.say('LINK: ' + link)


#Log informational item in the HTML log
@commands('info')
@example('.info all board members present')
def meetinginfo(bot, trigger):
    """
    Log an informational item in the meeting log
    https://github.com/embolalia/willie/wiki/Using-the-meetbot-module
    """
    if not ismeetingrunning(trigger.sender):
        bot.say('Can\'t do that, start meeting first')
        return
    if not trigger.group(2):
        bot.say('try .info some informative thing')
        return
    if not ischair(trigger.nick, trigger.sender):
        bot.say('Only meeting head or chairs can do that')
        return
    logplain('INFO: ' + trigger.group(2), trigger.sender)
    logHTML_listitem(trigger.group(2), trigger.sender)
    bot.say('INFO: ' + trigger.group(2))


#called for every single message
#Will log to plain text only
@rule('(.*)')
@priority('low')
def log_meeting(bot, trigger):
    if not ismeetingrunning(trigger.sender):
        return
    if trigger.startswith('.endmeeting') or trigger.startswith('.chairs') or trigger.startswith('.action') or trigger.startswith('.info') or trigger.startswith('.startmeeting') or trigger.startswith('.agreed') or trigger.startswith('.link') or trigger.startswith('.subject'):
        return
    logplain('<' + trigger.nick + '> ' + trigger, trigger.sender)


@commands('comment')
def take_comment(bot, trigger):
    """
    Log a comment, to be shown with other comments when a chair uses .comments.
    Intended to allow commentary from those outside the primary group of people
    in the meeting.

    Used in private message only, as `.comment <#channel> <comment to add>`
    https://github.com/embolalia/willie/wiki/Using-the-meetbot-module
    """
    target, message = trigger.group(2).split(None, 1)
    if trigger.sender[0] in '#&+!':
        return
    if not ismeetingrunning(target):
        bot.say("There's not currently a meeting in that channel.")
    else:
        meetings_dict[trigger.group(3)]['comments'].append((trigger.nick, message))
        bot.say("Your comment has been recorded. It will be shown when the"
                " chairs tell me to show the comments.")
        bot.msg(meetings_dict[trigger.group(3)]['head'], "A new comment has been recorded.")

@commands('comments')
def show_comments(bot, trigger):
    """
    Show the comments that have been logged for this meeting with .comment.
    https://github.com/embolalia/willie/wiki/Using-the-meetbot-module
    """
    if not ismeetingrunning(trigger.sender):
        return
    if not ischair(trigger.nick, trigger.sender):
        bot.say('Only meeting head or chairs can do that')
        return
    comments = meetings_dict[trigger.sender]['comments']
    if comments:
        msg = 'The following comments were made:'
        bot.say(msg)
        logplain('<%s> %s' % (bot.nick, msg), trigger.sender)
        for comment in comments:
            msg = '<%s> %s' % comment
            bot.say(msg)
            logplain('<%s> %s' % (bot.nick, msg), trigger.sender)
        meetings_dict[trigger.sender]['comments'] = []
    else:
        bot.say('No comments have been logged.')

