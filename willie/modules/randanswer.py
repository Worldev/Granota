# -*- coding: utf-8 -*-
import willie
import random
@willie.module.commands('resposta', 'respon', 'answer', 'responde')
def ball(bot, trigger):
    """Fa una pregunta al bot, i et respon. Sintaxi: .respon <pregunta>"""
    if bot.config.lang == 'ca':
        messages = ["Certament cert.","Sí senyor!","Sens dubte!","Sí, definitivament","Totalment d'acord!","Jo crec que sí","Segurament","No hi veig problemes...","Sí","Tot assenyala que sí","Buf! Torna-hi més tard.","Millor no t'ho dic ara...","Uf, tinc la bola màgica entelada.","M'has agafat per sorpresa, espera que em concentro... Torna-hi","No hi comptis","Jo crec que no","Jo de tu no ho faria","Dubto que que sigui cert","No sembla gaire bo...","Negativament negatiu."]
    elif bot.config.lang == 'es':
        messages = ["Ciertamente cierto.", "Si señor!", "Sin duda!", "Si, definitivamente", "Totalmente de acuerdo!", "Yo creo que si", "Seguramente", "No veo ningun problema...", "Si", "Parece que si", "Uy, intenta mas tarde.", "Mejor no te lo digo ahora.", "Uy, tengo la bola mágica sucia.", "Me has cojido por sopresa, espera que me concentre... Intenta otra vez", "No cuentes con ello", "Yo creo que no", "Yo no lo haria", "Suso que sea cierto", "No parece muy bueno...", "Negativamente negativo"]
    else:
        messages = ["It is certain"," It is decidedly so","Without a doubt","Yes definitely","You may rely on it","As I see it yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","God says no","Very doubtful","Outlook not so good"]
    answer = random.randint(0,len(messages))
    bot.say(messages[answer]);
