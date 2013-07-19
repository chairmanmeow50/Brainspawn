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
            value = self.func(*self.args, **self.kwargs)
        except Exception, e:
            print("Tick error:", self.func,
                   self.args, self.kwargs, '\n', e)
            value = None
        if self.length is None:
            self.length = len(value)
        else:
            if len(value) < self.length:
                value = numpy.append(value, numpy.zeros(self.length - len(value)))
            elif len(value) > self.length:
                value = value[:self.length]
        if (len(self.data) == 0):
            self.data = numpy.array([value])
        else:
            self.data = numpy.append(self.data, [value], axis=0)
        if limit is not None and len(self.data) > limit:
            delta = len(self.data) - limit
            self.offset += delta
            self.data = self.data[delta:]
            for k, value in self.filtered.items():
                if len(value) <= delta:
                    del self.filtered[k]
                else:
                    self.filtered[k] = value[delta:]
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
            # take first element in data, all elements multiplied by dt_tau
            filtered_data = numpy.array([[x * dt_tau for x in self.data[0]]])
            self.filtered[dt_tau] = filtered_data
        else:
            filtered_data = self.filtered[dt_tau]
        if len(filtered_data) < len(self.data):
            last_filtered_element = filtered_data[-1]
            unfiltered_data = self.data
            decay = math.exp(-dt_tau)
            n = len(self.data[0])
            for i in range(len(filtered_data), len(unfiltered_data)):
                last_filtered_element = numpy.array([last_filtered_element[j] * decay + unfiltered_data[i][j] * (1 - decay)
                        for j in range(n)])
                filtered_data = numpy.append(filtered_data, [last_filtered_element], axis=0)
        self.parent.processing = False
        self.semaphore.release()
        return filtered_data

    def get(self, start=None, count=None, dt_tau=None):
        self.semaphore.acquire()
        if dt_tau is None:
            data = self.data
        else:
            self.semaphore.release()
            data = self.update_filter(dt_tau)
            self.semaphore.acquire()
        offset = self.offset
        if start is None:
            start = 0
        if count is None:
            count = len(data) + offset
        if offset > start + count:
            # return empty 1-d array
            result = numpy.array([])
        elif offset > start:
            # no data before offset, pad with zeros
            result = numpy.zeros(offset - start)
            result = numpy.append(result, data[:count - offset + start], axis=0)
        else:
            result = data[start - offset:start - offset + count]
        if len(result) < int(count):
            # pad with zeros
            result = numpy.append(result, numpy.zeros(int(count)- len(result)), axis=0)
        self.semaphore.release()
        return result

    def get_first(self):
        return self.data[0]
