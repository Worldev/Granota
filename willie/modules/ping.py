# -*- coding: utf-8 -*-
from willie import module
from willie.module import commands
import random
import re

normal_ping_ca = [u"Et penses que et repondré? Bah!",u"Digues, amor meu!",
                 u"Dieu algo?",u"Vigila amb el que dius, que no saps qui sóc jo!",
                 u"Bah",u"Per què dius això? No m'ofenguis!",u"Aquí la bot-central. Digui?",
                 u"pfffff",u"hola!",u"Calla, que estic ocupat!",u"No siguis burro!",
                 u"mmmmmhhh",u"Tu creus?",u"un segon",u"hi hi hi",
                 u"Al món hi ha 10 tipus de bot: els que saben binari i els que no.",
                 u"Al món hi ha 3 tipus de bot: els que saben comptar i els que no.",
                 u"Calculant l'última xifra del nombre pi. Esperi si us plau...",
                 u"Últimes notícies: La tecla 'Control' ha detingut la tecla 'Escape' que ha quedat sota custòdia de la tecla 'Bloquejar Desplaçament'.",
                 u"Un hotel infinit ple pot acollir infinits clients més. Però un bot infinitament perfecte (Com jo) pot respondre a les teves peticions *finites*.",
                 u"Carpe diem et quid pro quo ut non habeas corpus mutatis mutandis.",
                 u"Menteixes quan dius que menteixes?",
                 u"Ho diuen les enquestes: cinc de cada deu bots... són la meitat.",
                 u"Jo mai oblido un nick... però en el teu cas faré una excepció.",
                 u"[<Espai reservat per a publicitat>]"]
owner_ping_ca = [u"Totalment d'acord!",u"L'amo sap guiar-nos molt bé...",
               u"Sí, amo, el que tu diguis.",u"A la órden!",
               u"per servir-lo",u"servidor",u"Senyor meu, m'omple de joia sentir el meu nom en el teu admirable discurs.",
               u":)",u"Els meus respectes, majestat",
               u"Oh, majestat, és evident que us recolzaré sempre, en totes les vostres decisions!",
               u"El jefe és un pesat, que algú el faci fora del xat!!! >:D",
               u"Un favor personal... dona els privilegis d'owner a algú altre!"]
               
normal_ping_es = [u"¿Crees que te responderé? ¡Bah!",u"¡Di, mi amor!",
                 u"¿Dijeron algo?",u"Vigila con lo que dices, que no sabes quien soy yo!",
                 u"Bah",u"¿Por qué dices eso? ¡No me ofendas!",u"Aquí la bot-central. ¿Diga?",
                 u"pffff",u"hola!",u"Cállate, que estoy ocupado!",u"No seas tonto!",
                 u"mmmmmhhh",u"¿Tu crees?",u"un segundo",u"ji ji ji",
                 u"En el mundo hay 10 tipos de bot: los que saben binario y los que no.",
                 u"En el mundo hay 3 tipos de bot: los que saben contar y los que no.",
                 u"Calculando el último decimal del número pi. Espere por favor...",
                 u"Últimes notícias: La tecla 'Control' ha detenido 'Escape' que ha quedado bajo custodia de 'Bloquear Desplazamiento'.",
                 u"Un hotel infinito lleno puede acojer infinitos clientes más. Peró un bot infinitamente perfecto (como yo) puede responder a tus peticiones *finitas*.",
                 u"Carpe diem et quid pro quo ut non habeas corpus mutatis mutandis.",
                 u"¿Mientes cuándo dices que mientes?",
                 u"Lo dicen las encuestas: cinco de cada diez bots... són la mitad.",
                 u"Yo nunca olvido un nick... pero en tu caso hare una excepcion.",
                 u"[<Espacio reservado para publicidad>]"]
owner_ping_es = [u"¡Totalmente de acuerdo!",u"Nuestro amo nos guía muy bien...",
               u"Sí, amo, lo que tu digas.",u"A la órden!",
               u"para servirlo",u"servidor",u"Miseñor, me llena de alegría sentir mi nombre en tu admirable discurso.",
               u":)",u"Mis respetos, majestad",
               u"Oh, majestad, es evidente que os apoyaré siempre en todas vuestras decisiones!",
               u"El jefe és un pezaooo, que alguien lo kickee del canal!!! >:D",
               u"Un favor personal... da los privilegios de owner a otro!"]     
               
normal_ping_en = [u"Do you think that I'll answer you? Bah!",u"Oh, my love! What do you want to say?",
                 u"Talking to me?",u"Be aware of what you say. You don't know who am I!",
                 u"Bah",u"Why do you say that? Don't offend me!",u"Hello, here the bot-central.",
                 u"pffff",u"hi!",u"Shut up, I'm unavailable!",u"Don't be silly!",
                 u"mmmmmhhh",u"are you sure?",u"one second",u"hi hi hi",
                 u"There are 10 types of bots: The ones that know binary and the ones that don't know it",
                 u"There are 3 types of bots: The ones that knows how to count and the ones that don't know how to do it.",
                 u"Looking for the full pi number. Wait a moment please...",
                 u"Breaking news: The 'Control' key has arrested 'Escape' and now it's being guarded by 'Block shift'.",
                 u"A full infinite hotel can host infinite more clients. But a bot infinitely perfect (like me) can't answer to your infinite commands.",
                 u"Carpe diem et quid pro quo ut non habeas corpus mutatis mutandis.",
                 u"Do you lie when you say you are lying?",
                 u"Polls say it: five of ten bots... are the half.",
                 u"I never forget a nick... but I will make an exception for you.",
                 u"[<Space reserved for ads>]"
                 ]            
owner_ping_en = [u"I agree with you!",u"Our lord guides us very well...",
               u"Yes, my lord, I'll follow you.",
               u"My lord, I'm very glad to listen my name in your great discourse.",
               u":)",u"I will follow you until the end, my Lord.",
               u"Oh, majesty, I will give my support on all your decisions!",
               u"My owner is crazy, kick him!!! >:D",
               u"One favour... give your owner rights to someone else!"]     
                                
@module.rule(r'(.*)?$nickname')
def mention(bot, trigger):
    if trigger.group(0).startswith('.'):
        return
    if trigger.owner or trigger.admin:
        dice = random.choice(['owner','nowner'])
        if dice == 'owner':
            if bot.config.lang == 'ca':
                bot.say(random.choice(owner_ping_ca) + u" [Més sobre mi: \x02%sajuda\x02]" % bot.config.prefix.replace("\\", ""))
            elif bot.config.lang == 'es':
                bot.say(random.choice(owner_ping_es) + u" [Más sobre mí: \x02%sayuda\x02]" % bot.config.prefix.replace("\\", ""))
            else:
                bot.say(random.choice(owner_ping_en) + u" [More about me: \x02%shelp\x02]" % bot.config.prefix.replace("\\", ""))
            return
        else:
            if bot.config.lang == 'ca':
                bot.say(random.choice(normal_ping_ca) + u" [Més sobre mi: \x02%sajuda\x02]" % bot.config.prefix.replace("\\", ""))
            elif bot.config.lang == 'es':
                bot.say(random.choice(normal_ping_es) + u" [Más sobre mí: \x02%sayuda\x02]" % bot.config.prefix.replace("\\", ""))
            else:
                bot.say(random.choice(normal_ping_en) + u" [More about me: \x02%shelp\x02]" % bot.config.prefix.replace("\\", ""))
            return          
    else:
        if bot.config.lang == 'ca':
            bot.say(random.choice(normal_ping_ca) + u" [Més sobre mi: \x02%sajuda\x02]" % bot.config.prefix.replace("\\", ""))
        elif bot.config.lang == 'es':
            bot.say(random.choice(normal_ping_es) + u" [Más sobre mí: \x02%sayuda\x02]" % bot.config.prefix.replace("\\", ""))
        else:
            bot.say(random.choice(normal_ping_en) + u" [More about me: \x02%shelp\x02]" % bot.config.prefix.replace("\\", ""))

@commands("ping")
def normal_ping(bot, trigger):
    bot.say("Pong!")
    
@commands("pong")
def normal_pong(bot, trigger):
    bot.say("Ping!")
