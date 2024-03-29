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
        fix = 0
        pix = 0
        totalpix = 0
        for x in range(len(pixel_list)):
            if pix > self.fixtures[fix].num_pixels - 1:
                #print "Next fixture: pix = %d, x = %d" % (pix, x)
                pix = 0
                fix += 1

            if fix > len(self.fixtures) - 1:
                print "Warning: got more data than the strand length (%d vs %d)" % (totalpix, len(pixel_list))
                return
            pix += 1
            totalpix += 1

            r = pixel_list[x][0]
            g = pixel_list[x][1]
            b = pixel_list[x][2]
            self.fixtures[fix].pixels[pix].set(r, g, b)

        #print "last fix = %d, last pix = %d" % (fix, pix)
