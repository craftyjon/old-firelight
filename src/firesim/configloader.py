import json

from fixturetype import FixtureType
from surface import Surface
from strand import Strand
from fixture import Fixture
from pixel import Pixel


class ConfigObject:

    def __init__(self):
        self.loaded = False
        self.fixture_types = []
        self.surfaces = []

    def __repr__(self):
        s = "ConfigObject:"
        for t in self.fixture_types:
            s += "\n\t" + repr(t).replace('\n\t', '\n\t\t')

        for surf in self.surfaces:
            s += "\n\t" + repr(surf).replace('\n\t', '\n\t\t')

        return s


class ConfigLoader:

    def __init__(self, filename=None):
        self.open_file(filename)

    def open_file(self, filename):
        self.file_loaded = False
        if filename is not None:
            with open(filename) as f:
                try:
                    self.cd = json.load(f)
                except:
                    print "Error loading config from " + filename
                    self.cd = None
                    return

            self.file_loaded = True

    def load(self):
        if not self.file_loaded:
            print "Error: no file loaded"
            return

        co = ConfigObject()

        cft = self.cd.get("fixture_types", None)

        if cft is not None:
            for ct in cft:
                boundbox = map(int, ct['boundbox'].split(','))
                t = FixtureType(ct['name'], ct['num_pixels'], tuple(boundbox), ct['channels_per_pixel'], ct['bits_per_channel'])
                co.fixture_types.append(t)

        csl = self.cd.get("surfaces", None)

        if csl is not None:

            for cs in csl:

                dimensions = map(int, cs['dimensions'].split(','))
                reference = cs.get('reference_image', "")
                s = Surface(cs['name'], dimensions, reference)

                for cstr in cs['strands']:

                    strand = Strand(cstr['name'], cstr['type'], cstr['address'], cstr['num_pixels'], cstr['ip_address'], cstr['port'])

                    for fix in cstr['fixtures']:

                        position = map(int, fix['tl'].split(','))
                        fixture = Fixture(fix['id'], fix['offset'], fix['type'], position, fix['scale'], fix['angle'])
                        strand.fixtures.append(fixture)

                    s.strands.append(strand)

                co.surfaces.append(s)

        return co


if __name__ == '__main__':
    cl = ConfigLoader('test_surface.json')

    co = cl.load()

    print co
