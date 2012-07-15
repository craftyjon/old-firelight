class Surface:

    def __init__(self, name="Untitled Surface", dimensions=(0, 0), reference_image=""):
        self.name = name
        self.dimensions = dimensions
        self.reference_image = reference_image
        self.strands = []

    def __repr__(self):
        rs = "Surface: {name='%s'}" % self.name
        for strand in self.strands:
            rs += '\n\t' + repr(strand)
        return rs
