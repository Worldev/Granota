# -*- coding: utf-8 -*-
from willie.module import commands, example
import time
import random
import re

@commands('pastis')
@example('.pastis NeoMahler')
def pastis(bot, trigger):
    u"""
    Dóna un pastís a l'usuari indicat
    """
    pastissos = ["...me'l menjo tot sencer, deixant les espelmes per %s, es clar!",
                "...el dono a %s, per bona persona!",
                "...el tiro a la cara de %s, per golafre!"]
    bot.say(u"Agafo un pastís i...")
    time.sleep(2)
    bot.say(random.choice(pastissos) % trigger.group(2))

@commands('galeta')
@example('.galeta NeoMahler')
def galeta(bot, trigger):
    u"""
    Dóna una galeta a l'usuari indicat
    """
    gust = random.choice(["amb gust de xocolata", "amb gust de maduixa", "amb gust de platan", "integral", "esmicolada"])
    mida = random.choice(["gran ", "gegant ", "immensa ", "petita ", "minuscula ", "gairebe invisible ", "de les mes grans que et pots trobar "])
    bot.say("Agafo una galeta " + mida + gust)
    bot.say("i la dono a " + trigger.group(2))
