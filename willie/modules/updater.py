#!/usr/bin/python
# coding=utf-8

import willie
import willie.module
from willie.module import commands, rule, event, version
from willie import module
import willie.modules.debug as debug
import urllib, json
import tarfile
import os, shutil
from distutils.dir_util import copy_tree

@willie.module.commands('update-stable')
@willie.module.priority('high')
def update_stable(bot, trigger):
    if not trigger.owner:
        return
    current = version()
    web = urllib.urlopen("https://api.github.com/repos/Worldev/Granota/releases/latest")
    data = json.load(web)
    latest = data['tag_name']
    if latest == current:
        if bot.config.lang == 'ca':
            bot.say(u"Ja estic actualitzat.")
        elif bot.config.lang == 'es':
            bot.say("Ya estoy actualizado.")
        else:
            bot.say("I'm already updated.")
        return
    url = data['tarball_url'] # Download url (.tar.gz)
    bot.say("Downloading latest version and updating... that will take less than a minute")
    os.mkdir('tmp') # Create temporary directory
    with cd("tmp"):
        urllib.urlretrieve(data['tarball_url'], "Granota-last-version.tar.gz") # Download las version and name the tarball
        tar = tarfile.open("Granota-last-version.tar.gz")
        tar.extractall() # Extract tarball
        tar.close()
        os.remove("Granota-last-version.tar.gz") # Delete the old tarball
        files = os.listdir('.')
        for f in files:
            if f.startswith('Worldev-Granota-'): # We don't know the name of the extracted tarball
                new = f

    # Start copying files in the "doc" folder
    with cd("tmp/%s/doc" % new):
        docfiles = os.listdir('.') # List of files inside the "doc" folder
    for f in docfiles:  # Copy them all
        if os.path.isfile("tmp/%s/doc/%s" % (new, f)):
            shutil.copy("tmp/%s/doc/%s" % (new, f), 'doc/%s' % f)
        else:
            copy_tree('tmp/%s/doc/%s' % (new, f), 'doc/%s' % f)

    # Start copying the files in the "willie" folder
    with cd("tmp/%s/willie" % new):
        williefiles = os.listdir('.')
    for f in williefiles:
        if f.startswith('modules'): # We will copy modules later
            pass
        else:
            if os.path.isfile("tmp/%s/willie/%s" % (new, f)):
                shutil.copy("tmp/%s/willie/%s" % (new, f), 'willie/%s' % f)
            else:
                copy_tree('tmp/%s/willie/%s' % (new, f), 'willie/%s' % f)
                
    # Start copying the files in the "willie/modules" folder
    with cd("tmp/%s/willie/modules" % new):
        modules = os.listdir('.')
    for f in modules:
        if os.path.isfile("tmp/%s/willie/modules/%s" % (new, f)):
            shutil.copy("tmp/%s/willie/modules/%s" % (new, f), 'willie/modules/%s' % f)
        else:
            copy_tree('tmp/%s/willie/modules/%s' % (new, f), 'willie/modules/%s' % f)

    shutil.rmtree('tmp/')
    bot.say("Done! Please reload me using the %sreload command" % bot.config.prefix.replace('\\', ''))

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
