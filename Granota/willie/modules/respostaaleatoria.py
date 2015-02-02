# -*- coding: utf-8 -*-
import willie
import random
@willie.module.commands('resposta', 'respon')
def ball(bot, trigger):
    """Fa una pregunta al bot, i et respon. Sintaxi: .respon <pregunta>"""
    messages = [u"Certament cert.",u"Sí senyor!",u"Sens dubte!",u"Sí, definitivament",u"Totalment d'acord!",u"Jo crec que sí",u"Segurament",u"No hi veig problemes...",u"Sí",u"Tot assenyala que sí",u"Buf! Torna-hi més tard.",u"Millor no t'ho dic ara...",u"Uf, tinc la bola màgica entelada.",u"M'has agafat per sorpresa, espera que em concentro... Torna-hi",u"No hi comptis",u"Jo crec que no",u"Jo de tu no ho faria",u"Dubto que que sigui cert",u"No sembla gaire bo...",u"Negativament negatiu."]
    answer = random.randint(0,len(messages))
    bot.say(messages[answer]);
