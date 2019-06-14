# -*- coding:utf-8 -*-
import os
import sys
import zipfile

from . import utils_str


def create_temporary_directory(root_dir):
    _tmpPath = ''
    _folderExists = True
    while _folderExists:
        _tmpDir = generate_random_folder()
        _tmpPath = '%s\\%s' % (root_dir, _tmpDir)
        if not os.path.exists(_tmpPath):
            _folderExists = False
    try:
        _pathData = _tmpPath.split('\\')
        for i in range(1, len(_pathData) + 1):
            _path = '\\'.join([_f for _f in _pathData[:i]])
            if not os.path.exists(_path):
                os.mkdir(_path)

    except Exception as e:
        _msg = 'Error while creating temporary folder %s : %s, %s' % (_tmpPath, type(e).__name__, e)
        return False, _msg
    return True, _tmpPath


def file_size_as_label(numeric_size):
    if numeric_size is None:
        return ''
    if type(numeric_size) is not str:
        numeric_size = str(numeric_size)
    numeric_size += '.0'
    numeric_size = float(numeric_size)
    if ('%s' % numeric_size).__len__() > 11:
        unit = "Gb"
        str_size = numeric_size / 1000000000
    elif ('%s' % numeric_size).__len__() > 8:
        unit = "Mb"
        str_size = numeric_size / 1000000
    elif ('%s' % numeric_size).__len__() > 5:
        unit = "Kb"
        str_size = numeric_size / 1000
    else:
        str_size = '%s' % numeric_size
        unit = "bytes"
    str_size = '%s' % str_size
    if str_size[len(str_size) - 2:] == '.0':
        str_size = str_size[:len(str_size) - 2]
    try:
        str_size = '%s' % str_size
        str_size = str_size[:str_size.index('.') + 2]
    except Exception as e:
        pass
    disk_space_str = '%s %s' % (str_size, unit)
    return disk_space_str


def generate_random_folder():
    return utils_str.generate_random(length=16)


def unzip_file(file_path, output_dir):
    try:
        zip_file = zipfile.ZipFile(file_path)
        zip_file.extractall(output_dir)
    except Exception as e:
        _msg = 'unzip_file error: %s %s' % (type(e).__name__, e)
        return False, _msg
    finally:
        zip_file.close()
    return True, None


def zip_folder(folder_path, output_path):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    # Retrieve the paths of the folder contents.
    contents = os.walk(folder_path)
    try:
        zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
        for root, folders, files in contents:
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path[len(folder_path) + 1:]
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path[len(folder_path) + 1:]
                zip_file.write(absolute_path, relative_path)
    except IOError as e:
        sys.exit(1)
    except OSError as e:
        sys.exit(1)
    except zipfile.BadZipfile as e:
        sys.exit(1)
    finally:
        zip_file.close()
