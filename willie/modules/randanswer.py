# -*- coding: utf-8 -*-
import willie
import random
@willie.module.commands('resposta', 'respon', 'answer', 'responde')
def ball(bot, trigger):
    """Fa una pregunta al bot, i et respon. Sintaxi: .respon <pregunta>"""
    if bot.config.lang == 'ca':
        messages = [u"Certament cert.",u"Sí senyor!",u"Sens dubte!",u"Sí, definitivament",u"Totalment d'acord!",u"Jo crec que sí",u"Segurament",u"No hi veig problemes...",u"Sí",u"Tot assenyala que sí",u"Buf! Torna-hi més tard.",u"Millor no t'ho dic ara...",u"Uf, tinc la bola màgica entelada.",u"M'has agafat per sorpresa, espera que em concentro... Torna-hi",u"No hi comptis",u"Jo crec que no",u"Jo de tu no ho faria",u"Dubto que que sigui cert",u"No sembla gaire bo...",u"Negativament negatiu."]
    elif bot.config.lang == 'es':
        messages = [u"Ciertamente cierto.", u"Si señor!", u"Sin duda!", u"Si, definitivamente", u"Totalmente de acuerdo!", u"Yo creo que si", u"Seguramente", "No veo ningun problema...", u"Si", u"Parece que si", "Uy, intenta mas tarde.", "Mejor no te lo digo ahora.", u"Uy, tengo la bola mágica sucia.", "Me has cojido por sopresa, espera que me concentre... Intenta otra vez", "No cuentes con ello", "Yo creo que no", "Yo no lo haria", "Suso que sea cierto", "No parece muy bueno...", "Negativamente negativo"]
    else:
        messages = ["It is certain"," It is decidedly so","Without a doubt","Yes definitely","You may rely on it","As I see it yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","God says no","Very doubtful","Outlook not so good"]
    answer = random.randint(0,len(messages))
    bot.say(messages[answer]);
