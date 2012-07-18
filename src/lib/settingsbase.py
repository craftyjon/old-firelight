import ConfigParser


class SettingsBase:

    def __init__(self, filename=None):
        self.filename = filename

    def load(self):
        if not self.filename:
            return False

        self.cp = ConfigParser.ConfigParser()
        self.cp.read(self.filename)

        print self.cp.sections()
