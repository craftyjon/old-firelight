import time
from threading import Thread


class LoopingThread(Thread):

    def __init__(self, interval, fn, args=(), kwargs={}):
        super(LoopingThread, self).__init__(target=fn, args=args, kwargs=kwargs)

        self.__interval = interval
        self.__func = fn
        self.__args = args
        self.__kwargs = kwargs
        self.__exiting = False

    def run(self):
        while not self.__exiting:
            time.sleep(self.__interval)
            self.__func(*self.__args, **self.__kwargs)

    def stop(self):
        self.__exiting = True
