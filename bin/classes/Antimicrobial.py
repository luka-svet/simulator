# Modelling the dynamics of different microbial populations in various environmental conditions: implications for the emergence and spread of antimicrobial resistance
#
# Copyright 2018-2019 Pedro HC David <https://github.com/Kronopt> and SimulATe contributors
# Copyright 2019-2023 Luka Svet <luka.svet@kuleuven.be>
#
# The following code is a derivative work of the code from the Mercurial project,
# which is licensed under GPLv3. This code therefore is also licensed under the terms
# of the GNU General Public License, version 3.

from colorsys import hsv_to_rgb
from bin.deps.kivy_graph import SmoothLinePlot
from bin.functions.helper_functions import NewColor


class Antimicrobial(object):

    _total_antimicrobials = 0  # int

    def __init__(self, name):

        self._id = 'ant' + str(Antimicrobial._total_antimicrobials)  # str
        self._name = name  # str
        self._line_color = hsv_to_rgb(*NewColor.new_color())  # (R,G,B)
        self._plot = SmoothLinePlot(points=[(0, 0)],
                                    color=self._line_color)  # SmoothLinePlot

        Antimicrobial._total_antimicrobials += 1

    @staticmethod
    def get_total_antimicrobials():

        return Antimicrobial._total_antimicrobials

    def get_id(self):

        return self._id

    def get_name(self):

        return self._name

    def get_line_color(self):

        return self._line_color

    def get_plot(self):

        return self._plot
