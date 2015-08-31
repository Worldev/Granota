#!/usr/bin/env python2
# coding=utf-8

import sys
import os
import optparse
import signal

from willie.__init__ import run
from willie.config import Config, create_config, ConfigurationError, wizard
import willie.tools as tools
from willie.tools import stderr


homedir = os.path.join(os.path.expanduser('~'), '.willie')


def check_python_version():
    if sys.version_info < (3, 3):
        stderr('Error: You need at least Python 3.3!')
        sys.exit(1)


def enumerate_configs(extension='.cfg'):
    configfiles = []
    if os.path.isdir(homedir):
        willie_dotdirfiles = os.listdir(homedir)  # Preferred
        for item in willie_dotdirfiles:
            if item.endswith(extension):
                configfiles.append(item)

    return configfiles


def find_config(name, extension='.cfg'):
    if os.path.isfile(name):
        return name
    configs = enumerate_configs(extension)
    if name in configs or name + extension in configs:
        if name + extension in configs:
            name = name + extension

    return os.path.join(homedir, name)


def main(argv=None):
    global homedir
    # Step One: Parse The Command Line
    try:
        parser = optparse.OptionParser('%prog [options]')
        parser.add_option('-c', '--config', metavar='filename',
            help='use a specific configuration file')
        parser.add_option("-d", '--fork', action="store_true",
            dest="deamonize", help="Deamonize willie")
        parser.add_option("-q", '--quit', action="store_true", dest="quit",
            help="Gracefully quit Willie")
        parser.add_option("-k", '--kill', action="store_true", dest="kill",
            help="Kill Willie")
        parser.add_option('--exit-on-error', action="store_true", dest="exit_on_error",
            help="Exit immediately on every error instead of trying to recover")
        parser.add_option("-l", '--list', action="store_true",
            dest="list_configs", help="List all config files found")
        parser.add_option("-m", '--migrate', action="store_true",
            dest="migrate_configs",
            help="Migrate config files to the new format")
        parser.add_option('--quiet', action="store_true", dest="quiet",
            help="Supress all output")
        parser.add_option('-w', '--configure-all', action='store_true',
            dest='wizard', help='Run the configuration wizard.')
        parser.add_option('--configure-modules', action='store_true',
            dest='mod_wizard', help='Run the configuration wizard, but only for the module configuration options.')
        parser.add_option('--configure-database', action='store_true',
            dest='db_wizard', help='Run the configuration wizard, but only for the database configuration options.')
        opts, args = parser.parse_args(argv)

        if opts.wizard:
            wizard('all', opts.config)
            return
        elif opts.mod_wizard:
            wizard('mod', opts.config)
            return
        elif opts.db_wizard:
            wizard('db', opts.config)
            return

        check_python_version()
        if opts.list_configs is not None:
            configs = enumerate_configs()
            print('Arxius de configuació a ~/.willie:')
            if len(configs[0]) is 0:
                print('\tNo he trobat res')
            else:
                for config in configs:
                    print('\t%s' % config)
            print('-------------------------')
            return

        config_name = opts.config or 'default'

        configpath = find_config(config_name)
        if not os.path.isfile(configpath):
            print("Welcome to Granota configuration wizard! -- Bienvenido al asistente de configuracion de Granota! -- Benvingut a l'assistent de cnfiguracio de Granota!\n")
            if not configpath.endswith('.cfg'):
                configpath = configpath + '.cfg'
            create_config(configpath)
            configpath = find_config(config_name)
        try:
            config_module = Config(configpath)
        except ConfigurationError as e:
            stderr(e)
            sys.exit(2)

        if config_module.core.not_configured:
            stderr('The bot is not configured. -- El bot no esta configurado. -- El bot no esta configurat.')
            # exit with code 2 to prevent auto restart on fail by systemd
            sys.exit(2)

        if not config_module.has_option('core', 'homedir'):
            config_module.dotdir = homedir
            config_module.homedir = homedir
        else:
            homedir = config_module.core.homedir
            config_module.dotdir = config_module.core.homedir

        if not config_module.core.logdir:
            config_module.core.logdir = os.path.join(homedir, 'logs')
        logfile = os.path.os.path.join(config_module.logdir, 'stdio.log')
        if not os.path.isdir(config_module.logdir):
            os.mkdir(config_module.logdir)

        if opts.exit_on_error:
            config_module.exit_on_error = True
        else:
            config_module.exit_on_error = False

        if opts.quiet is None:
            opts.quiet = False

        sys.stderr = tools.OutputRedirect(logfile, True, opts.quiet)
        sys.stdout = tools.OutputRedirect(logfile, False, opts.quiet)

        #Handle --quit, --kill and saving the PID to file
        pid_dir = config_module.core.pid_dir or homedir
        if opts.config is None:
            pid_file_path = os.path.join(pid_dir, 'willie.pid')
        else:
            basename = os.path.basename(opts.config)
            if basename.endswith('.cfg'):
                basename = basename[:-4]
            pid_file_path = os.path.join(pid_dir, 'willie-%s.pid' % basename)
        if os.path.isfile(pid_file_path):
            pid_file = open(pid_file_path, 'r')
            old_pid = int(pid_file.read())
            pid_file.close()
            if tools.check_pid(old_pid):
                if opts.quit is None and opts.kill is None:
                    stderr('There is already a Granota running. -- Ya hay un bot executandose. -- Ja hi ha un bot executant-se.')
                    stderr('Try -- Intenta: --quit o --kill')
                    sys.exit(1)
                elif opts.kill:
                    stderr('Killing Granota. -- Matando a Granota. -- Matant Granota.')
                    os.kill(old_pid, signal.SIGKILL)
                    sys.exit(0)
                elif opts.quit:
                    stderr('Quitting Granota. -- Desconnectando a Granota. -- Desconnectant a Granota.')
                    if hasattr(signal, 'SIGUSR1'):
                        os.kill(old_pid, signal.SIGUSR1)
                    else:
                        os.kill(old_pid, signal.SIGTERM)
                    sys.exit(0)
            elif not tools.check_pid(old_pid) and (opts.kill or opts.quit):
                stderr('The bot is not running. -- El bot no se esta executando. -- El bot no s\'esta executant.')
                sys.exit(1)
        elif opts.quit is not None or opts.kill is not None:
            stderr('The bot is not running. -- El bot no se esta executando. -- El bot no s\'esta executant.')
            sys.exit(1)
        if opts.deamonize is not None:
            child_pid = os.fork()
            if child_pid is not 0:
                sys.exit()
        pid_file = open(pid_file_path, 'w')
        pid_file.write(str(os.getpid()))
        pid_file.close()
        config_module.pid_file_path = pid_file_path

        # Step Five: Initialise And Run willie
        run(config_module)
    except KeyboardInterrupt:
        print("\n\nKeyboard Interrupt")
        os._exit(1)
if __name__ == '__main__':
    main()
