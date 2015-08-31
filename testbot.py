# coding=utf-8
"""
Granota testing script

Tests Granota's script searching possible bugs. 

NOTE: This is supposed to be used on Travis CI.
"""

import sys
import os
import pytest
import socket
import time
import urllib2

working = []
notworking = []
criticalnotworking = []

def nreport(msg):
    urllib2.urlopen("http://n.tkte.ch/h/4314/eOoVGWdAFqh-sJRGGTJb3XCW?payload={0}".format(urllib.parse.quote("[Granota testing] {0}".format(msg))))

print "Granota testing script\n"

print "Granota testing script has started.\n"

print "Testing: Core\n"

print "Testing: willie.__init__"
try:
	import willie.__init__
	print "WORKING: willie.__init__\n"
	working.append("willie.__init__")
except:
	print "FAILING: willie.__init__\n"
	notworking.append("willie.__init__")
	criticalnotworking.append("willie.__init__")

print "Testing: willie.bot"
try:
	import willie.bot
	print "WORKING: willie.bot\n"
	working.append("willie.bot")
except:
	print "FAILING: willie.bot\n"
	notworking.append("willie.bot")
	criticalnotworking.append("willie.bot")

print "Testing: willie.config"
try:
	import willie.config
	print "WORKING: willie.config\n"
	working.append("willie.config")
except:
	print "FAILING: willie.config\n"
	notworking.append("willie.config")
	criticalnotworking.append("willie.config")
	
print "Testing: willie.coretasks"
try:
	import willie.coretasks
	print "WORKING: willie.coretasks\n"
	working.append("willie.coretasks")
except:
	print "FAILING: willie.coretasks\n"
	notworking.append("willie.coretasks")
	criticalnotworking.append("willie.coretasks")

print "Testing: willie.db"
try:
	import willie.db
	print "WORKING: willie.db\n"
	working.append("willie.db")
except:
	print "FAILING: willie.db\n"
	notworking.append("willie.db")
	criticalnotworking.append("willie.db")
	
print "Testing: willie.icao"
try:
	import willie.icao
	print "WORKING: willie.icao\n"
	working.append("willie.icao")
except:
	print "FAILING: willie.icao\n"
	notworking.append("willie.icao")
	criticalnotworking.append("willie.icao")

print "Testing: willie.irc"
try:
	import willie.irc
	print "WORKING: willie.irc\n"
	working.append("willie.irc")
except:
	print "FAILING: willie.irc\n"
	notworking.append("willie.bot")
	criticalnotworking.append("willie.bot")
	
print "Testing: willie.module"
try:
	import willie.module
	print "WORKING: willie.module\n"
	working.append("willie.module")
except:
	print "FAILING: willie.module\n"
	notworking.append("willie.module")
	criticalnotworking.append("willie.module")
	
print "Testing: willie.test_tools"
try:
	import willie.test_tools
	print "WORKING: willie.test_tools\n"
	working.append("willie.test_tools")
except:
	print "FAILING: willie.test_tools\n"
	notworking.append("willie.test_tools")
	criticalnotworking.append("willie.test_tools")

print "Testing: willie.tools"
try:
	import willie.tools
	print "WORKING: willie.tools\n"
	working.append("willie.tools")
except:
	print "FAILING: willie.tools\n"
	notworking.append("willie.tools")
	criticalnotworking.append("willie.tools")
	
print "Testing: willie.web"
try:
	import willie.web
	print "WORKING: willie.web\n"
	working.append("willie.web")
except:
	print "FAILING: willie.web\n"
	notworking.append("willie.web")
	criticalnotworking.append("willie.web")

print "\nTesting: granota.py"
testgra = pytest.main(["granota.py", "-s", '--tb', 'native'])

if testgra is 0:
	print "WORKING: granota.py\n"
	working.append("granota.py")
else:
	print "FAILING: granota.py\n"
	notworking.append("granota.py")
	criticalnotworking.append("granota.py")

print "Testing: Modules\n" 

for val in os.listdir("willie/modules"):
	if val.find("__init__") == -1 and val.find(".pyc") == -1 and val.find("__pycache__") == -1:
		print "Testing: Module {0}".format(val)
		testmod = pytest.main(["willie/modules/{0}".format(val), "-s", '--tb', 'native'])
		if testmod is 0:
			print "WORKING: Module {0}".format(val)
			working.append("module {0}".format(val))
		else:
			print "FAILING: Module {0}".format(val)
			notworking.append("module {0}".format(val))

print "\nThe tests have been done successfully.\n"

print "============================= test results =============================="
workingnum = len(working)
notworkingnum = len(notworking)
criticalnotworkingnum = len(criticalnotworking)
alltestsmade = workingnum + notworkingnum + criticalnotworkingnum
workingvals = ""
notworkingvals = ""
criticalnotworkingvals = ""
for val in working:
	workingvals = workingvals + val + ", "
for val in notworking:
	notworkingvals = notworkingvals + val + ", "
for val in criticalnotworking:
	criticalnotworkingvals = criticalnotworkingvals + val + ", "
print "Tests made: {0}".format(alltestsmade)
nreport("Tests made: {0}".format(alltestsmade))
print "WORKING: {0}{1} in total".format(workingvals, workingnum)
print "FAILING: {0}{1} in total".format(notworkingvals, notworkingnum)
print "CRITICALLY FAILING {0}{1} in total".format(criticalnotworkingvals, criticalnotworkingnum)
if criticalnotworkingnum is 0 and notworkingnum is not 0:
	print "The build has passed, but there are failing stuff that should get fixed."
	nreport("The build has \x0309passed\x0F, but there are \x0304failing\x0F stuff that should get fixed.")
elif criticalnotworkingnum is 0 and notworkingnum is 0:
	print "The build has passed successfully."
	nreport("The build has \x0309passed\x0F successfully.")
else:
	print "The build has failed."
	nreport("The build has \x02\x0304failed\x0F.")
nreport("For more information please visit https://travis-ci.org/CatIRCBots/Granota")
print "============================= test results =============================="
if criticalnotworkingnum is 0:
	sys.exit(0)
else:
	sys.exit(1)
