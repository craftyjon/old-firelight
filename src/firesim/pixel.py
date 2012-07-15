class Pixel:

    def __init__(self):
        self.position = (0, 0)  # Position within fixture, relative coords
        self.channels = 3
        self.bits_per_channel = 8
        self.value = [0, 0, 0]
