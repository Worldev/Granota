# coding=utf-8
"""
You may ignore this. Is just an test.
"""

import sys

print "Granota test script"
print "Testing core"

try:
    import willie.config
    import willie.bot
    import willie.irc
    import willie.tools
except:
    print "Core is failling!"
    sys.exit(1)
    
print "Looks like core is working"

print "Running pytest and testing granota.py"

import pytest
test = pytest.main(["granota.py", "-s", '--tb', 'native'])

if test is 1:
    print "granota.py is failling!"
    sys.exit(1)
else:
    print "Looks like granota.py is working"

print "All done."
sys.exit(0)
