class Fixture:

    def __init__(self, id=0, offset=0, ft="", position=(0, 0), scale=1.0, angle=0.0, num_pixels=0, pixels=[]):
        self.id = id
        self.offset = offset
        self.type = ft
        self.position = position
        self.scale = scale
        self.angle = angle
        self.num_pixels = num_pixels
        self.pixels = pixels

    def __repr__(self):
        return "Fixture: {id=%d, offset=%d, type='%s'}" % (self.id, self.offset, self.type)
