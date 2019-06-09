# -*- coding:utf-8 -*-
from datetime import datetime as dt

from django.core.management.base import BaseCommand

from main.core.logger import Log
from ...const import DEFAULT_BACKUP_FOLDER, BACKUP_CONTENT
from ...core.backup_manager import BackupManager


class Command(BaseCommand):
    help = """Dump current Rallyman configuration (from files and database) to an archive (.zip)

    Command:
        configuration [--mode <backup/restore>] [--path <archive path-or-folder>]
                      [--label <archive label>]
                      [--content <archivent content>]
                      [--debug]

    Optionnal parameters:
        -m, --mode            Backup or restore given file
        
        -p, --path            archive path or folder where to backup the configuration

            * if `path` is a filepath: dump archive at given filepath
            * if `path` a folder: dump archive in given folder, with a generated file name

        -l, --label           label of the archive. If not set, replaced by a datetime information

        -ct, --content        content to backup (all/config/templates)

    Switches:
        -d, --debug           show .debug logs and method profiles

    Examples:
        # Create archive to the default folder, with a generated name
        python manage.py configuration --mode backup
        
        # Create archive to a folder, with a generated name
        python manage.py configuration --mode backup --path _BKP
        
        # Create archive to a file path.
        python manage.py configuration --mode backup --path _BKP/backup.zip
        
        # Create archive to the default folder, with a generated name suffixed by a label
        python manage.py configuration --mode backup --label some_label
        
        # Create archive to a folder, with a generated name suffixed by a label
        python manage.py configuration --mode backup --path _BKP --label some_label
    """
    optWithChoices = ['all', 'config', 'templates']

    def add_arguments(self, parser):
        # optionnal parameters

        parser.add_argument('-m', '--mode',
                            choices=['backup', 'restore'],
                            default='backup',
                            help='Backup or restore.')
        parser.add_argument('-p', '--path',
                            default=DEFAULT_BACKUP_FOLDER,
                            help='Path of the archive to be created.')
        parser.add_argument('-l', '--label',
                            help='Label of the archive.')

        parser.add_argument('-ct', '--content',
                            help='Content to dump in archive.',
                            choices=BACKUP_CONTENT.getChoices(),
                            default=BACKUP_CONTENT.getDefaultChoice())

        # switch parameters
        parser.add_argument('-C', '--confirm',
                            help='Confirmation is required to force archive creation.',
                            default=False,
                            action='store_true')
        parser.add_argument('-f', '--force',
                            help='Allows to bypass errors. Use with caution.',
                            default=False,
                            action='store_true')
        parser.add_argument('-d', '--debug',
                            help='Debug.',
                            default=False,
                            action='store_true')

    def handle(self, *args, **options):
        print ''
        _tStart = dt.now()

        # Option debug
        debug = options.get('debug')
        log = Log(self)
        log.debug('Begins...')

        # Option label
        _optLabel = options.get('label')

        # Option mode
        _optMode = options.get('mode')

        # Option label
        _optLabel = options.get('label')

        # Option path
        _mgr = BackupManager()
        _optPath = options.get('path')
        _optPath = _mgr.parse_backup_file_path(_optPath, label=_optLabel)

        log.info('Archive path : %s' % _optPath)

        # Option content
        _optContent = options.get('content')

        # Option confirm
        _optConfirm = options.get('confirm', False)

        # Process command
        if _optMode == 'backup':
            if _optContent != 'all':
                _mgr.backup_config(_optPath)
                # config.Configurator.backup(_optPath, conf_name=_optContent)
            else:
                # config.Configurator.backup(_optPath)
                _mgr.backup_config(_optPath)

        elif _optMode == 'restore':
            # config.Configurator.restore(_optPath)
            _mgr.restore_config(_optPath)

        exit(0)
