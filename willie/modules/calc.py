# coding=utf-8

import re
from willie import web
from willie.module import commands, example
from willie.tools import eval_equation
from socket import timeout
import string
import HTMLParser


@commands('=', 'calcula', 'calculate', 'calc')
def c(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            return bot.reply("Res a calcular.")
        elif bot.config.lang == 'es':
            return bot.reply(u"Nada a calcular.")
        else:
            return bot.reply("Nothing to calculate.")
    try:
        result = str(eval_equation(trigger.group(2)))
    except ZeroDivisionError:
        if bot.config.lang == 'ca':
            result = u"La diviso entre zero no esta suportada en aquest univers."
        elif bot.config.lang == 'es':
            result = u"La division entre zero no esta soportada en ese universo."
        else:
            result = "Division by zero is not supported in this universe."
    except Exception:
        if bot.config.lang == 'ca':
            result = ("Ho sento, no puc calcular aixo amb aquesta ordre. "
                  "Potser en tinc un altre que pot fer-ho. "
                  "Escriu .ordres per una llista.")
        if bot.config.lang == 'es':
            result = ("Lo siento, pero no puedo calcular eso con ese comando. "
                  "Quizas tengo otro que si puede. "
                  "Escribe .comandos por una lista.")
        else:
            result = ("Sorry, I can't calculate that with this command. "
                      "I might have another one that can. "
                      "Use .commands for a list.")
    bot.reply(result)

@commands('wa', 'wolfram')
def wa(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            return bot.reply("Res per buscar. Sintaxi: .wa <paraula|frase|operacio|...>.")
        elif bot.config.lang == 'es':
            return bot.reply("Nada para buscar. Sintaxis: .wa <palabra|frase|operacion|...>.")
        else:
           return bot.reply("Nothing to search. Syntax: .wa <word|sentence|operation|...>.")     
    query = trigger.group(2)
    uri = 'http://tumbolia.appspot.com/wa/'
    try:
        answer = web.get(uri + web.quote(query.replace('+', '%2B')), 45)
    except timeout as e:
        if bot.config.lang == 'ca':
            return bot.say('[WOLFRAM ERROR] Temps d\'espera excedit.')
        elif bot.config.lang == 'es':
            return bot.say('[WOLFRAM ERROR] Tiempo de espera excedido.')
        else:
            return bot.say('[WOLFRAM ERROR] Request timed out')
    if answer:
        answer = answer.decode('string_escape')
        answer = HTMLParser.HTMLParser().unescape(answer)
        # This might not work if there are more than one instance of escaped
        # unicode chars But so far I haven't seen any examples of such output
        # examples from Wolfram Alpha
        match = re.search('\\\:([0-9A-Fa-f]{4})', answer)
        if match is not None:
            char_code = match.group(1)
            char = unichr(int(char_code, 16))
            answer = answer.replace('\:' + char_code, char)
        waOutputArray = string.split(answer, ";")
        if(len(waOutputArray) < 2):
            if(answer.strip() == "Couldn't grab results from json stringified precioussss."):
                # Answer isn't given in an IRC-able format, just link to it.
                if bot.config.lang == 'ca':
                    bot.say('[WOLFRAM] No hi ha cap resposta disponible. Prova amb http://www.wolframalpha.com/input/?i=' + query.replace(' ', '+'))
                elif bot.config.lang == 'es':
                    bot.say('[WOLFRAM] No hay ninguna respusta disponible. Prueba con http://www.wolframalpha.com/input/?i=' + query.replace(' ', '+'))
                else:
                    bot.say('[WOLFRAM] Couldn\'t display answer, try http://www.wolframalpha.com/input/?i=' + query.replace(' ', '+'))
            else:
                bot.say('[WOLFRAM ERROR]' + answer)
        else:

            bot.say('[WOLFRAM] ' + waOutputArray[0] + " = "
                    + waOutputArray[1])
        waOutputArray = []
    else:
        if bot.config.lang == 'ca':
            bot.reply(u"Sense resultats.")
        elif bot.config.lang == 'es':
            bot.repy(u"Sin resultados.")
        else:
            bot.reply('Sorry, no result.')


if __name__ == "__main__":
    from willie.test_tools import run_example_tests
    run_example_tests(__file__)
