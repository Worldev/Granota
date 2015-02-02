# -*- coding: utf-8 -*-

from willie import module
from willie.module import commands
import random
import re

@module.rule(r".* quit")
def onjoin(bot, trigger):
    bot.say(u"Hola!")
