# -*- coding: utf-8 -*-


class VersionStatus(object):
    ALPHA = 'Alpha'
    BETA = 'Beta'
    RELEASECANDIDATE = 'RC'
    RELEASE = 'build'


class Version(object):

    def __init__(self, MAJOR, MINOR, BUILD, STATUS, REVISION, COMMENT=None):
        self.MAJOR = MAJOR
        self.MINOR = MINOR
        self.BUILD = BUILD
        self.STATUS = STATUS
        self.REVISION = REVISION
        self.COMMENT = COMMENT

    @property
    def Version(self):
        return '%s.%s.%s' % (self.MAJOR, self.MINOR, self.BUILD)

    @property
    def Revision(self):
        return '%s %s' % (self.STATUS, self.REVISION)

    @property
    def VersionFull(self):
        return '%s %s' % (self.Version, self.Revision)

    @property
    def Version_Underscored(self):
        return str(self.Version).replace('.', '_')

    def Comment(self):
        return self.COMMENT if (self.COMMENT not in [None, '']) else 'n.a.'
