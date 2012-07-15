class Fixture:

    def __init__(self, id=0, offset=0, type="", position=(0, 0), scale=1.0, angle=0.0):
        self.id = id
        self.offset = offset
        self.type = type
        self.position = position
        self.scale = scale
        self.angle = angle

    def __repr__(self):
        return "Fixture: {id=%d, offset=%d, type='%s'}" % (self.id, self.offset, self.type)
