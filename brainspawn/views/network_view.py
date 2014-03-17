import nengo
import networkx as nx
from scipy.spatial import cKDTree as KDTree
from collections import OrderedDict

from views.canvas_item import CanvasItem

from gi import pygtkcompat
pygtkcompat.enable()
pygtkcompat.enable_gtk(version="3.0")
import gtk

class NetworkView(CanvasItem):
    """ Visualization of a model's network
    """
    def __init__(self, controller, model=None, **kwargs):
        super(NetworkView, self).__init__(controller)
        self._model = model
        self.axes = self.figure.add_subplot(111)

        self.plots_menu_item = gtk.MenuItem("Plots")
        self._context_menu.append(self.plots_menu_item)

        self.canvas.connect("button_press_event", self.on_button_press)
        self.canvas.connect("motion_notify_event", self.on_mouse_motion)

        # Build graph
        self._node_radius = 10
        self._xlim = None
        self._ylim = None
        self.load_model(model)

        # Remove the invisible axes to get more drawing room
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

        # Used for grabbing + dragging node positions
        self.node_grabbed = None

    def node_at(self, x, y):
        if not self.model or not self._kdtree:
            return None

        w, h = self.canvas.get_width_height()

        if (w,h) != self._kdtree_creation_dim:
            self.rebuild_kd_tree()

        # Invert the y coordinate so origin is bottom left (matches networkx coords)
        y = h - y

        # Check if we hit a node. The returned index corresponds
        # to the list given to the KDTree on creation.
        d, hit_index = self._kdtree.query((x, y), distance_upper_bound=self._node_radius)
        if hit_index == len(self._node_positions):
            return None

        return self._node_positions.keys()[hit_index]

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
        self._node_positions = None
        self._kdtree = None
        self._xlim = None
        self._ylim = None
        self.axes.clear()

        if model is None:
            return

        # Add ensembles and nodes
        for obj in model.objs:
            name = None
            if isinstance(obj, nengo.Ensemble):
                name = _find_uniq_name(obj.label, self.G.nodes())
            elif isinstance(obj, nengo.Node):
                name = _find_uniq_name(obj.label, self.G.nodes())
            else:
                print "Warning: model object not recognised: \"", str(obj), "\"."
                name = str(obj)

            if name:
                self.G.add_node(name, obj=obj)
                self._associate_obj_name(name, obj)
            else:
                print "Warning: unable to add object:", str(obj)

        # Add connections
        for conn in model.connections:
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
        self._node_positions = OrderedDict(nx.graphviz_layout(self.G, prog="neato"))

        # Draw graph
        self.repaint()
        self.rebuild_kd_tree()

    def repaint(self):
        """ Clears and draws the network view.
        """
        self.axes.clear()
        if not self.model:
            return

        node_diam_sqr = (self._node_radius * 2) ** 2
        nx.draw(self.G, self._node_positions, ax=self.axes, node_color=self._node_colors, node_size=node_diam_sqr)

        # Save the limits of the first draw, and restore them after each
        # additional repaint, to avoid autoresizing
        if not self._xlim:
            self._xlim = self.axes.get_xlim()
        if not self._ylim:
            self._ylim = self.axes.get_ylim()
        self.axes.set_xlim(self._xlim)
        self.axes.set_ylim(self._ylim)

        self.canvas.queue_draw()

    def rebuild_kd_tree(self):
        """ Recalculates the K-D tree used to find graph nodes. Since it's in
        display coordinates, it must be recalculated every time the figure's
        size changes.
        """
        if not self.model:
            self._kdtree = None
            return

        # Remember the creation dimensions
        self._kdtree_creation_dim = self.canvas.get_width_height()

        transform = self.axes.transData.transform
        display_coords = [transform(node_pos) for node_pos in self._node_positions.values()]
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

    def move_node(self, node_name, x, y, rebuild_kd_tree=True):
        """ All coordinates, unless otherwise mentioned, are in screen coordinates
        """
        w, h = self.canvas.get_width_height()
        # Invert the y coordinate so origin is bottom left (matches networkx coords)
        y = h - y

        trans = self.axes.transData.transform
        invtrans = self.axes.transData.inverted().transform

        xmin, ymin = trans((self._xlim[0], self._ylim[0]))
        xmax, ymax = trans((self._xlim[1], self._ylim[1]))

        correction_factor = 4
        xmin += self._node_radius + correction_factor
        xmax -= self._node_radius + correction_factor
        ymin += self._node_radius + correction_factor
        ymax -= self._node_radius + correction_factor
        x = max(xmin, min(xmax, x))
        y = max(ymin, min(ymax, y))

        self._node_positions[node_name] = invtrans((x, y))
        self.repaint()
        if rebuild_kd_tree:
            self.rebuild_kd_tree()

    def on_button_press(self, widget, event):
        if event.button == 1:
            node_name = self.node_at(event.x, event.y)
            if node_name:
                self.node_grabbed = node_name
                print "Grabbing:", self.node_grabbed, "at (%.0f, %.0f) " % (event.x, event.y)
                return True

        return False

    def on_button_release(self, widget, event, canvas):
        """ Overrides parent's method so it can decide which context menu items
        to add, in order to offer adding graphs based on clicked nengo object.
        """
        if event.button == 1:
            if self.node_grabbed:
                print "Released:", self.node_grabbed, "at (%.0f, %.0f) " % (event.x, event.y)
                self.rebuild_kd_tree()
                self.node_grabbed = None
                return True
        if event.button == 3:
            node_name = self.node_at(event.x, event.y)

            self._context_menu.remove(self.plots_menu_item)

            if node_name:
                obj = self.get_obj_from_name(node_name)
                supported = self.main_controller.plots_for_object(obj)
                submenu = gtk.Menu()

                for (vz, obj, cap) in supported:
                    item = gtk.MenuItem("%s (%s)" % (vz.plot_name(), cap.name))
                    # Hack: b-p-e connect (instead of "activate") is a workaround for
                    # submenu item not getting activate signal unless the submenu is
                    # also clicked. b-p-e works but has the extra event arg, discarded
                    # by the call-through
                    item.connect("button-press-event", self._call_through, vz, obj, cap)
                    submenu.append(item)

                self.plots_menu_item.set_submenu(submenu)
                self._context_menu.append(self.plots_menu_item)
                self._context_menu.show_all()

            return super(NetworkView, self).on_button_release(widget, event, canvas)
        return False

    def _call_through(self, widget, event, vz, obj, cap):
        self.main_controller.add_plot_for_obj(widget, vz, obj, cap)

    def on_mouse_motion(self, widget, event):
        if self.node_grabbed:
            self.move_node(self.node_grabbed, event.x, event.y, rebuild_kd_tree=False)
            event.request_motions()
            return True
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
