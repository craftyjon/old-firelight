"""FireServe is the backend server for FireLight"""

import threading
import sys
import time
import colorsys
import signal
import socket
from Queue import Queue, Full, Empty
from copy import copy

from lib.util import *
from lib.loopingthread import LoopingThread

from node import Node


n = None
pixels = []
colorshift = 0.0
updater = None
rainbow_loop = None
pixel_lock = threading.RLock()
pixel_queue = Queue()


class NodeUpdater(threading.Thread):
    def __init__(self, node_list):
        threading.Thread.__init__(self)
        self.node_list = node_list
        self.exit_flag = False

    def connect(self):
        for node in self.node_list:
            node.connect()

    def run(self):
        while not self.exit_flag:
            try:
                p = pixel_queue.get(False)
            except Empty:
                continue
            try:
                self.node_list[0].set_all(p)
                #print "Sent message"
                time.sleep(1.0 / 30.0)
            except socket.error, e:  # TODO: add specific exceptions
                print "Error sending!", e[1]
                self.connect()
                time.sleep(1.0 / 4.0)

    def stop(self):
        for node in self.node_list:
            node.disconnect()


def rainbow_tick():
    global colorshift, pixels, pixel_queue

    for i in range(160):
        h = (float(i) / 160) + colorshift
        (r, g, b) = map(lambda f: int(255.0 * f), colorsys.hsv_to_rgb(h, 1.0, 1.0))
        pixels[i] = [r, g, b]

    try:
        pixel_queue.put(copy(pixels), block=False)
    except Full:
        print "Queue full"

    colorshift += 0.0075


def tick():
    rainbow_tick()


def signal_handler(signum, frame):
    global updater, rainbow_loop
    print "Caught signal, exiting..."
    if updater:
        updater.exit_flag = True
        updater.join()
    if rainbow_loop:
        rainbow_loop.stop()
    sys.exit(0)


if __name__ == "__main__":

    n = Node(ip_addr="127.0.0.1", port=5200)

    pixels = [[0, 0, 0] for i in range(160)]
    pixel_queue.put(copy(pixels))

    signal.signal(signal.SIGINT, signal_handler)

    updater = NodeUpdater([n])
    updater.connect()
    updater.start()

    rainbow_loop = LoopingThread((1.0 / 30.0), tick)
    rainbow_loop.run()
