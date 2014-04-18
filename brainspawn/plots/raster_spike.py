from plots.base_plot import registered_plot
from plots.plot import Plot
import settings

@registered_plot
class RasterSpike(Plot):

    WINDOW_SIZE = 100

    def __init__(self, main_controller, obj, cap):
        super(RasterSpike, self).__init__(main_controller, obj, cap)

        self.axes = self.figure.add_subplot(111)
        self.axes.patch.set_alpha(0.0)
        self.axes.set_title(self.title)
        self.axes.set_ylabel("Neurons")
        self.axes.set_xlabel("Time (s)")
        #TODO: The 1.0 here shouldn't be hardcoded, as with all plots
        self._initial_end_time = 1.0 * self.WINDOW_SIZE / settings.MAX_WINDOW_SIZE
        self.axes.set_xlim([0, self._initial_end_time])
        self._image = None

    @staticmethod
    def plot_name():
        return "Raster Spike"

    @staticmethod
    def supports_cap(cap):
        return cap.name in ["spikes"]

    def update(self, start_step, step_size, spikes):
        if self._image:
            self._image.remove()
            self._image = None
        if len(spikes) == 0:
            return
        spikes_view = spikes[-self.WINDOW_SIZE:]
        end_step = start_step + spikes.shape[0]
        start_time = (end_step - spikes_view.shape[0]) * step_size
        end_time = end_step * step_size
        self._image = self.axes.imshow(  # interpolation="none" is not supported on cairo
                spikes_view.T, cmap="binary", aspect="auto", interpolation="nearest", origin="lower",
                extent=(start_time, end_time, 0, spikes_view.shape[1]))
        
        self.set_default_xlim(max(end_time, self._initial_end_time), self._initial_end_time)
