import networkx as nx
import matplotlib.pyplot as plt

class Network_View():
    def tick(self):
        pass

    def clear(self):
        pass

    def get_figure(self):
        return self.figure

    def __init__(self, simulator):
        print "Network_View::__init__()"
        self.simulator = simulator
        self.figure = plt.figure()

        # Graph construction
        self.G = nx.DiGraph()

        # TODO(gmdavis): build graph from simulator's model
        N = MockNengoNetwork(10, 20, 50)
        self.G.add_nodes_from(N.ensembles)
        self.G.add_nodes_from(N.nodes)
        self.G.add_edges_from(N.conns)

        nx.draw_graphviz(self.G)

#---------- Mock objects --------

import random

class MockNengoNetwork:
    """ A simple mock object to represent a network model, containing
    ensembles, nodes, and connections.
    """
    def __init__(self, n_ensembles = None, n_nodes = None, conn_prob = 50):
        self.ensembles = []
        self.nodes = []
        self.conns = []

        if n_ensembles is None:
            n_ensembles = random.randint(3, 10)
        if n_nodes is None:
            n_nodes = random.randint(1, 7)

        # Create ensembles
        for i in range(n_ensembles):
            self.ensembles.append( "ens-" + str(i) )

        # Create nodes
        for i in range(n_nodes):
            self.nodes.append( "node-" + str(i) )

        # Create ensemble connections
        for ens1 in self.ensembles:
            for ens2 in self.ensembles:
                if ens1 == ens2:
                    continue
                if random.randint(1, 100) <= conn_prob:
                    self.conns.append( (ens1, ens2) )

        # Create node connections
        for node in self.nodes:
            target = random.choice( self.ensembles )
            self.conns.append( (node, target) )

#---------- Main method (testing) --------

def main():
    nv = Network_View(simulator=None)
    fig = nv.get_figure()
    fig.show()
    plt.show()

if __name__ == '__main__':
    main()