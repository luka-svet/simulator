# Modelling the dynamics of different microbial populations in various environmental conditions: implications for the emergence and spread of antimicrobial resistance
#
# Copyright 2018-2019 Pedro HC David <https://github.com/Kronopt> and SimulATe contributors
# Copyright 2019-2023 Luka Svet <luka.svet@kuleuven.be>
#
# The following code is a derivative work of the code from the Mercurial project,
# which is licensed under GPLv3. This code therefore is also licensed under the terms
# of the GNU General Public License, version 3.

from kivy.clock import Clock
from bin.deps.kivy_graph import Graph
from bin.functions.graphs import xy_max_resize


class Microbiome(object):

    _total_microbiomes = 0  # int

    def __init__(self,
                 name,
                 microbes,
                 language,
                 graph_y_axis,
                 relative_frequency=False):

        if relative_frequency:
            ymin = 0.0001
            ymax = 1
        else:
            ymin = 0.001
            ymax = 1000

        self._graph_widget = Graph(xlabel=language["graph_x_axis"],
                                   ylabel=language[graph_y_axis],
                                   xmin=0,
                                   xmax=10,
                                   x_ticks_major=1,
                                   x_ticks_minor=4,
                                   x_grid_label=True,
                                   ymin=ymin,
                                   ymax=ymax,
                                   y_ticks_major=1,
                                   y_ticks_minor=7,
                                   y_grid_label=True,
                                   ylog=True,
                                   padding=3,
                                   font_size=13,
                                   **{
                                       'background_color': (0.25, 0.25, 0.25),
                                       'border_color': (0.27, 0.27, 0.27),
                                       'tick_color': (0.5, 0.5, 0.5)
                                   })  # Graph

        self._id = 'mic' + str(Microbiome._total_microbiomes)  # str
        self._name = name  # str
        self._microbes = microbes  # dict[Microbes]

        # scheduled function calls (clocks) must be strong referenced, otherwise will not work
        self._clocks = []  # list[Clock]
        for _microbes in sorted(
                iter(self._microbes.keys()),
                reverse=True):  # sorted so that "total" plots come in first
            self._clocks.append(
                Clock.schedule_interval(
                    xy_max_resize(self._microbes[_microbes].get_plot(),
                                  self._graph_widget, "log"), 1 / 60.))

            # add each microbes plot to the main graph
            self._graph_widget.add_plot(self._microbes[_microbes].get_plot())

        Microbiome._total_microbiomes += 1

    @staticmethod
    def get_total_microbiomes():

        return Microbiome._total_microbiomes

    def get_graph_widget(self):

        return self._graph_widget

    def get_id(self):

        return self._id

    def get_name(self):

        return self._name

    def get_microbes(self):

        return self._microbes

    def get_clocks(self):

        return self._clocks
