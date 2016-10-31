# coding=utf-8

import re
from willie import web
from willie.module import commands, example
from willie.tools import eval_equation
from socket import timeout
import string
import HTMLParser
import wolframalpha

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
        result = str(eval_equation(trigger.group(2).replace(',', '')))
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
    client = wolframalpha.Client(bot.config.wolframID)
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            return bot.reply("Res per buscar. Sintaxi: .wa <paraula|frase|operacio|...>.")
        elif bot.config.lang == 'es':
            return bot.reply("Nada para buscar. Sintaxis: .wa <palabra|frase|operacion|...>.")
        else:
           return bot.reply("Nothing to search. Syntax: .wa <word|sentence|operation|...>.")     
    query = trigger.group(2)
    res = client.query(query)
    answers = []
    for pod in res.pods:
        for sub in pod.subpods:
            answers.append(str(sub))
    answer = " - ".join(answers)
    if answer:
        bot.say("[WOLFRAM] " + answer)
    else:
        if bot.config.lang == 'ca':
            bot.reply(u"Sense resultats.")
        elif bot.config.lang == 'es':
            bot.repy(u"Sin resultados.")
        else:
            bot.reply('Sorry, no results.')


if __name__ == "__main__":
    from willie.test_tools import run_example_tests
    run_example_tests(__file__)
