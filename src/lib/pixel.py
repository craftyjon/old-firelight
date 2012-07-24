class Pixel:

    def __init__(self, position=(0, 0), channels=3, bits_per_channel=8):
        self.position = position  # Position within fixture, relative coords
        self.channels = channels
        self.bits_per_channel = bits_per_channel
        self.value = [0, 0, 0]

    def __repr__(self):
        return "Pixel: {position: (%d, %d)}" % ((self.position[0], self.position[1]))

    def set(self, r, g, b):
        self.value = [r, g, b]

    def get(self):
        return (self.value[0], self.value[1], self.value[2])
