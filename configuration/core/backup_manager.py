# -*- coding:utf-8 -*-
from datetime import datetime as dt
import os
import shutil

from main.core import config, utils_file
from main.core.logger import Log


class BackupManager(object):

    def __init__(self, verbose=False):
        self.verbose = verbose

    def parse_backup_file_path(self, input_value, label=None):
        """
            Build an archive path according to the input value:

                * if input_value targets a file: returns the backup path using given archive name
                * if input_value targets a folder: returns the backup path using a generated archive name
            :param input_value: desired path or folder for archive
            :type input_value: str
            :param label: additional label for the archive
            :type label: str, None
            :return: the final (parsed) archive path
            :rtype: str
        """
        log = Log(self)

        _slashPos = input_value.rfind('\\')
        _dotPos = input_value.rfind('.')
        if _dotPos > _slashPos:
            _filePath = input_value
        else:
            _now = dt.now()
            if label:
                _fileNameDetails = label
            else:
                _fileNameDetails = '%s-%s-%s_%sh%s' % (_now.year,
                                                       str(_now.month).rjust(2, '0'),
                                                       str(_now.day).rjust(2, '0'),
                                                       str(_now.hour).rjust(2, '0'),
                                                       str(_now.minute).rjust(2, '0'))
            _fileName = '%s.zip' % _fileNameDetails
            _filePath = '%s\\%s' % (input_value, _fileName)

        log.debug(returns=_filePath)
        return _filePath

    def backup_config(self, archive_path):
        """
            Dump (as .zip) MCM configuration to archive_path
            :param archive_path: path of the archive to dump the configuration into
            :type archive_path: str
            :return: (success / error, archive size / error message)
            :rtype: tuple
        """
        log = Log(self)

        # remove output file if already exists and force option is set
        if os.path.exists(archive_path):

            # erase file
            try:
                log.info('Erase existing archive : %s' % archive_path)
                os.unlink(archive_path)
            except Exception as e:
                _msg = 'Error while removing existing output file : %s, %s' % (type(e).__name__, e)
                log.error(_msg)
                return False, _msg

        # create a temporary directory
        _tmpDir = self._create_temporary_directory(archive_path)
        log.info('Temporary directory created : %s' % _tmpDir)

        # copy configuration files to temporary directory
        log.info('Export MCM configuration resources to temporary folder')
        for _confRes in config.Configurator.registry:
            _confRes.backup(_tmpDir)

        # zip temporary directory to archive_path
        log.info('Zip temporary folder')
        try:
            utils_file.zip_folder(_tmpDir, archive_path)
        except Exception as e:
            _msg = 'Error while zipping backup from %s to %s : %s, %s' % (_tmpDir, archive_path, type(e).__name__, e)
            log.error(_msg)
            return False, _msg

        # measure size of backup
        _fileSize = os.path.getsize(archive_path)
        log.info('Backup size : %s octets (%s)' % (_fileSize, utils_file.file_size_as_label(_fileSize)))

        # delete temporary directory
        log.info('Remove temporary folder')
        try:
            shutil.rmtree(_tmpDir)
        except Exception as e:
            _msg = 'Error while removing temporary folder %s : %s, %s' % (_tmpDir, type(e).__name__, e)
            log.error(_msg)

        return True, _fileSize

    def restore_config(self, archive_path):
        """
            Restore a MCM configuration archive to archive_path
            :param archive_path: path of the archive to restore the configuration from
            :type archive_path: str
            :param force: Must be set to force the restoration of the given archive
            :type force: bool
            :return: (success / error, None / error message)
            :rtype: tuple
        """
        log = Log(self)

        if not os.path.exists(archive_path):
            _msg = 'Archive not found : %s' % archive_path
            log.error(_msg)
            return False, _msg

        # create temporary folder
        _tmpDir = self._create_temporary_directory(archive_path)

        # unzip archive_path to temporary directory
        log.info('Unzip backup to temporary folder')
        _success, _data = utils_file.unzip_file(archive_path, _tmpDir)
        if not _success:
            _msg = 'Error while unzipping backup %s to %s : %s' % (archive_path, _tmpDir, _data)
            log.error(_msg)
            return False, _msg

        # restore configuration from temporary directory
        log.info('Restore configuration resources')
        for _confRes in config.Configurator.registry:
            _confRes.restore(_tmpDir)

        # delete temporary directory
        log.info('Remove temporary folder')
        try:
            shutil.rmtree(_tmpDir)
        except Exception as e:
            _msg = 'Error while removing temporary directory %s : %s, %s' % (_tmpDir, type(e).__name__, e)
            log.error(_msg)

        return True, None

    def _create_temporary_directory(self, folder):
        log = Log(self)

        log.info('Create temporary folder')
        _tmpRootDir = folder[:folder.rfind('\\')] if folder.find('\\') > 0 else '.\\'

        _success, _data = utils_file.create_temporary_directory(_tmpRootDir)
        if not _success:
            _msg = 'Error while creating temporary folder in %s : %s' % (_tmpRootDir, _data)
            log.error(_msg)
            raise Exception(_msg)

        return _data
