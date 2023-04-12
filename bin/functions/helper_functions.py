# Modelling the dynamics of different microbial populations in various environmental conditions: implications for the emergence and spread of antimicrobial resistance
#
# Copyright 2018-2019 Pedro HC David <https://github.com/Kronopt> and SimulATe contributors
# Copyright 2019-2023 Luka Svet <luka.svet@kuleuven.be>
#
# The following code is a derivative work of the code from the Mercurial project,
# which is licensed under GPLv3. This code therefore is also licensed under the terms
# of the GNU General Public License, version 3.

import xml.parsers.expat as xml
from math import sqrt
from random import random, seed


class NewColor(object):

    golden_ratio = (1 + sqrt(5)) / 2

    seed(100)  # enables the same colors to be generated between simulations
    CURRENT_COLOR = (random(), 0.7, 0.95)  # (H,S,V), random initial color

    microbes_already_colored = {}  # dict[HSV]

    @staticmethod
    def new_color(microbes_name=None):

        def update_random_color():
            # generates a new random hue, saves the new HSV and returns it
            new_h = (NewColor.CURRENT_COLOR[0] + 1 / NewColor.golden_ratio) % 1
            NewColor.CURRENT_COLOR = new_h, NewColor.CURRENT_COLOR[
                1], NewColor.CURRENT_COLOR[2]
            return NewColor.CURRENT_COLOR

        if microbes_name is None:
            # if no name is provided, simply generate a new color and return it
            return update_random_color()
        else:
            # check if microbe already has a color
            if microbes_name in NewColor.microbes_already_colored:
                # if it has, returns it without generating a new color
                return NewColor.microbes_already_colored[microbes_name]
            else:
                # generates a new color, saves it, inserts its value into dict and returns it
                NewColor.microbes_already_colored[
                    microbes_name] = update_random_color()
                return NewColor.microbes_already_colored[microbes_name]


class XMLTextParser(object):

    def __init__(self, element, lang):

        self.element = element
        self.lang = lang  # str
        self.xml_parser = xml.ParserCreate()  # xml
        self.corresponding_element = False  # bool
        self.last_element = ""  # str
        self.strings_dict = {}  # dict[str]

    def start_element(self, name, attributes):

        if name == self.element and attributes["language"] == self.lang:
            self.strings_dict[
                attributes["id"]] = None  # char_data then fills this
            self.last_element = attributes["id"]
            self.corresponding_element = True

    def char_data(self, data):

        if data != "\n" and self.corresponding_element:
            self.strings_dict[self.last_element] = data
            self.corresponding_element = False

    def parse(self, xml_file):

        with open(xml_file, "rb") as xml_file_object:
            self.xml_parser.StartElementHandler = self.start_element
            self.xml_parser.CharacterDataHandler = self.char_data

            self.xml_parser.ParseFile(xml_file_object)

        return self.strings_dict
