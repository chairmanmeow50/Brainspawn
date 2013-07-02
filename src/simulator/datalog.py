import sys
import math
import threading
import numpy


class Datalog:

    def __init__(self, parent, func, args=(), kwargs={}, type=None, offset=0):
        self.semaphore = threading.Semaphore()
        self.parent = parent
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.data = numpy.array([])
        self.filtered = {}
        self.offset = offset
        self.type = type
        self.length = None
        self.tick()

    def tick(self, limit=None):
        self.semaphore.acquire()
        try:
            v = self.func(*self.args, **self.kwargs)
        except Exception, e:
            print("Tick error:", self.func,
                   self.args, self.kwargs, '\n', e)
            v = None
        if self.length is None:
            self.length = len(v)
        else:
            if len(v) < self.length:
                v = numpy.append(v, numpy.zeros(self.length - len(v)))
            elif len(v) > self.length:
                v = v[:self.length]
        self.data = numpy.append(self.data, v)
        if limit is not None and len(self.data) > limit:
            delta = len(self.data) - limit
            self.offset += delta
            self.data = self.data[delta:]
            for k, v in self.filtered.items():
                if len(v) <= delta:
                    del self.filtered[k]
                else:
                    self.filtered[k] = v[delta:]
        self.semaphore.release()

    def reset(self):
        self.semaphore.acquire()
        self.data = numpy.array([])
        self.filtered = {}
        self.offset = 0
        self.semaphore.release()
        self.tick()

    def update_filter(self, dt_tau):
        self.semaphore.acquire()
        self.parent.processing = True
        if dt_tau not in self.filtered:
            f = numpy.array([[x * dt_tau for x in self.data[0]]])
            self.filtered[dt_tau] = f
        else:
            f = self.filtered[dt_tau]
        if len(f) < len(self.data):
            v = f[-1][:]
            d = self.data
            decay = math.exp(-dt_tau)
            n = len(self.data[0])
            for i in range(len(f), len(d)):
                v = [numpy.append(v[j] * decay, d[i][j] * (1 - decay))
                        for j in range(n)]
                f = numpy.append(f, v[:])
        self.parent.processing = False
        self.semaphore.release()
        return f

    def get(self, start=None, count=None, dt_tau=None):
        self.semaphore.acquire()
        if dt_tau is None:
            d = self.data
        else:
            self.semaphore.release()
            d = self.update_filter(dt_tau)
            self.semaphore.acquire()
        off = self.offset
        if start is None:
            start = 0
        if count is None:
            count = len(d) + off
        if off > start + count:
            r = numpy.array([])
        elif off > start:
            r = numpy.zeros(off - start)
            r = numpy.apppend(r, d[:count - off + start])
        else:
            r = d[start - off:start - off + count]
        if len(r) < count:
            r = numpy.append(r, numpy.zeros(count - len(r)))
        self.semaphore.release()
        return r

    def get_first(self):
        return self.data[0]
