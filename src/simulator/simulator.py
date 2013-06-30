import datalog_manager
import watcher_manager


class Simulator:

    def __init__(self, net, dt):
        self.min_tick = 0
        self.max_tick = 0
        self.current_tick = 0
        self.dt = dt
        self.net = net
        self.datalog_manager = datalog_manager.DatalogManager()
        self.watcher_manager = watcher_manager.WatcherManager(self.datalog_manager)

    def add_watcher(self, watcher):
        self.watcher_manager.add_watcher(watcher)

    def tick(self):
        if (self.current_tick > self.datalog_manager.tick_count):
            self.net.run(self.dt)
            self.datalog_manager.tick()
            self.min_tick = max(0, self.datalog_manager.tick_count -
                    self.datalog_manager.tick_limit + 1)
            self.max_tick = self.datalog_manager.tick_count
        self.current_tick += 1
