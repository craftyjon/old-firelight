class Strand:

    def __init__(self, name="Untitled Strand", type="", address=0, num_pixels=0, ip_address="127.0.0.1", port=5202):
        self.name = name
        self.type = type
        self.address = address
        self.num_pixels = num_pixels
        self.ip_address = ip_address
        self.port = port
        self.fixtures = []

    def __repr__(self):
        s = "Strand: {name='%s', address=%d, num_pixels=%d, net=%s:%d}" % (self.name, self.address, self.num_pixels, self.ip_address, self.port)
        for fix in self.fixtures:
            s += '\n\t\t' + repr(fix)
        return s

    def set_all(self, pixel_list):
        i = 0
        for fix in self.fixtures:
            for j in range(fix.num_pixels):
                r = pixel_list[i + j][0]
                g = pixel_list[i + j][1]
                b = pixel_list[i + j][2]
                fix.pixels[j].set(r, g, b)
            i += fix.num_pixels
