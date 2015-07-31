# coding=utf-8
"""
You may ignore this. Is just an test.
"""
import sys
import re

import willie.config
import willie.bot
import willie.irc
import willie.tools
import pytest
from multiprocessing import cpu_count

args = [filename, "-s"]
args.extend(['--tb', 'native'])
if multithread and cpu_count() > 1:
    args.extend(["-n", str(cpu_count())])

pytest.main(args)
