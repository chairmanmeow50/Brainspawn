import nengo
import networkx as nx
import matplotlib.pyplot as plt

from gi import pygtkcompat
pygtkcompat.enable()
pygtkcompat.enable_gtk(version="3.0")
import gtk
from math import sqrt
from view.visualizations._visualization import Visualization

class NetworkView(Visualization):
    """ Visualization of a model's network
    """
    def __init__(self, controller, model=None, name="Network View", **kwargs):
        super(NetworkView, self).__init__(controller, None, None)
        self._model = model
        self.name = name

        self.menu_items = []

        # Hmmm.. we need to spit controller/view functionality here?
        self.view.button_press = self.button_press

        # Build graph
        self._node_radius_sq = 100
        self.load_model(model)

    @staticmethod
    def plot_name():
        return 'Network View'

    @staticmethod
    def supports_cap(cap):
        return False

    def update(self, start_step, step_size, data):
        pass

    def remove_plot(self, widget, canvas):
        pass

    def node_at(self, x, y):
        if self.model is None:
            return None

        for name, data_pos in self._graph_pos.items():
            screen_pos = self.view._figure.axes[0].transData.transform(data_pos)
            w, h = self.view._canvas.get_width_height()
            dist_sq = (screen_pos[0] - x) ** 2 + (screen_pos[1] - (h - y)) ** 2

            if dist_sq <= self._node_radius_sq:
                return name

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
        self.view._figure.clear()

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
            elif isinstance(obj, nengo.Node):
                # print "obj.label      = ", obj.label
                # print "obj.dimensions = ", obj.size_out
                # print "obj.output     = ", obj.output
                # print "obj.probes     = ", obj.probes
                name = _find_uniq_name(obj.label, self.G.nodes())
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

            self.G.add_edge(pre_name, post_name)

        # Draw graph
        node_diam_sqr = (sqrt(self._node_radius_sq) * 2) ** 2

        axis = None
        if len(self.view._figure.axes) == 0:
            axis = self.view._figure.add_subplot(1,1,1)
        else:
            axis = self.view._figure.axes[0]

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

    def button_press(self, widget, event, canvas):
        """ Overrides parent's method so it can decide which context menu items
        to add, in order to offer adding graphs based on clicked nengo object.
        """
        if event.button == 3:
            node_name = self.node_at(event.x, event.y)

            for item in self.menu_items:
                self.view.context_menu.remove(item)
            self.menu_items = []

            if node_name is not None:
                obj = self.get_obj_from_name(node_name)
                supported = self.main_controller.plots_for_object(obj)

                for (vz, obj, cap) in supported:
                    item = gtk.MenuItem("View: " + vz.plot_name() + '-' + cap.name)
                    item.connect("activate", self.main_controller.add_plot_for_obj, vz, obj, cap)
                    self.view.context_menu.append(item)

                    self.menu_items.append(item)
                self.view.context_menu.show_all()

            return super(NetworkView, self).button_press(widget, event, canvas)
        return False

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

    # print "Warning: modifying original name to \"%s\" to make it unique." % (name)
    return name

#---------- Main method (testing) --------

import sample_networks.large_network as example

def main():
    nv = NetworkView(controller=None, model=example.model)
    plt.show()

if __name__ == '__main__':
    main()
