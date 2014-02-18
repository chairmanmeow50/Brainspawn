from datalog import Datalog


class DatalogManager:

    DEFAULT_TICK_LIMIT = 4001

    def __init__(self):
        self.items = []
        self.tick_count = 0
        self.tick_limit = self.DEFAULT_TICK_LIMIT
        self.processing = False

    def add(self, func, args=(), kwargs={}, type=None):
        item = Datalog(self, func, args=args, kwargs={},
                type=type, offset=self.tick_count)
        self.items.append(item)
        return item

    def remove(self, item):
        self.items.remove(item)

    def tick(self):
        for item in self.items:
            item.tick(limit=self.tick_limit)
        self.tick_count += 1

    def reset(self):
        for item in self.items:
            item.reset()
        self.tick_count = 0
