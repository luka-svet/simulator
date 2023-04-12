# Modelling the dynamics of different microbial populations in various environmental conditions: implications for the emergence and spread of antimicrobial resistance
#
# Copyright 2018-2019 Pedro HC David <https://github.com/Kronopt> and SimulATe contributors
# Copyright 2019-2020 Luka Svet <luka.svet@kuleuven.be>
#
# The following code is a derivative work of the code from the Mercurial project,
# which is licensed under GPLv3. This code therefore is also licensed under the terms
# of the GNU General Public License, version 3.

import os
from colorsys import hsv_to_rgb
from kivy.clock import Clock
from bin.deps.kivy_graph import SmoothLinePlot
from bin.classes.Antimicrobial import Antimicrobial
from bin.classes.AntimicrobialAssortment import AntimicrobialAssortment
from bin.classes.Microbes import Microbes
from bin.classes.Microbiome import Microbiome
from bin.functions.graphs import xy_max_resize
from bin.functions.helper_functions import NewColor, XMLTextParser

# Language
language = "en"  # if translations are missing, defaults to english
LANGUAGE = XMLTextParser("string",
                         language).parse(os.path.join("bin", "ui", "text.xml"))
DEFAULT_LANGUAGE = dict(LANGUAGE)  # copy language dict

# Antimicrobials
ANTIMICROBIALS = {
    "Generic Antimicrobial": Antimicrobial("Generic Antimicrobial")
}
ANTIMICROBIAL_ASSORTMENT = AntimicrobialAssortment(
    ANTIMICROBIALS, LANGUAGE, "graph_antimicrobial_y_axis")

# Microbes
MICROBES = {
    "Sensitive": Microbes("Sensitive"),
    "Resistant": Microbes("Resistant"),
    "SensitiveBF": Microbes("SensitiveBF"),
    "ResistantBF": Microbes("ResistantBF"),
    "Total": Microbes("Total", (0.4, 0.4, 0.4))
}
MICROBES_ASSORTMENT = Microbiome("Generic Microbiome", MICROBES, LANGUAGE,
                                 "graph_microbes_y_axis")

# Immune System
immune_system_color = hsv_to_rgb(*NewColor.new_color())
IMMUNE_PLOT = SmoothLinePlot(
    points=[(0, 0.001)],
    color=immune_system_color,
)
immune_plot_clock = Clock.schedule_interval(
    xy_max_resize(IMMUNE_PLOT, MICROBES_ASSORTMENT.get_graph_widget(), "log"),
    1 / 60.)

# Density limit
DEATH_LIMIT = SmoothLinePlot(points=[], color=(0, 0, 0))
GROWTH_LIMIT = SmoothLinePlot(points=[], color=(0.141, 0.901, 0.039))
GROWTH_LIMIT_BF = SmoothLinePlot(points=[], color=(0.039, 0.121, 0.901))
MICROBES_ASSORTMENT.get_graph_widget().add_plot(IMMUNE_PLOT)
MICROBES_ASSORTMENT.get_graph_widget().add_plot(DEATH_LIMIT)
MICROBES_ASSORTMENT.get_graph_widget().add_plot(GROWTH_LIMIT)
MICROBES_ASSORTMENT.get_graph_widget().add_plot(GROWTH_LIMIT_BF)
