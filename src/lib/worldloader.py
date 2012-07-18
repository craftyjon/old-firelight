import json

from fixturetype import FixtureType
from surface import Surface
from strand import Strand
from fixture import Fixture
from pixel import Pixel


class WorldObject:

    def __init__(self):
        self.loaded = False
        self.fixture_types = []
        self.surfaces = []

    def __repr__(self):
        s = "WorldObject:"
        for t in self.fixture_types:
            s += "\n\t" + repr(t).replace('\n\t', '\n\t\t')

        for surf in self.surfaces:
            s += "\n\t" + repr(surf).replace('\n\t', '\n\t\t')

        return s


class WorldLoader:

    def __init__(self, filename=None):
        self.open_file(filename)

    def open_file(self, filename):
        self.file_loaded = False
        if filename is not None:
            with open(filename) as f:
                try:
                    self.cd = json.load(f)
                except:
                    print "Error loading world from " + filename
                    self.cd = None
                    return

            self.file_loaded = True

    def load(self):
        if not self.file_loaded:
            print "Error: no file loaded"
            return None

        co = WorldObject()

        cft = self.cd.get("fixture_types", None)

        if cft is not None:
            for ct in cft:
                boundbox = map(int, ct['boundbox'].split(','))
                t = FixtureType(ct['name'], ct['num_pixels'], tuple(boundbox), ct['channels_per_pixel'], ct['bits_per_channel'])

                for loc in ct['pixel_locations']:
                    locn = map(int, loc.split(','))
                    pixel = Pixel(locn, t.channels_per_pixel, t.bits_per_channel)
                    t.pixel_locations.append(pixel)

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
                        ft = co.fixture_types[next(index for (index, d) in enumerate(co.fixture_types) if d.name == fix['type'])]
                        fixture = Fixture(fix['id'], fix['offset'], ft, position, fix['scale'], fix['angle'])

                        strand.fixtures.append(fixture)

                    s.strands.append(strand)

                co.surfaces.append(s)

        return co


if __name__ == '__main__':
    wl = WorldLoader('test_world.json')

    wo = wl.load()

    print wo
