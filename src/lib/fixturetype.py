class FixtureType:

    def __init__(self, name="", num_pixels=0, boundbox=(0, 0), channels_per_pixel=3, bits_per_channel=8):
        self.name = name
        self.num_pixels = num_pixels
        self.boundbox = boundbox
        self.channels_per_pixel = channels_per_pixel
        self.bits_per_channel = bits_per_channel
        self.pixel_locations = []

    def __repr__(self):
        return "FixtureType: {name: '%s', num_pixels: %d}" % (self.name, self.num_pixels)
