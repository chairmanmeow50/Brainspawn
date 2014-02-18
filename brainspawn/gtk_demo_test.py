import unittest
from gtk_demo import MainFrame
from simulator.watcher_manager import WatcherManager
from simulator.simulator import Simulator
from simulator.datalog import Datalog
from simulator.datalog_manager import DatalogManager
import numpy
import simulator
from spa_sequence.spa_sequence import net, pThal
import simulator.watchers

# Here's our "unit".

# Here's our "unit tests".
class MainFrameTests(unittest.TestCase):
  
    def setUp(self):
        self.sim = simulator.Simulator(net, net.dt)
        self.datalog_manager = DatalogManager()
        self.watcher_manager = WatcherManager(self.datalog_manager)
#         self.datalog = Datalog(self.datalog_manager, )
#         self.watcher = 
  
    def testMagnitude(self):
        mf = MainFrame()
        mag = mf.magnitude(3, 4)
        self.failUnless(mag == 5)
        
    def testSimulatorInit(self):
        self.assertEqual(self.sim.min_tick, 0)
        self.assertEqual(self.sim.max_tick, 0)
        
#     def testSimulatorAddWatcher(self):
#         self.sim.add_watcher(self.watcher)
        
    def testSimulatorTick(self):
        self.sim.tick()
        self.assertEqual(self.sim.current_tick, 1)
        
#     def testSimulatorReset(self):

    def testDatalogManagerInit(self):
        self.assertEquals(len(self.datalog_manager.items), 0)
        self.assertEquals(self.datalog_manager.tick_count, 0)
        self.assertEquals(self.datalog_manager.tick_limit, DatalogManager.DEFAULT_TICK_LIMIT)
        self.assertEquals(self.datalog_manager.processing, False)

    def testDatalogManagerAdd(self):
        self.datalog_manager.add(lambda:[])
        self.assertEquals(len(self.datalog_manager.items), 1)
        
    def testDatalogManagerTick(self):
        self.datalog_manager.tick()
        self.assertEquals(self.datalog_manager.tick_count, 1)
        
    def testDatalogManagerReset(self):
        self.datalog_manager.reset()
        self.assertEquals(self.datalog_manager.tick_count, 0)
        
    def testWatcherManagerInit(self):
        self.assertEquals(self.watcher_manager.datalog_manager, self.datalog_manager)
        self.assertEquals(len(self.watcher_manager.objects), 0)
        self.assertEquals(len(self.watcher_manager.watchers), 0)
        self.assertEquals(len(self.watcher_manager.active), 0)
        
    def testWatcherManagerAddObject(self):
        self.watcher_manager.add_object("test", None)
        self.assertTrue(self.watcher_manager.objects.has_key("test"))
        self.assertEquals(self.watcher_manager.objects.get("test"), None)
        
    def testWatcherManagerAddWatcher(self):
        lfpwatcher = simulator.watchers.LFPSpectrogramWatcher()
        self.watcher_manager.add_watcher(lfpwatcher)
        self.assertEquals(self.watcher_manager.watchers.count(lfpwatcher), 1)
        
    def testWatcherManagerListWatcherViews(self):
        self.watcher_manager.add_object("test", None)
        self.assertEquals(len(self.watcher_manager.list_watcher_views("test")), 0)
        
        
#     def testDatalogReset(self):
#         self.datalog.tick()
#         self.datalog.reset()
#         self.failUnless(self.datalog.data == numpy.array([]))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
