import nengo
import networkx as nx
import numpy
from matplotlib.collections import LineCollection
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
        self.canvas.connect("size_allocate", self.on_size_allocate)

        # Build graph
        self._node_radius = 10
        self._xlim = None
        self._ylim = None
        self._node_collection = None
        self._line_collection = None
        self.load_model(model)

        # Remove the invisible axes to get more drawing room
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

        # Used for grabbing + dragging node positions
        self.node_grabbed = None

        # Used for highlighting mouseover node
        self._last_highlighted = None

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
        if node_name in self._graph_name_to_obj:
            print "Warning: \"%s\" already in dictionary" % node_name
        if nengo_obj in self._graph_obj_to_name:
            print "Warning: \"%s\" already in dictionary" % nengo_obj

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
            pre, post = conn.pre, conn.post
            if isinstance(conn.pre, nengo.objects.Neurons):
                for obj in model.objs:
                    if isinstance(obj, nengo.Ensemble) and conn.pre == obj.neurons:
                        print "Warning: treating neuron connection as connection to parent ensemble", obj
                        pre = obj
            if isinstance(conn.post, nengo.objects.Neurons):
                for obj in model.objs:
                    if isinstance(obj, nengo.Ensemble) and conn.post == obj.neurons:
                        print "Warning: treating neuron connection as connection to parent ensemble", obj
                        post = obj

            pre_name = self.get_name_from_obj(pre)
            post_name = self.get_name_from_obj(post)

            if not pre_name:
                print "Error: unable to determine connection's pre. Dropping edge \"%s\"." % (pre)
                continue
            if not pre_name:
                print "Error: unable to determine connection's post. Dropping edge \"%s\"." % (pre)
                continue

            self.G.add_edge(str(pre_name), str(post_name))

        # establish color map
        objs = [self.get_obj_from_name(name) for name in self.G.nodes()]
        self._node_colors = [self.node_color(o) for o in objs]

        # build the graph layout
        pos = nx.graphviz_layout(self.G, prog="neato")
        self._node_positions = OrderedDict(pos)

        # Draw graph
        self.full_repaint()
        self.rebuild_kd_tree()

    def full_repaint(self):
        """ Clears and draws the network view.
        """
        self.axes.clear()
        if not self.model:
            return

        node_diam_sqr = (self._node_radius * 2) ** 2

        self._node_collection = nx.draw_networkx_nodes(self.G, self._node_positions, ax=self.axes, node_color=self._node_colors, node_size=node_diam_sqr)
        self._edge_collection = nx.draw_networkx_edges(self.G, self._node_positions, ax=self.axes, arrows=False)
        self._arrow_collection = self._draw_arrows(self.G, self._node_positions, ax=self.axes)
        self._label_collection = nx.draw_networkx_labels(self.G, self._node_positions, ax=self.axes, horizontalalignment='left')

        self.axes.set_axis_off()

        # Update the label positions (shifted right, off of the nodes)
        self._update_label_pos(self._node_positions)

        # Save the limits of the first draw, and restore them after each
        # additional repaint, to avoid autoresizing
        if not self._xlim:
            self._xlim = self.axes.get_xlim()
        if not self._ylim:
            self._ylim = self.axes.get_ylim()
        self.axes.set_xlim(self._xlim)
        self.axes.set_ylim(self._ylim)

        self.repaint()

    def _draw_arrows(self, G, pos,  ax):
        # Matplotlib's directed graph hack
        # draw thick line segments at head end of edge
        edge_pos = [(pos[n1], pos[n2]) for n1, n2 in self.G.edges()]
        arrow_pos = self._calc_arrow_pos(edge_pos)

        arrow_collection = LineCollection(arrow_pos,
                            colors = 'k',
                            linewidths = 4,
                            antialiaseds = (1,),
                            transOffset = ax.transData,
                            )
        arrow_collection.set_zorder(1) # edges go behind nodes
        ax.add_collection(arrow_collection)
        return arrow_collection

    def _calc_arrow_pos(self, edge_pos):
        arrow_pos=[]
        p=1.0-0.35 # make head segment 25 percent of edge length
        for src,dst in edge_pos:
            x1,y1=src
            x2,y2=dst
            dx=x2-x1 # x offset
            dy=y2-y1 # y offset
            d=numpy.sqrt(float(dx**2+dy**2)) # length of edge
            if d==0: # source and target at same position
                continue
            if dx==0: # vertical edge
                xa=x2
                ya=dy*p+y1
            if dy==0: # horizontal edge
                ya=y2
                xa=dx*p+x1
            else:
                theta=numpy.arctan2(dy,dx)
                xa=p*d*numpy.cos(theta)+x1
                ya=p*d*numpy.sin(theta)+y1

            arrow_pos.append(((xa,ya),(x2,y2)))
        return arrow_pos

    def _update_label_pos(self, node_pos):
        trans = self.axes.transData.transform
        invtrans = self.axes.transData.inverted().transform

        for node, pos in node_pos.items():
            x, y = trans(pos)
            x += self._node_radius * 1.5
            self._label_collection[node].set_position(invtrans((x, y)))

    def repaint(self):
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
            return (30/255.0, 144/255.0, 255/255.0, 1)
        if isinstance(nengo_obj, nengo.Ensemble):
            return (50/255.0, 205/255.0, 50/255.0, 1)
        else:
            return (1,1,1, 1) # white

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

        # Update node position
        new_pos = invtrans((x, y))
        self._node_positions[node_name] = new_pos

        # Update positions of attached edges + arrows
        pos = self._node_positions
        segs = [(pos[n1], pos[n2]) for n1, n2 in self.G.edges()]
        arrows = self._calc_arrow_pos(segs)

        # Updating matplotlib's collections will automatically update the view
        self._node_collection.set_offsets(pos.values())
        self._edge_collection.set_segments(segs)
        self._arrow_collection.set_segments(arrows)

        # Update label pos
        self._update_label_pos({node_name: new_pos})

        self.repaint()
        if rebuild_kd_tree:
            self.rebuild_kd_tree()

    def on_button_press(self, widget, event):
        if event.button == 1:
            node_name = self.node_at(event.x, event.y)
            if node_name:
                self.node_grabbed = node_name
                return True

        return False

    def on_button_release(self, widget, event, canvas):
        """ Overrides parent's method so it can decide which context menu items
        to add, in order to offer adding graphs based on clicked nengo object.
        """
        if event.button == 1:
            if self.node_grabbed:
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
        self.main_controller.add_plot_for_obj(vz, obj, cap)

    def on_mouse_motion(self, widget, event):
        if self.node_grabbed:
            self.move_node(self.node_grabbed, event.x, event.y, rebuild_kd_tree=False)
            event.request_motions()
            return True

        return self._update_node_highlighting(event.x, event.y)

    def _update_node_highlighting(self, x, y):
        curr = self.node_at(x, y)
        prev = self._last_highlighted

        if curr == prev:
            return curr is not None

        colors = self._node_collection.get_facecolors()

        if curr:
            idx = self.G.nodes().index(curr)
            r, g, b, a = colors[idx]
            c = 1.4
            colors[idx] = min(1, r*c), min(1, g*c), min(1, b*c), a

        if prev:
            idx = self.G.nodes().index(prev)
            colors[idx] = self.node_color(self.get_obj_from_name(prev))

        if curr or prev:
            self._node_collection.set_facecolors(colors)
            self.repaint()
            self._last_highlighted = curr
            return True

        return False

    def on_size_allocate(self, widget, allocation):
        self._update_label_pos(self._node_positions)

    def store_layout(self):
        """Returns a dictionary representing the
        current node positions
        """
        node_pos = { name: (pos[0], pos[1]) for name, pos in self._node_positions.items()}
        layout_dict = {"node_positions" : node_pos}
        return layout_dict

    def restore_layout(self, layout):
        """Restores node positions from layout
        dictionary
        """
        # Update node position
        self._node_positions = layout["node_positions"]

        # Update positions of attached edges + arrows
        pos = self._node_positions
        segs = [(pos[n1], pos[n2]) for n1, n2 in self.G.edges()]
        arrows = self._calc_arrow_pos(segs)

        # Updating matplotlib's collections will automatically update the view
        self._node_collection.set_offsets(pos.values())
        self._edge_collection.set_segments(segs)
        self._arrow_collection.set_segments(arrows)

        # Update label pos
        self._update_label_pos(pos)

        self.rebuild_kd_tree()
        self.repaint()

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
