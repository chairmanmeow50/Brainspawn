import nengo
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree as KDTree
from collections import OrderedDict

from view.visualizations.plot import Plot

from gi import pygtkcompat
pygtkcompat.enable()
pygtkcompat.enable_gtk(version="3.0")
import gtk

class NetworkView(Plot):
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
        self._node_radius = 10
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
        if not self.model or not self._kdtree:
            return None

        w, h = self.view._canvas.get_width_height()

        if (w,h) != self._kdtree_creation_dim:
            self.rebuild_kd_tree()

        # Invert the y coordinate so origin is bottom left (matches networkx coords)
        y = h - y

        # Check if we hit a node. The returned index corresponds
        # to the list given to the KDTree on creation.
        d, hit_index = self._kdtree.query((x, y), distance_upper_bound=self._node_radius)
        if hit_index == len(self._graph_pos):
            return None

        return self._graph_pos.keys()[hit_index]

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
        self._graph_pos = None
        self._kdtree = None
        self.view.figure.clear()

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

            if name:
                self.G.add_node(name, obj=obj)
                self._associate_obj_name(name, obj)
            else:
                print "Warning: unable to add object:", str(obj)

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

        # establish color map
        objs = [self.get_obj_from_name(name) for name in self.G.nodes()]
        self._node_colors = [self.node_color(o) for o in objs]

        # build the graph layout
        self._graph_pos = OrderedDict(nx.graphviz_layout(self.G, prog="neato"))

        # Draw graph
        self.repaint()
        self.rebuild_kd_tree()

    def repaint(self):
        """ Clears and draws the network view.
        """
        self.view.figure.clear()
        if not self.model:
            return

        axis = None
        if len(self.view.figure.axes) == 0:
            axis = self.view.figure.add_subplot(1,1,1)
        else:
            axis = self.view.figure.axes[0]

        node_diam_sqr = (self._node_radius * 2) ** 2
        nx.draw(self.G, self._graph_pos, ax=axis, node_color=self._node_colors, node_size=node_diam_sqr)

        self.view.canvas.queue_draw()

    def rebuild_kd_tree(self):
        """ Recalculates the K-D tree used to find graph nodes. Since it's in
        display coordinates, it must be recalculated every time the figure's
        size changes.
        """
        if not self.model:
            self._kdtree = None
            return

        # Remember the creation dimensions
        self._kdtree_creation_dim = self.view._canvas.get_width_height()

        axis = self.view.figure.axes[0]
        transform = axis.transData.transform
        display_coords = [transform(node_pos) for node_pos in self._graph_pos.values()]
        self._kdtree = KDTree(display_coords)

    def node_color(self, nengo_obj):
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
