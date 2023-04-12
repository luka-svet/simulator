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


class AntimicrobialAssortment(object):

    def __init__(self, antimicrobials, language, graph_y_axis):

        self._graph_widget =\
            Graph(xlabel=language["graph_x_axis"], ylabel=language[graph_y_axis],
                  xmin=0, xmax=10, x_ticks_major=1, x_ticks_minor=4, x_grid_label=True,
                  ymin=0, ymax=20, y_ticks_major=4, y_ticks_minor=5, y_grid_label=True,
                  padding=3, font_size=13, **{'background_color': (0.25, 0.25, 0.25),
                                'border_color': (0.27, 0.27, 0.27),
                                'tick_color': (0.5, 0.5, 0.5)})  # Graph

        self._antimicrobials = antimicrobials  # dict[Antimicrobial]

        # scheduled function calls (clocks) must be strong referenced, otherwise will not work
        self._clocks = []  # list[Clock]
        for _antimicrobial in self._antimicrobials.values():
            self._clocks.append(
                Clock.schedule_interval(
                    xy_max_resize(_antimicrobial.get_plot(),
                                  self._graph_widget), 1 / 60.))

            # add each antimicrobial plot to the main graph
            self._graph_widget.add_plot(_antimicrobial.get_plot())

    def get_graph_widget(self):

        return self._graph_widget

    def get_antimicrobials(self):

        return self._antimicrobials

    def get_clocks(self):

        return self._clocks
