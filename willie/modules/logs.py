import willie

willie.module.rule(".*")
willie.module.unblockable
willie.module.rate(0)
def log(bot, trigger):
    """Sends all command calls to the logging channel"""
    msg_command = "[LOG] %s (%s): %s"
    if trigger.group(0).startswith(bot.config.prefix.replace('\\', '')):
        bot.msg(bot.config.logging_channel, msg_command % trigger.nick, trigger.channel, trigger.group(0))
