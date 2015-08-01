from willie.module import commands, NOLIMIT
import datetime


@commands('countdown', 'comptenrere', 'cuentatras')
def generic_countdown(bot, trigger):
    """
    .countdown <year> <month> <day> - displays a countdown to a given date.
    """
    text = trigger.group(2)
    if not text:
        if bot.config.lang == 'ca':
            bot.reply(u"Utilitza el format correcte: .comptenrere 2018 12 19")
        elif bot.config.lang == 'es':
            bot.say(u"Utiliza el formato correcto: .cuentatras 2018 12 19")
        else:
            bot.say("Please use correct format: .countdown 2018 12 19")
        return NOLIMIT
    text = trigger.group(2).split()
    if text and (text[0].isdigit() and text[1].isdigit() and text[2].isdigit()
            and len(text) == 3):
        diff = (datetime.datetime(int(text[0]), int(text[1]), int(text[2]))
                - datetime.datetime.today())
        if bot.config.lang == 'ca':
            bot.say(str(diff.days) + " dies, " + str(diff.seconds / 60 / 60)
                       + " hores i "
                       + str(diff.seconds / 60 - diff.seconds / 60 / 60 * 60)
                       + " minuts per "
                       + text[0] + " " + text[1] + " " + text[2])
        elif bot.config.lang == 'es':
            bot.say(str(diff.days) + " dias, " + str(diff.seconds / 60 / 60)
                       + " horas y "
                       + str(diff.seconds / 60 - diff.seconds / 60 / 60 * 60)
                       + " minutos por "
                       + text[0] + " " + text[1] + " " + text[2])
        else:
            bot.say(str(diff.days) + " days, " + str(diff.seconds / 60 / 60)
                       + " hours and "
                       + str(diff.seconds / 60 - diff.seconds / 60 / 60 * 60)
                       + " minutes for "
                       + text[0] + " " + text[1] + " " + text[2])
    else:
        if bot.config.lang == 'ca':
            bot.reply(u"Utilitza el format correcte: .comptenrere 2018 12 19")
        elif bot.config.lang == 'es':
            bot.say(u"Utiliza el formato correcto: .cuentatras 2018 12 19")
        else:
            bot.say("Please use correct format: .countdown 2018 12 19")
        return NOLIMIT
