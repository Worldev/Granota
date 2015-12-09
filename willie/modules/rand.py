
from willie.module import commands, example
import random
import sys


@commands('rand', 'alea')
def rand(bot, trigger):
    arg1 = trigger.group(3)
    arg2 = trigger.group(4)

    if arg2 is not None:
        low = int(arg1)
        high = int(arg2)
    elif arg1 is not None:
        low = 0
        high = int(arg1)
    else:
        low = 0
        high = sys.maxint

    if low > high:
        low, high = high, low

    number = random.randint(low, high)
    if bot.config.lang == 'ca':
        bot.reply("aleatori(%d, %d) = %d" % (low, high, number))
    elif bot.config.lang == 'es':
        bot.reply("aleatorio(%d, %d) = %d" % (low, high, number))
    else:
        bot.reply("random(%d, %d) = %d" % (low, high, number))


if __name__ == "__main__":
    from willie.test_tools import run_example_tests
    run_example_tests(__file__)
