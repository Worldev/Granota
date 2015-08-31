# -*- coding: cp1252 -*-
from willie import module
from willie.module import commands
import random
import re

normal_ping_ca = ["Et penses que et repondré? Bah!","Digues, amor meu!",
                 "Dieu algo?","Vigila amb el que dius, que no saps qui sóc jo!",
                 "Bah","Per què dius això? No m'ofenguis!","Aquí la bot-central. Digui?",
                 "pfffff","hola!","Calla, que estic ocupat!","No siguis burro!",
                 "mmmmmhhh","Tu creus?","un segon","hi hi hi",
                 "Al món hi ha 10 tipus de bot: els que saben binari i els que no.",
                 "Al món hi ha 3 tipus de bot: els que saben comptar i els que no.",
                 "Calculant l'última xifra del nombre pi. Esperi si us plau...",
                 "Últimes notícies: La tecla 'Control' ha detingut la tecla 'Escape' que ha quedat sota custòdia de la tecla 'Bloquejar Desplaçament'.",
                 "Un hotel infinit ple pot acollir infinits clients més. Però un bot infinitament perfecte (Com jo) pot respondre a les teves peticions *finites*.",
                 "Carpe diem et quid pro quo ut non habeas corpus mutatis mutandis.",
                 "Menteixes quan dius que menteixes?",
                 "Ho diuen les enquestes: cinc de cada deu bots... són la meitat.",
                 "Jo mai oblido un nick... però en el teu cas faré una excepció.",
                 "[<Espai reservat per a publicitat>]"]
owner_ping_ca = ["Totalment d'acord!","L'amo sap guiar-nos molt bé...",
               "Sí, amo, el que tu diguis.","A la órden!",
               "per servir-lo","servidor","Senyor meu, m'omple de joia sentir el meu nom en el teu admirable discurs.",
               ":)","Els meus respectes, majestat",
               "Oh, majestat, és evident que us recolzaré sempre, en totes les vostres decisions!",
               "El jefe és un pesat, que algú el faci fora del xat!!! >:D",
               "Un favor personal... dona els privilegis d'owner a algú altre!"]
               
normal_ping_es = ["¿Crees que te respondré? ¡Bah!","¡Di, mi amor!",
                 "¿Decís algo?","Vigila con lo que dices, que no sabes quien soy yo!",
                 "Bah","¿Por qué dices eso? ¡No me ofendas!","Aquí la bot-central. ¿Diga?",
                 "pffff","hola!","Cállate, que estoy ocupado!","No seas tonto!",
                 "mmmmmhhh","¿Tu crees?","un segundo","ji ji ji",
                 "En el mundo hay 10 tipos de bot: los que saben binario y los que no.",
                 "En el mundo hay 3 tipos de bot: los que saben contar y los que no.",
                 "Calculando el último decimal del número pi. Espere por favor...",
                 "Últimes notícias: La tecla 'Control' ha detenido 'Escape' que ha quedado bajo custodia de 'Bloquear Desplazamiento'.",
                 "Un hotel infinito lleno puede acojer infinitos clientes más. Peró un bot infinitamente perfecto (como yo) puede responder a tus peticiones *finitas*.",
                 "Carpe diem et quid pro quo ut non habeas corpus mutatis mutandis.",
                 "¿Mientes cuándo dices que mientes?",
                 "Lo dicen las encuestas: cinco de cada diez bots... són la mitad.",
                 "Yo nunca olvido un nick... pero en tu caso hare una excepcion.",
                 "[<Espacio reservado para publicidad>]"]
owner_ping_es = ["¡Totalmente de acuerdo!","Nuestro amo nos guía muy bien...",
               "Sí, amo, lo que tu digas.","A la órden!",
               "para servirlo","servidor","Miseñor, me llena de alegría sentir mi nombre en tu admirable discurso.",
               ":)","Mis respetos, majestad",
               "Oh, majestad, és evidente que os apoyaré siempre en todas vuestras decisiones!",
               "El jefe és un pezaooo, que alguien lo kickee del canal!!! >:D",
               "Un favor personal... da los privilegios de owner a otro!"]     
               
normal_ping_en = ["Do you think that I'll answer you? Bah!","Oh, my love! What do you want to say?",
                 "Talking to me?","Be aware of what you say. You don't know who am I!",
                 "Bah","Why yo say that? Don't offend me!","Hello, here the bot-central.",
                 "pffff","hi!","Shut up, I'm unavailable!","Don't be silly!",
                 "mmmmmhhh","are you sure?","one second","hi hi hi",
                 "There are 10 types of bots: The ones that know binary and the ones that don't know it",
                 "There are 3 types of bots: The ones that knows how to count and the ones that don't know how to do it.",
                 "Looking for the full pi number. Wait a moment please...",
                 #u"Últimes notícias: La tecla 'Control' ha detenido 'Escape' que ha quedado bajo custodia de 'Bloquear Desplazamiento'.",
                 #u"Un hotel infinito lleno puede acojer infinitos clientes más. Peró un bot infinitamente perfecto (como yo) puede responder a tus peticiones *finitas*.",
                 "Carpe diem et quid pro quo ut non habeas corpus mutatis mutandis.",
                 "Do you lie when you say you are lying?",
                 #u"Lo dicen las encuestas: cinco de cada diez bots... són la mitad.",
                 "I never forget a nick... but I will make an exception for you.",
                 #u"[<Espacio reservado para publicidad>]"
                 ]            
owner_ping_en = ["I agree with you!","Our lord guides us very well...",
               "Yes, my lord, I'll follow you.",
               #u"para servirlo",u"servidor",
               "My lord, I'm very glad to listen my name in your great discourse.",
               ":)","I will follow you until the end, my Lord.",
               "Oh, majesty, I will give my support on all your decisions!",
               "My owner is crazy, kick him!!! >:D",
               "One favour... give your owner rights to someone else!"]     
                                
@module.rule(r'(.*)?$nickname')
def mention(bot, trigger):
    if trigger.owner or trigger.admin:
        dice = random.choice(['owner','nowner'])
        if dice == 'owner':
            if bot.config.lang == 'ca':
                bot.say(random.choice(owner_ping_ca))
            elif bot.config.lang == 'es':
                bot.say(random.choice(owner_ping_es))
            else:
                bot.say(random.choice(owner_ping_en))
            return
    else:
        if bot.config.lang == 'ca':
            bot.say(random.choice(normal_ping_ca))
        elif bot.config.lang == 'es':
            bot.say(random.choice(normal_ping_es))
        else:
            bot.say(random.choice(normal_ping_en))

@commands("ping")
def normal_ping(bot, trigger):
    bot.say("Pong!")
