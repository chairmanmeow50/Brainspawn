import unittest
import nengo
import time
import numpy as np
import matplotlib.pyplot as plt
from brainspawn.simulator.sim_manager import SimManager
from brainspawn.sample_networks.two_dimensional_rep import model, sin, cos, neurons

class SimManagerTests(unittest.TestCase):
    """Test cases for SimManager
    """

    #TODO - Mike really needs to add real tests here...

    def test_simulator(self):
        """Runs simulator
        Not really a unit test, more of an integration test
        and/or demo of the simulator
        """

        # Init the sim_manager with a basic model
        sim_manager = SimManager()
        sim_manager.load_new_model(model, 0.001)

        #Assert model contains expected nodes, connections?

        # What graphs can I show for some Ensemble?
        node_caps = sim_manager.get_caps_for_obj(neurons)
        for cap in node_caps:
            print (cap.name, cap.get_out_dimensions(neurons))
            if (cap.name is 'output'):
                out_cap = cap

        assert(out_cap)

        # Okay, show a basic xy plot
        plt.ion()
        p1,p2 = plt.plot([], np.empty((0, 2)))
        text = []

        # Create update function, subscribe it
        def update_graph(data, start_time):
            start = start_time/sim_manager.dt
            count = sim_manager.current_step - sim_manager.min_step
            t = np.linspace(start, start + data[start:count].shape[0]*sim_manager.dt, data[start:count].shape[0])
            p1.set_xdata(t)
            p1.set_ydata(data[start:count,:1])
            p2.set_xdata(t)
            p2.set_ydata(data[start:count,1:])

            if(not text and len(t) > 10):
                text.append(plt.text(0.2, 0.67, "such line", fontsize=18, color='orange'))
                text.append(plt.text(0.7, 0.5, "very neuron", fontsize=18, color='green'))
                text.append(plt.text(0.5, 0.2, "wow", fontsize=18, color='purple'))
            elif (text and len(t) < 275):
                for txt in text:
                    txt.set_x((txt.get_position()[0]*100000 + len(t))/100000 % 1 )
            plt.draw()

        sim_manager.connect_to_obj(neurons, out_cap, update_graph)

        # Run the simulation for a bit
        for i in range(1000):
            time.sleep(.001)
            sim_manager.step()

        # Hey, everything worked
        assert(True)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
