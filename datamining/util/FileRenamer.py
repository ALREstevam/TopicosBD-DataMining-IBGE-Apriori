
class FileRenamer:
    def __init__(self, filename):
        self.fullfilename = filename
        self.extention = '.'.join(filename.split('.')[-1:])
        self.filename = '.'.join(filename.split('.')[:-1])


    def appendNameAtEnd(self, name):
        return '{}{}.{}'.format(self.filename, name, self.extention)

    def appendNameAtBegin(self, name):
        return '{}{}.{}'.format(name, self.filename, self.extention)

    def changeExtention(self, ext):
        return '{}.{}'.format(self.filename, ext)