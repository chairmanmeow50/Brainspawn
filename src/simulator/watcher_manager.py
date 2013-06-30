class WatcherManager:

    def __init__(self, datalog_manager):
        self.datalog_manager = datalog_manager
        self.objects = {}
        self.watchers = []
        self.active = {}

    def add_object(self, name, obj):
        assert name not in self.objects
        self.objects[name] = obj

    def add_watcher(self, watcher):
        self.watchers.append(watcher)
        self.watchers.sort(key=lambda w: w.priority())

    def activate_watcher(self, name, func, args=()):
        for key in self.active.keys():
            if (name, func, args) == key:
                w = self.active[key]
                break
        else:
            w = self.datalog_manager.add(func, args=tuple(
                [self.objects[name]] + list(args)))
            w.watch_count = 0
            self.active[(name, func, args)] = w
        w.watch_count += 1
        return w

    def list_watcher_views(self, name):
        r = []
        obj = self.objects[name]
        for w in self.watchers:
            if w.check(obj):
                r.extend(w.views(obj))
        return r

    def is_watched_object(self, name):
        obj = self.objecs[name]
        for w in self.watches:
            if w.check(obj):
                return True

        return False

    def reset(self):
        self.datalog_manager.reset()
