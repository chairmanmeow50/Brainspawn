import nengo

import networkx as nx
import matplotlib.pyplot as plt

class Network_View():
    def update(self):
        pass

    def clear(self):
        pass

    def get_figure(self):
        return self._figure

    def get_obj(self, node_name):
        return self._graph_name_to_obj.get(node_name)

    def get_name(self, nengo_obj):
        return self._graph_obj_to_name.get(nengo_obj)

    def _associate_obj_name(self, node_name, nengo_obj):
        self._graph_name_to_obj[node_name] = nengo_obj
        self._graph_obj_to_name[nengo_obj] = node_name

    def _build_graph(self, model):
        self.G = nx.MultiDiGraph()
        self._graph_name_to_obj = {}
        self._graph_obj_to_name = {}

        # Add ensembles and nodes
        for obj in model.objs:
            name = None
            if isinstance(obj, nengo.Ensemble):
                # print "obj.label       = ", obj.label
                # print "obj.dimensions  = ", obj.dimensions
                # print "obj.n_neurons   = ", obj.n_neurons
                # print "obj.probes      = ", obj.probes
                # print "obj.radius      = ", obj.radius
                name = _find_uniq_name(obj.label, self.G.nodes())
                print "Adding ensemble:", name
            elif isinstance(obj, nengo.Node):
                # print "obj.label      = ", obj.label
                # print "obj.dimensions = ", obj.dimensions
                # print "obj.output     = ", obj.output
                # print "obj.probes     = ", obj.probes
                name = _find_uniq_name(obj.label, self.G.nodes())
                print "Adding node:", name
            else:
                print "Error: Uknown model object \"", str(obj), "\", unable to add to network view."
                name = str(obj)

            if name is not None:
                self.G.add_node(name, obj=obj)
                self._associate_obj_name(name, obj)


        # Add connections
        for conn in model.connections:
            # print "conn.label       = ", conn.label
            # print "conn.pre         = ", conn.pre
            # print "conn.post        = ", conn.post
            # print "conn.dimensions  = ", conn.dimensions
            # print "conn.filter      = ", conn.filter
            # print "conn.probes      = ", conn.probes
            # print "conn.transform   = ", conn.transform
            # print "conn.modularity  = ", conn.modulatory

            # The following are listed as attributes but cause an error when accessed
            ### print "conn.decoders    = ", conn.decoders
            ### print "conn.eval_points = ", conn.eval_points

            pre_name = self.get_name(conn.pre)
            post_name = self.get_name(conn.post)

            if pre_name is None:
                print "Error: unable to determine connection's pre. Dropping edge \"%s\"." % (conn.pre)
                continue
            if pre_name is None:
                print "Error: unable to determine connection's post. Dropping edge \"%s\"." % (conn.pre)
                continue

            # TODO(gmdavis): lookup names (may be modified in duplicate prevention)
            print "Adding edge: \"%s\" to \"%s\"" % (pre_name, post_name)
            self.G.add_edge(pre_name, post_name)

        # TODO(gmdavis): add probes?

    def decide_obj_color(self, nengo_obj):
        if isinstance(nengo_obj, nengo.Node):
            return (1,1,0)
        if isinstance(nengo_obj, nengo.Ensemble):
            return (1,0,1)
        else:
            return (1,1,1) # white

    def __init__(self, sim_manager, model, name="Network View", *args, **kwargs):
        self.sim_manager = sim_manager
        self._figure = plt.figure()
        self.model = model
        self.G = None
        self._graph_name_to_obj = {}

        # Graph construction
        self._build_graph(model)

        colors = [self.decide_obj_color(self.get_obj(obj)) for obj in self.G.nodes()]

        nx.draw_graphviz(self.G, node_color=colors, node_size=400)

#---------- Helper functions --------

def _find_uniq_name(name, collection, threashold=1000):
    if name not in collection:
        return name

    orig_name = name
    count = 1
    while name in collection:
        if count >= threashold:
            print "Error: %d existing copies of %s. Not creating another." % (count, name)
            return None
        name = orig_name + " (%d)" % count
        count += 1

    print "Warning: modifying original name to \"%s\" to make it unique." % (name)
    return name

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

    def add_to_graph(self, G):
        G.add_nodes_from(self.ensembles)
        G.add_nodes_from(self.nodes)
        G.add_edges_from(self.conns)

#---------- Main method (testing) --------

import sample_networks.two_dimensional_rep as example

def main():
    nv = Network_View(sim_manager=None, model=example.model)
    fig = nv.get_figure()
    fig.show()
    plt.show()

if __name__ == '__main__':
    main()