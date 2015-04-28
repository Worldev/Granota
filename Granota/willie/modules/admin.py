# coding=utf-8
"""
admin.py - Willie Admin Module
Copyright 2010-2011, Sean B. Palmer (inamidst.com) and Michael Yanovich
(yanovich.net)
Copyright © 2012, Elad Alfassa, <elad@fedoraproject.org>
Copyright 2013, Ari Koivula <ari@koivu.la>

Licensed under the Eiffel Forum License 2.

http://willie.dfbta.net
"""

import willie
import willie.module
from willie.module import commands
from willie import module

def configure(config):
    """
    | [admin] | example | purpose |
    | -------- | ------- | ------- |
    | hold_ground | False | Auto re-join on kick |
    """
    config.add_option('admin', 'hold_ground', u"Vols que torni a entrar que el facin fora d'un canal?")


@willie.module.commands('join', 'entra')
@willie.module.priority('low')
@willie.module.example('.entra #exemple')
def join(bot, trigger):
    u"""Entra al canal especificat. Només els administradors."""
    # Can only be done in privmsg by an admin
    if trigger.sender.startswith('#'):
        bot.reply(u"En privat, si us plau")
        return

    if trigger.admin:
        channel, key = trigger.group(2), trigger.group(3)
        if not channel:
            return
        elif not key:
            bot.join(channel)
        else:
            bot.join(channel, key)
    if not trigger.admin:
        if trigger.group(1) == 'join':
            bot.reply(u"You need admin rights.")
        else:
            bot.reply(u"No ets admin")
        return

@willie.module.commands('part', 'surt', 'sal')
@willie.module.priority('low')
@willie.module.example('.surt #exemple')
def part(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        if trigger.group(1) == 'join':
            bot.reply(u"You don't have admin rights")
        elif trigger.group(1) = 'sal':
            bot.reply(u"No eres admin")
        else:
            bot.reply(u"No ets admin")
        return
    """Deixa el canal especificat. Només els administrdors del bot."""
    # Can only be done in privmsg by an admin

    channel, _sep, part_msg = trigger.group(2).partition(' ')
    if part_msg:
        bot.part(channel, part_msg)
    else:
        bot.part(channel)


@willie.module.commands('quit')
@willie.module.priority('low')
def quit(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    if not trigger.owner:
        return
    """Es desconnecta del servidor. Només els administradors del bt"""
    # Can only be done in privmsg by the owner

    quit_message = trigger.group(2) + "[by " + trigger.nick + "]"
    if not quit_message:
        quit_message = u"Command "quit" performed by %s" % trigger.nick
    bot.quit(quit_message)


@willie.module.commands('msg')
@willie.module.priority('low')
@willie.module.example(u'.msg #exemple Hola! Que hi ha algú per aquí? :D')
def msg(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        return
    """
    Envia un missatge al canal especificat. Només pels administradors en un missatge privat.
    """

    channel, _sep, message = trigger.group(2).partition(' ')
    message = message.strip()
    if not channel or not message:
        return

    bot.msg(channel, message)


@willie.module.commands('me')
@willie.module.priority('low')
def me(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        return
    """
    Envia un missatge amb l'acció "/me" en el canal especificat. Només els administradors en missatge privat.
    """

    channel, _sep, action = trigger.group(2).partition(' ')
    action = action.strip()
    if not channel or not action:
        return

    msg = '\x01ACTION %s\x01' % action
    bot.msg(channel, msg)


@willie.module.event('INVITE')
@willie.module.rule('.*')
@willie.module.priority('low')
def invite_join(bot, trigger):
    if not trigger.admin:
        return
    """
    Entra en un canal on el bot està convidat.
    """
    bot.join(trigger.args[1])


@willie.module.event('KICK')
@willie.module.rule(r'.*')
@willie.module.priority('low')
def hold_ground(bot, trigger):
    """
    This function monitors all kicks across all channels willie is in. If it
    detects that it is the one kicked it'll automatically join that channel.

    WARNING: This may not be needed and could cause problems if willie becomes
    annoying. Please use this with caution.
    """
    if bot.config.has_section('admin') and bot.config.admin.hold_ground:
        channel = trigger.sender
        if trigger.args[1] == bot.nick:
            bot.join(channel)


@willie.module.commands('mode')
@willie.module.priority('low')
def mode(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        return
    """Set a user mode on Willie. Can only be done in privmsg by an admin."""

    mode = trigger.group(3)
    bot.write(('MODE ', bot.nick + '' + mode))


@willie.module.commands('set')
@willie.module.example('.set core.owner Me')
def set_config(bot, trigger):
    if trigger.sender.startswith('#'):
        bot.reply("Només funciona en un missatge privat.")
        return
    if not trigger.admin:
        bot.reply("Necessites ser administrador del bot.")
        return
    """See and modify values of willies config object.

    Trigger args:
        arg1 - section and option, in the form "section.option"
        arg2 - value

    If there is no section, section will default to "core".
    If value is None, the option will be deleted.
    """

    # Get section and option from first argument.
    arg1 = trigger.group(3).split('.')
    if len(arg1) == 1:
        section, option = "core", arg1[0]
    elif len(arg1) == 2:
        section, option = arg1
    else:
        bot.reply(u"Ús: .set secció.opció valor")
        return

    # Display current value if no value is given.
    value = trigger.group(4)
    if not value:
        if not bot.config.has_option(section, option):
            bot.reply("Option %s.%s does not exist." % (section, option))
            return
        # Except if the option looks like a password. Censor those to stop them
        # from being put on log files.
        if option.endswith("password") or option.endswith("pass"):
            value = "(password censored)"
        else:
            value = getattr(getattr(bot.config, section), option)
        bot.reply("%s.%s = %s" % (section, option, value))
        return

    # Otherwise, set the value to one given as argument 2.
    setattr(getattr(bot.config, section), option, value)


@willie.module.commands('save')
@willie.module.example('.save')
def save_config(bot, trigger):
    """Save state of willies config object to the configuration file."""
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        return
    bot.config.save()

@commands('nick', 'nom', 'nombre')
def nick(bot, trigger):
    if trigger.admin:
        bot.write(("NICK", trigger.group(2)))
    if not trigger.admin:
        return

if __name__ == '__main__':
    print __doc__.strip()
