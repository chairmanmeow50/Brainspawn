import nengo
import networkx as nx
import matplotlib.pyplot as plt
from math import sqrt
from view.visualizations.__visualization import Visualization

class NetworkView(Visualization):
    """Visualization of a model's network
    """
    def __init__(self, sim_manager, controller, model=None, name="Network View", **kwargs):
        super(NetworkView, self).__init__(sim_manager, controller)
        self.sim_manager = sim_manager
        self._model = model
        self.name = name

        self._figure = plt.figure()
        self.init_canvas(self._figure)
        self._figure.patch.set_facecolor('white')

        # Event connections
        self._figure.canvas.mpl_connect('button_press_event', self.onclick)

        # Build graph
        self._node_radius_sq = 100
        self.load_model(model)

    def display_name(self):
        return None

    def supports_cap(self, cap, dimension):
        return False

    def update(self, data, start_time):
        pass

    def clear(self):
        pass

    def nearest_obj(self, x, y):
        if self.model is None:
            return None

        for obj, data_pos in self._graph_pos.items():
            screen_pos = self._figure.axes[0].transData.transform(data_pos)
            dist_sq = (screen_pos[0] - x) ** 2 + (screen_pos[1] - y) ** 2

            if dist_sq <= self._node_radius_sq:
                return obj

        return None

    def get_obj_from_name(self, node_name):
        """ Maps the given graph node name to the object it represents
        """
        return self._graph_name_to_obj.get(node_name)

    def get_name_from_obj(self, nengo_obj):
        """ Maps the given object to the name of the graph node representing it
        """
        return self._graph_obj_to_name.get(nengo_obj)

    def _associate_obj_name(self, node_name, nengo_obj):
        """ Updates the maps that associate graph node names and the objects
        that they represent. Since network objects aren't guaranteed to have
        unique names, they are modified to a similar but unique name. In order
        to keep the association, these maps are used.
        """
        self._graph_name_to_obj[node_name] = nengo_obj
        self._graph_obj_to_name[nengo_obj] = node_name

    def load_model(self, model):
        # Clear and initialize graph data
        self.model = model
        self.G = nx.MultiDiGraph()
        self._graph_name_to_obj = {}
        self._graph_obj_to_name = {}
        self._figure.clear()    

        if model is None:
            return

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

            pre_name = self.get_name_from_obj(conn.pre)
            post_name = self.get_name_from_obj(conn.post)

            if pre_name is None:
                print "Error: unable to determine connection's pre. Dropping edge \"%s\"." % (conn.pre)
                continue
            if pre_name is None:
                print "Error: unable to determine connection's post. Dropping edge \"%s\"." % (conn.pre)
                continue

            print "Adding edge: \"%s\" to \"%s\"" % (pre_name, post_name)
            self.G.add_edge(pre_name, post_name)

        # TODO(gmdavis): add probes?

        # Draw graph
        node_diam_sqr = (sqrt(self._node_radius_sq) * 2) ** 2

        axis = None
        if len(self._figure.axes) == 0:
            axis = self._figure.add_subplot(1,1,1)
        else:
            axis = self._figure.axes[0]

        self._graph_pos = nx.graphviz_layout(self.G, prog="neato")
        colors = [self.decide_obj_color(self.get_obj_from_name(obj)) for obj in self.G.nodes()]
        nx.draw(self.G, self._graph_pos, ax=axis, node_color=colors, node_size=node_diam_sqr)

    def decide_obj_color(self, nengo_obj):
        """ Provides a mapping between graph nodes and their desired colour.
        """
        if isinstance(nengo_obj, nengo.Node):
            return (1,1,0)
        if isinstance(nengo_obj, nengo.Ensemble):
            return (1,0,1)
        else:
            return (1,1,1) # white

    def onclick(self, event):
        self.nearest_obj(event.x, event.y)


#---------- Helper functions --------

def _find_uniq_name(name, collection, threashold=1000):
    """ Used to find a unique name in collection, based on the given name.
    """
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
    nv = NetworkView(sim_manager=None, controller=None, model=example.model)
    fig = nv.figure()
    fig.show()
    plt.show()

if __name__ == '__main__':
    main()