from lib.settingsbase import SettingsBase


class FireSimSettings(SettingsBase):

    def __init__(self, filename=None):
        SettingsBase.__init__(self, filename)
        self.config = {}
        self.load()

    def load(self):
        SettingsBase.load(self)
        if self.cp.has_section('FireSim'):
            print "Loading settings from file"
            self.config = {}
            self.cp.defaults = {"listen_host": "127.0.0.1", "listen_port": 5200, "world": "test_world.json"}
            self.config['listen_host'] = self.cp.get('FireSim', 'listen_host')
            self.config['listen_port'] = self.cp.getint('FireSim', 'listen_port')
            self.config['world'] = self.cp.get('FireSim', 'world')
            print self.config
        else:
            print "Warning: could not load settings"
