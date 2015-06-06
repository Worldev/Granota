import willie

@willie.module.commands('saluda', 'hello', 'hola')
def helloworld(bot, trigger):
    if bot.config.lang == 'ca':
        hi = "Hola "
        if trigger.group(2):
            nick = trigger.group(2)
        else:
            nick = "a tots i a totes!"
    elif bot.config.lang == 'es':
        hi = "Hola "
        if trigger.group(2):
            nick = trigger.group(2)
        else:
            nick = "a todos y a todas!"
    else:
        hi = "Hello "
        if trigger.group(2):
            nick = trigger.group(2)
        else:
            nick = "everybody!"
    return
