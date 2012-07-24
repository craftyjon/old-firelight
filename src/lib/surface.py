class Surface:

    def __init__(self, name="Untitled Surface", dimensions=(0, 0), reference_image=""):
        self.name = name
        self.dimensions = dimensions
        self.reference_image = reference_image
        self.strands = []
        self.active_strand = 0

    def __repr__(self):
        rs = "Surface: {name='%s'}" % self.name
        for strand in self.strands:
            rs += '\n\t' + repr(strand)
        return rs

    def set_all(self, pixel_list):
        for strand in self.strands:
            strand.set_all(pixel_list)
