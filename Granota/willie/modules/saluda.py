import willie

@willie.module.commands('saluda')
def helloworld(bot, trigger):
    bot.say('Hola a tots i a totes!')
