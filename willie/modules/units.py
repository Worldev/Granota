# -*- coding: utf-8 -*-

from willie.module import commands, example, NOLIMIT
import re

find_temp = re.compile('(-?[0-9]*\.?[0-9]*)[ °]*(K|C|F)', re.IGNORECASE)
find_length = re.compile('([0-9]*\.?[0-9]*)[ ]*(mile[s]?|mi|inch|in|foot|feet|ft|yard[s]?|yd|(?:centi|kilo|)meter[s]?|[kc]?m)', re.IGNORECASE)


def f_to_c(temp):
    return (float(temp) - 32) * 5 / 9


def c_to_k(temp):
    return temp + 273.15


def c_to_f(temp):
    return (9.0 / 5.0 * temp + 32)


def k_to_c(temp):
    return temp - 273.15


@commands('temp', 'temperatura', 'temperature')
def temperature(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            bot.reply(u"Error de sintaxi. Escriu .temp <número><unitat de mesura>")
        elif bot.config.lang == 'es':
            bot.repy(u"Error de sintaxis. Escribe .temp <número><unidad de mesura>")
        else:
            bot.reply(u"Syntax error. User .temp <number><measure unit>")
        return
    try:
        source = find_temp.match(trigger.group(2)).groups()
    except AttributeError:
        if bot.config.lang == 'ca':
            bot.reply(u"Aquesta temperatura no és vàlida")
        elif bot.config.lang == 'es':
            bot.reply(u"Esa temperatura no es valida")
        else:
            bot.reply("That's not a valid temperature.")
        return NOLIMIT
    unit = source[1].upper()
    numeric = float(source[0])
    celsius = 0
    if unit == 'C':
        celsius = numeric
    elif unit == 'F':
        celsius = f_to_c(numeric)
    elif unit == 'K':
        celsius = k_to_c(numeric)

    kelvin = c_to_k(celsius)
    fahrenheit = c_to_f(celsius)
    bot.reply("%s°C = %s°F = %sK" % (celsius, fahrenheit, kelvin))


@commands('length', 'distance', 'distancia')
def distance(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            bot.reply(u"Error de sintaxi. Escriu .distancia <número><unitat de mesura>")
        elif bot.config.lang == 'es':
            bot.repy(u"Error de sintaxis. Escribe .distancia <número><unidad de mesura>")
        else:
            bot.reply(u"Syntax error. User .length <number><measure unit>")
        return
    try:
        source = find_length.match(trigger.group(2)).groups()
    except AttributeError:
        if bot.config.lang == 'ca':
            bot.reply(u"Aquesta no és unitat de distànica vàlida.")
        elif bot.config.lang == 'es':
            bot.reply(u"Esa no es una unidad de distancia valida.")
        else:
            bot.reply("That's not a valid length unit.")
        return NOLIMIT
    unit = source[1].lower()
    numeric = float(source[0])
    meter = 0
    if unit in ("meters", "meter", "m", "metre", "metro", "metres", "metros"):
        meter = numeric
    elif unit in ("kilometers", "kilometer", "km", "kilometres", "kilometre", "quilometres", "quilometre", "kilometros", "kilometro"):
        meter = numeric * 1000
    elif unit in ("miles", "mile", "mi", "milla", "milles", "millas"):
        meter = numeric / 0.00062137
    elif unit in ("inch", "in"):
        meter = numeric / 39.370
    elif unit in ("centimeters", "centimeter", "cm", "centimetre", "centimetres", "centimetro", "centimetros"):
        meter = numeric / 100
    elif unit in ("feet", "foot", "ft", "peu", "peus", "pie", "pies"):
        meter = numeric / 3.2808
    elif unit in ("yards", "yard", "yd", "iarda", "iardes", "yarda", "yardas"):
        meter = numeric / (3.2808 * 3)

    if meter >= 1000:
        metric_part = '%skm' % (meter / 1000)
    elif meter < 1:
        metric_part = '%scm' % (meter * 100)
    else:
        metric_part = '%sm' % meter

    # Shit like this makes me hate being an American.
    inch = meter * 39.37
    foot = int(inch) / 12
    inch = inch - (foot * 12)
    yard = foot / 3
    mile = meter * 0.00062137

    if yard > 500:
        if mile == 1:
            stupid_part = '1 mile'
        else:
            stupid_part = '%s miles' % mile
    else:
        parts = []
        if yard >= 100:
            parts.append('%s yards' % yard)
            foot -= (yard * 3)

        if foot == 1:
            parts.append('1 foot')
        elif foot != 0:
            parts.append('%s feet' % foot)

        if inch == 1:
            parts.append('1 inch')
        elif inch != 0:
            parts.append('%s inches' % inch)

        stupid_part = ', '.join(parts)

    bot.reply('%s = %s' % (metric_part, stupid_part))


if __name__ == "__main__":
    from willie.test_tools import run_example_tests
    run_example_tests(__file__)
