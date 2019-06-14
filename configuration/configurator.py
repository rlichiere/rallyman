# -*- coding:utf-8 -*-
import yaml
import json


class ConfigurationContentTypes(object):
    JSON = 'json'
    YML = 'yml'
    TXT = 'txt'


class Configuration(object):

    def __init__(self, name, file_path, content_type=None):
        self.name = name
        _pathEnd = file_path.rfind('\\')
        self.fileName = file_path[_pathEnd + 1:]
        self.fileFolder = file_path[:_pathEnd]
        self.filePath = file_path

        if content_type:
            self.contentType = content_type
        else:
            _ext = self.filePath[self.filePath.rfind('.'):]
            if _ext == '.json':
                self.contentType = ConfigurationContentTypes.JSON
            elif _ext == '.txt':
                self.contentType = ConfigurationContentTypes.TXT
            elif _ext == '.yml':
                self.contentType = ConfigurationContentTypes.YML
            else:
                raise Exception('Unrecognized content_type : %s' % _ext)

        self.data = None

    def load(self):
        with open(self.filePath) as _file:
            if self.contentType == ConfigurationContentTypes.JSON:
                _fileData = json.loads(_file.read())
            elif self.contentType == ConfigurationContentTypes.TXT:
                _fileData = _file.read()
            elif self.contentType == ConfigurationContentTypes.YML:
                _fileData = yaml.load(_file.read())
            else:
                raise Exception('Unexpected type : %s' % self.contentType)
            return _fileData

    def backup(self, path):
        _sourceFilePath = '%s\\%s' % (self.fileFolder, self.fileName)
        _targetFilePath = '%s\\%s' % (path, self.fileName)

        self.copy_file(_sourceFilePath, _targetFilePath)

    def restore(self, path):
        _sourceFilePath = '%s\\%s' % (path, self.fileName)
        _targetFilePath = '%s\\%s' % (self.fileFolder, self.fileName)
        self.copy_file(_sourceFilePath, _targetFilePath)

    @classmethod
    def copy_file(cls, source_file, target_file):
        with open(source_file, 'r') as _sourceFile, open(target_file, 'w') as _targetFile:
            _targetFile.write(_sourceFile.read())


class Configurator(object):

    registry = list()

    @classmethod
    def register(cls, config_description):
        cls.registry.append(config_description)

    @classmethod
    def load(cls, conf_name):
        for _conf in cls.registry:
            if _conf.name == conf_name:
                return _conf.load()

    @classmethod
    def backup(cls, path, conf_name=None):
        for _conf in cls.registry:
            _conf.backup(path)

    @classmethod
    def restore(cls, path, conf_name=None):
        for _conf in cls.registry:
            _conf.restore(path)
