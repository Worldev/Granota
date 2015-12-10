from willie.module import commands


@commands('lmgtfy', 'lmgify', 'gify', 'gtfy')
def googleit(bot, trigger):
    if not trigger.group(2):
        return bot.say('http://google.com/')
    bot.say('http://lmgtfy.com/?q=' + trigger.group(2).replace(' ', '+'))
