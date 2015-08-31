# coding=utf-8
"""
*Availability: 3+ for all functions; attributes may vary.*

The config class is an abstraction class for accessing the active Willie
configuration file.

The Willie config file is divided to sections, and each section contains keys
and values. A section is an attribute of the config class, and is of type
``ConfigSection``. Each section contains the keys as attributes. For example,
if you want to access key example from section test, use
``config.test.example``. Note that the key names are made lower-case by the
parser, regardless of whether they are upper-case in the file.

The ``core`` section will always be present, and contains configuration used by
the Willie core. Modules are allowed to read those, but must not change them.

The config file can store strings, booleans and lists. If you need to store a
number, cast it to ``int()`` when reading.

For backwards compatibility, every key in the core section is an attribute of
the config class as well as of config.core. For new code, always specify the
name of the section, because this behavior might be removed in the future.

Running the ``config.py`` file directly will give the user an interactive
series of dialogs to create the configuration file. This will guide the user
through creating settings for the Willie core, the settings database, and any
modules which have a configuration function.

The configuration function, if used, must be declared with the signature
``configure(config)``. To add options, use ``interactive_add``, ``add_list``
and ``add_option``.
"""

import db
import os
import sys
import ConfigParser
import getpass
import imp

lang = None

class ConfigurationError(Exception):
    """ Exception type for configuration errors """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'ConfigurationError: %s' % self.value


class Config(object):
    def __init__(self, filename, load=True, ignore_errors=False):
        """
        Return a configuration object. The given filename will be associated
        with the configuration, and is the file which will be written if
        write() is called. If load is not given or True, the configuration
        object will load the attributes from the file at filename.

        A few default values will be set here if they are not defined in the
        config file, or a config file is not loaded. They are documented below.
        """
        self.filename = filename
        """The config object's associated file, as noted above."""
        self.parser = ConfigParser.RawConfigParser(allow_no_value=True)
        if load:
            self.parser.read(self.filename)

            if not ignore_errors:
                #Sanity check for the configuration file:
                if not self.parser.has_section('core'):
                    raise ConfigurationError('Core section missing!')
                if not self.parser.has_option('core', 'nick'):
                    raise ConfigurationError(
                        'Bot IRC nick not defined,'
                        ' expected option `nick` in [core] section'
                    )
                if not self.parser.has_option('core', 'owner'):
                    raise ConfigurationError(
                        'Bot owner not defined,'
                        ' expected option `owner` in [core] section'
                    )
                if not self.parser.has_option('core', 'host'):
                    raise ConfigurationError(
                        'IRC server address not defined,'
                        ' expceted option `host` in [core] section'
                    )

            #Setting defaults:
            if not self.parser.has_option('core', 'port'):
                self.parser.set('core', 'port', '6667')
            if not self.parser.has_option('core', 'user'):
                self.parser.set('core', 'user', 'willie')
            if not self.parser.has_option('core', 'name'):
                self.parser.set('core', 'name',
                                'Granota the frog - https://github.com/CatIRCBots/Granota')
            if not self.parser.has_option('core', 'prefix'):
                self.parser.set('core', 'prefix', r'\.')
            if not self.parser.has_option('core', 'admins'):
                self.parser.set('core', 'admins', '')
            if not self.parser.has_option('core', 'verify_ssl'):
                self.parser.set('core', 'verify_ssl', 'True')
            if not self.parser.has_option('core', 'timeout'):
                self.parser.set('core', 'timeout', '200')
        else:
            self.parser.add_section('core')

    def save(self):
        """Save all changes to the config file"""
        cfgfile = open(self.filename, 'w')
        self.parser.write(cfgfile)
        cfgfile.flush()
        cfgfile.close()

    def add_section(self, name):
        """
        Add a section to the config file, returns ``False`` if already exists.
        """
        try:
            return self.parser.add_section(name)
        except ConfigParser.DuplicateSectionError:
            return False

    def has_option(self, section, name):
        """ Check if option ``name`` exists under section ``section`` """
        return self.parser.has_option(section, name)

    def has_section(self, name):
        """ Check if section ``name`` exists """
        return self.parser.has_section(name)

    class ConfigSection(object):
        """
        Represents a section of the config file, contains all keys in the
        section as attributes.
        """
        def __init__(self, name, items, parent):
            object.__setattr__(self, '_name', name)
            object.__setattr__(self, '_parent', parent)
            for item in items:
                value = item[1].strip()
                if not value.lower() == 'none':
                    if value.lower() == 'false':
                        value = False
                    object.__setattr__(self, item[0], value)

        def __getattr__(self, name):
            return None

        def __setattr__(self, name, value):
            object.__setattr__(self, name, value)
            if type(value) is list:
                value = ','.join(value)
            self._parent.parser.set(self._name, name, value)

        def get_list(self, name):
            value = getattr(self, name)
            if not value:
                return []
            if isinstance(value, basestring):
                value = value.split(',')
                # Keep the split value, so we don't have to keep doing this
                setattr(self, name, value)
            return value

    def __getattr__(self, name):
        """"""
        if name in self.parser.sections():
            items = self.parser.items(name)
            section = self.ConfigSection(name, items, self)  # Return a section
            setattr(self, name, section)
            return section
        elif self.parser.has_option('core', name):
            return self.parser.get('core', name)  # For backwards compatibility
        else:
            raise AttributeError("%r object has no attribute %r"
                                 % (type(self).__name__, name))

    def interactive_add(self, section, option, prompt, default=None,
                        ispass=False):
        """
        Ask user in terminal for the value to assign to ``option`` under
        ``section``. If ``default`` is passed, it will be shown as the default
        value in the prompt. If ``option`` is already defined in ``section``,
        it will be used instead of ``default``, regardless of wheather
        ``default`` is passed.
        """
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        if self.parser.has_option(section, option):
            atr = self.parser.get(section, option)
            if ispass:
                value = getpass.getpass(prompt + ' [%s]: ' % atr) or atr
                self.parser.set(section, option, value)
            else:
                value = raw_input(prompt + ' [%s]: ' % atr) or atr
                self.parser.set(section, option, value)
        elif default:
            if ispass:
                value = getpass.getpass(
                    prompt + ' [%s]: ' % default
                ) or default
                self.parser.set(section, option, value)
            else:
                value = raw_input(prompt + ' [%s]: ' % default) or default
                self.parser.set(section, option, value)
        else:
            value = ''
            while not value:
                if ispass:
                    value = getpass.getpass(prompt + ': ')
                else:
                    value = raw_input(prompt + ': ')
            self.parser.set(section, option, value)

    def add_list(self, section, option, message, prompt):
        """
        Ask user in terminal for a list to assign to ``option``. If
        ``option`` is already defined under ``section``, show the user the
        current values and ask if the user would like to keep them. If so,
        additional values can be entered.
        """
        print message
        lst = []
        if self.parser.has_option(section, option) and self.parser.get(section,
                                                                       option):
            m = "You currently have " + self.parser.get(section, option)
            if self.option(m + '. Would you like to keep them', True):
                lst = self.parser.get(section, option).split(',')
        mem = raw_input(prompt + ' ')
        while mem:
            lst.append(mem)
            mem = raw_input(prompt + ' ')
        self.parser.set(section, option, ','.join(lst))

    def add_option(self, section, option, question, default=False):
        """
        Show user in terminal a "y/n" prompt, and set `option` to True or False
        based on the response. If default is passed as true, the default will
        be shown as ``[y]``, else it will be ``[n]``. ``question`` should be
        phrased as a question, but without a question mark at the end. If
        ``option`` is already defined, it will be used instead of ``default``,
        regardless of wheather ``default`` is passed.
        """
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        if self.parser.has_option(section, option):
            default = self.parser.getboolean(section, option)
        answer = self.option(question, default)
        self.parser.set(section, option, str(answer))

    def option(self, question, default=False):
        """
        Show user in terminal a "y/n" prompt, and return true or false based on
        the response. If default is passed as true, the default will be shown
        as ``[y]``, else it will be ``[n]``. ``question`` should be phrased as
        a question, but without a question mark at the end.
        """
        d = 'n'
        if default:
            if lang == 'en':
                d = 'y'
            elif lang == 'es' or lang == 'ca':
                d = 's'
        if lang == 'en':
            ans = raw_input(question + ' (y/n)? [' + d + '] ')
        elif lang == 'es' or lang == 'ca':
            ans = raw_input(question + ' (s/n)? [' + d + '] ')
        if not ans:
            ans = d
        return (ans is 'y' or ans is 'Y' or ans is 's' or ans is 'S')

    def _core(self):
        global lang
        if lang == 'en':
            print("You have set up the language for the setup wizard, but the bot language can be different. \
            Now, choose the language that the bot has to use in the IRC. This can be 'en' for English, \
            'es' for Spanish or 'ca' for Catalan.\n")
            self.interactive_add('core', 'lang', 'Language to use',
                            'en')
        elif lang == 'es':
            print(u"Has configurado un idioma para el asistente de configuración, pero el idioma del bot puede \
            ser diferente. Ahora, escoje el idioma que el bot debe usar en IRC. Puede ser 'en' para Inglés, \
            'es' para Español o 'ca' para Catalán.\n")
            self.interactive_add('core', 'lang', 'Idioma en el que el bot debe usar',
                            'es')
        elif lang == 'ca':
            print(u"Has configurat un idioma per l'assistent de configuració, però l'idioma del bot pot ser diferent. \
            Ara, escull l'idioma que el bot ha d'utilitzar a l'IRC. Pot ser 'en' per Anglès, 'es' per Castellà \
            o 'ca' per Català.\n")
            self.interactive_add('core', 'lang', 'Idioma en el que el bot ha d\'utilitzar',
                            'ca')
        else:
            print("There is a problem in your language settings. The language can be only 'en', 'es' or 'ca'. Fix \
            it and run the wizard again.")
            sys.exit()
        if lang == 'en':
            print("First of all, you need to set up a nickname for your bot. It can be 'Granota', but if your bot \
            will connect to a network with the official version of Granota, your bot will not be able to connect. \
            You should also check if the nickname is in use or registered with NickServ by typing \
            /msg NickServ info <the nick that you want>.\n")
            self.interactive_add('core', 'nick', 'Enter the nickname for your bot',
                                 'Granota')
            print("Of course, the bot is useless if it doesn't connect to some IRC server. If you don't know the host \
            of your server, contact the server administrators.\n")
            self.interactive_add('core', 'host', 'Enter the server to connect to',
                                 'irc.lizardirc.org')
            print("Some server support SSL connections. If your server supports it, it's recommended to \
            use it. If you are in doubt, contact the server administrators.\n")
            self.add_option('core', 'use_ssl', 'Should the bot connect with SSL?')
            if self.use_ssl == 'True':
                default_port = '6697'
            else:
                default_port = '6667'
            print("You also need to know the port of the server. The default port for an IRC server is 6667, \
            but if your bot connects with SSL the default port is 6697.\n")
            self.interactive_add('core', 'port', 'Enter the port to connect on',
                                 default_port)
            print("Granota has some commands that can also be performed by its owner (probably you). \
            Be careful, because the owner will have an absolut control of the bot.\n")
            self.interactive_add(
                'core', 'owner',
                "Enter your own IRC name (or that of the bot's owner)"
            )
            c = 'Now, let\'s set up the channels. You will be able to make the \
            bot to join a channel when it is connected, but you can also configure some channels to connect by \
            default.\nEnter the channels to connect to by default, one at a time.' + \
                ' When done, hit enter again.'
            self.add_list('core', 'channels', c, 'Channel:')
        elif lang == 'es':
            print(u"Antes de todo, necesitas configurar un nick para tu bot. Puede ser 'Granota', pero si quieres que \
            se connecte en una red donde haya el Granota oficial, no lo hara. Tiene que ser un nick que no esté en \
            uso o registrado con NickServ (compruébalo con /msg NickServ info <el nick que tu quieres>). Se recomienda \
            registrar el nick de tu bot para evitar que te lo quiten.\n")
            self.interactive_add('core', 'nick', 'Nick del bot',
                                 'Granota')
            print(u"Evidentemente, el bot es inútil si no se connecta en una red IRC. Escoje un servidor y busca \
            su 'hostname'. Si no sabes su hostname, contacta con los administradores de la red.\n")
            self.interactive_add('core', 'host', 'Server donde el bot debe conectarse',
                                 'irc.freenode.net')
            print(u"La conexión SSL es recomendada, pero algunos servidores no soportan conexiones SSL. Si no estás \
            seguro, contacta con los administradores del servidor.\n")
            self.add_option('core', 'use_ssl', 'El bot tiene que conectarse con SSL?')
            if self.use_ssl == 'True':
                default_port = '6697'
            else:
                default_port = '6667'
            print(u"Además del servidor tienes que escojer el puerto. El puerto por defecto es 6667 para conexiones \
            sin SSL. Si has escojido connectarte con SSL, el puerto por defecto es 6697.\n")
            self.interactive_add('core', 'port', 'Puerto del servidor donde el bot debe conectarse',
                                 default_port)
            print(u"Hay algunas funciones que solo las puede usar el propietario del bot. Ten en cuenta que el el nick \
            que configures aqui tendrá un poder absoluto sobre el bot.\n")
            self.interactive_add(
                'core', 'owner',
                "Tu nick de IRC (o el del propietario del bot)"
            )
            c = u'Mientras el bot está connectado puedes hacer que entre o salga de canales, pero se recomienda \
            configurar los canales dónde debe entrar siempre que se connecte a IRC. Escribe los canales en los que \
            el bot debe conectarse de forma automática. Despues cada canal presiona la tecla enter.' + \
                ' Cuando hayas puesto todos los canales, vuelve a presionar enter.'
            self.add_list('core', 'channels', c, 'Canal:')
        elif lang == 'ca':
            print(u"Primer, necessites configurar un nick pel teu bot. Pot ser 'Granota', però tingues en compte que \
            si vols que el bot es connecti en una xarxa IRC on ja hi ha un Granota oficial, el bot no es podrà \
            connectar. Et recomanem que abans comprovis si el nick ja s'està utilitzant o està registrat amb el \
            NickServ (comprova-ho amb /msg NickServ info <nick>). També et recomanem que registris el nick \
            per evitar que algú altre te'l prengui.\n")
            self.interactive_add('core', 'nick', 'Nick del bot',
                                 'Granota')
            print(u"Ara has d'escollir el servidor on el bot s'ha de connectar. Quan l'hagis escollit escriu el \
            servidor, has de trobar el seu 'hostname'. Si no saps quin és, contacta amb els administradors del \
            servidor.\n")
            self.interactive_add('core', 'host', 'Servidor on el bot ha de connectar-se',
                                 'irc.freenode.net')
            print(u"Es recomana utilitzar connexió SSL, però hi ha servidors que no poden rebre connexions \
            d'aquest tipus. Si no n'estàs segur, pots preguntar als administradors de la xarxa.\n")
            self.add_option('core', 'use_ssl', 'El bot ha de connectar-se amb SSL')
            if self.use_ssl == 'True':
                default_port = '6697'
            else:
                default_port = '6667'
            print(u"A més del servidor, el bot necessita saber el port on s'ha de connectar. Normalment és el \
            6667, però si utilitza SSL segurament serà 6697.\n")
            self.interactive_add('core', 'port', 'Port del servidor on el bot ha de connectar-se',
                                 default_port)
            print(u"Hi ha algunes funciones reservades nomes al propietari del bot. Ves en compte en escollir-lo \
            si no ets tu, perque el propietari tindra un control absolut sobre el bot mentre estigui connectat.\n")
            self.interactive_add(
                'core', 'owner',
                "El teu nick d'IRC (o el del propietari del bot)"
            )
            c = u'Mentre el bot està connectat pots fer que entri o surti de canals. Però es recomana que especifiquis \
            ara els canals en els que el bot ha de connectar-se de manera automatica a cada connexió. Despres de \
            cada canal presiona la tecla enter. Al acabar la llista de canals, pressiona enter una altra vegada.'
            self.add_list('core', 'channels', c, 'Canal:')            

    def _db(self):
        db.configure(self)
        self.save()

    def _modules(self):
        home = os.getcwd()
        modules_dir = os.path.join(home, 'modules')
        filenames = self.enumerate_modules()
        os.sys.path.insert(0, modules_dir)
        for name, filename in filenames.iteritems():
            try:
                module = imp.load_source(name, filename)
            except Exception, e:
                print >> sys.stderr, ("Error loading %s: %s (in config.py)"
                                      % (name, e))
            else:
                if hasattr(module, 'configure'):
                    module.configure(self)
        self.save()

    def enumerate_modules(self, show_all=False):
        """
        *Availability: 4.0+*

        Return a dict mapping the names of modules to the location of their
        file.  This searches the regular modules directory and all directories
        specified in the `core.extra` attribute of the `config` object. If two
        modules have the same name, the last one to be found will be returned
        and the rest will be ignored. Modules are found starting in the regular
        directory, followed by `~/.willie/modules`, and then through the extra
        directories in the order that the are specified.

        If `show_all` is given as `True`, the `enable` and `exclude`
        configuration options will be ignored, and all modules will be shown
        (though duplicates will still be ignored as above).
        """
        modules = {}

        # First, add modules from the regular modules directory
        this_dir = os.path.dirname(os.path.abspath(__file__))
        modules_dir = os.path.join(this_dir, 'modules')
        for fn in os.listdir(modules_dir):
            if fn.endswith('.py') and not fn.startswith('_'):
                modules[fn[:-3]] = os.path.join(modules_dir, fn)
        # Next, look in ~/.willie/modules
        if self.core.homedir is not None:
            home_modules_dir = os.path.join(self.core.homedir, 'modules')
        else:
            home_modules_dir = os.path.join(os.path.expanduser('~'), '.willie',
                                        'modules')
        if not os.path.isdir(home_modules_dir):
            os.makedirs(home_modules_dir)
        for fn in os.listdir(home_modules_dir):
            if fn.endswith('.py') and not fn.startswith('_'):
                modules[fn[:-3]] = os.path.join(home_modules_dir, fn)

        # Last, look at all the extra directories. (get_list returns [] if
        # there are none or the option isn't defined, so it'll just skip this
        # bit)
        for directory in self.core.get_list('extra'):
            for fn in os.listdir(directory):
                if fn.endswith('.py') and not fn.startswith('_'):
                    modules[fn[:-3]] = os.path.join(directory, fn)

        # If caller wants all of them, don't apply white and blacklists
        if show_all:
            return modules

        # Apply whitelist, if present
        enable = self.core.get_list('enable')
        if enable:
            enabled_modules = {}
            for module in enable:
                if module in modules:
                    enabled_modules[module] = modules[module]
            modules = enabled_modules

        # Apply blacklist, if present
        exclude = self.core.get_list('exclude')
        for module in exclude:
            if module in modules:
                del modules[module]

        return modules


def wizard(section, config=None):
    dotdir = os.path.expanduser('~/.willie')
    configpath = os.path.join(dotdir, (config or 'default') + '.cfg')
    if section == 'all':
        create_config(configpath)
    elif section == 'db':
        check_dir(False)
        if not os.path.isfile(configpath):
            print "No config file found." + \
                " Please make one before configuring these options."
            sys.exit(1)
        config = Config(configpath, True)
        config._db()
    elif section == 'mod':
        check_dir(False)
        if not os.path.isfile(configpath):
            print "No config file found." + \
                " Please make one before configuring these options."
            sys.exit(1)
        config = Config(configpath, True)
        config._modules()


def check_dir(create=True):
    dotdir = os.path.join(os.path.expanduser('~'), '.willie')
    if not os.path.isdir(dotdir):
        if create:
            print 'Creating a config directory at ~/.willie...'
            try:
                os.makedirs(dotdir)
            except Exception, e:
                print >> sys.stderr, \
                    ('There was a problem creating %s: -- Problema creando %s -- Problema creant %s' % (dotdir, dotdir, dotdir))
                print >> sys.stderr, e.__class__, str(e)
                print >> sys.stderr, \
                    'Please fix this and then run Granota again. -- Por favor, arregle eso y vuelva a executar a Granota -- Si us plau, arregla el problema i torna a executar el bot.'
                sys.exit(1)
        else:
            print "No config file found. Please make one before configuring these options."
            sys.exit(1)


def create_config(configpath):
    check_dir()
    global lang
    lang = raw_input('Language -- Idioma (en, es, ca) [en]: ')
    if lang == "":
        lang = "en"
    if lang == 'en':
        print "Please answer the following questions:\n"
    elif lang == 'es':
        print "Responde esas preguntas:\n"
    elif lang == 'ca':
        print "Respon aquestes preguntes:\n"
    else:
        print "The language specified is not valid. It must be 'en' for english, 'es' for spanish and 'ca' for catalan."
        print "El idioma especificado no es valido. Tiene que ser 'en' para ingles, 'es' para espanol y 'ca' para catalan."
        print "L'idioma especificat no es valid. Ha de ser 'en' per angles, 'es' per espanyol i 'ca' per catala."
        create_config(configpath)
        return
    try:
        config = Config(configpath, os.path.isfile(configpath))
        config._core()
        if config.option("Would you like to set up a settings database now?"):
            config._db()
        if config.option(
            'Would you like to see if there are any modules'
            ' that need configuring'
        ):
            config._modules()
        config.save()
    except Exception, e:
        if lang == 'en':
            print "Encountered an error while writing the config file." + \
                " This shouldn't happen. Check permissions."
        elif lang == 'es':
            print "Error encontrado al escribir el archivo de configuracion. Comprueba que el servidor o ordenador tenga permiso de escritura."
        else:
            print "Error a l'escriure l'arxiu de configuracio. Comprova que el servidor o ordinador tingui permis d'escriptura."
        raise
        sys.exit(1)
    if lang == 'en':
        print "Config file written sucessfully!"
    elif lang == 'es':
        print "Fichero de configuracion escrito con exito!"
    elif lang == 'ca':
        print "Fitxer de configuracio escrit amb exit!"
